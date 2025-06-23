import subprocess

# This script retrieves and prints the current system's hostname, OS name, and memory usage.
with open("/etc/os-release") as os:
    lines=os.readlines()
    os_final=lines[6].split("=")
    os_final[1] = os_final[1].replace('"','')
    print(os_final[1])

status_memory= subprocess.run(["free", "-h"],capture_output=True, text=True)
status_disk = subprocess.run(["df", "-h", "--total"], capture_output=True, text=True)
cpu_usage = subprocess.run(
    "top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'",
    shell=True, capture_output=True, text=True
)
top_five_processes_by_cpu = subprocess.run(["ps aux --sort=-%cpu | head -n 6"], shell=True, capture_output=True, text=True)
top_five_processes_by_mem = subprocess.run(["ps aux --sort=-%mem | head -n 6"], shell=True, capture_output=True, text=True)


disk_total = status_disk.stdout.splitlines()[-1].split()

mem_status=(status_memory.stdout.splitlines()[1])
mem_values = mem_status.split()

mem_usage_percent = int(mem_values[-1].replace('Gi',''))
mem_total_percent = int(mem_values[1].replace('Gi',''))

mem_usage_percent = round((mem_usage_percent * 100) / mem_total_percent, 2)
mem_free_percent = 100 - mem_usage_percent

print("Mem Total", mem_values[1])
print("Mem Usage", mem_values[2], mem_usage_percent,"%")
print("Mem Free", mem_values[-1], mem_free_percent,"%","\n")


print("Disk Total", disk_total[1])
print("Disk Used", disk_total[2] , disk_total[-2])
print("Disk Free", disk_total[3], (100 - int(disk_total[-2].replace('%', ''))), "%","\n")

print("CPU Usage", cpu_usage.stdout.strip() if cpu_usage.stdout.strip() != "" else "0", "%","\n")

print("Top 5 Processes By CPU Usage")
for process in top_five_processes_by_cpu.stdout.splitlines():
    print(process)
print("\n") 
print("Top 5 Processes By Memory Usage")
for process in top_five_processes_by_mem.stdout.splitlines():
    print(process)
