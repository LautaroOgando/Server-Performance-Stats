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

top_five_processes_by_cpu = subprocess.run(
            r"""ps aux --sort=-%cpu | awk 'NR>1 {printf "%-10s %-8s %-6s %-6s %-s\n", $1, $2, $3, $4, $11}' | head -n 5""",
        shell=True,             # Indispensable para ejecutar pipelines
        capture_output=True,    # Captura la salida
        text=True,              # Decodifica como texto
        check=True              # Lanza excepción si el comando falla
        ).stdout.strip()

top_five_processes_by_mem = subprocess.run(
            r"""ps aux --sort=-%mem | awk 'NR>1 {printf "%-10s %-8s %-6s %-6s %-s\n", $1, $2, $3, $4, $11}' | head -n 5""",
        shell=True,             # Indispensable para ejecutar pipelines
        capture_output=True,    # Captura la salida
        text=True,              # Decodifica como texto
        check=True              # Lanza excepción si el comando falla
        ).stdout.strip()



uptime = subprocess.run("uptime | awk '{sub(/,$/, \"\", $4); print $3, $4}'", shell=True, capture_output=True, text=True)
user_live=subprocess.run("uptime | awk '{sub(/,$/, \"\", $7); print $6, $7}'", shell=True, capture_output=True, text=True)

print("Uptime:",uptime.stdout.strip(),"\n")
print("Users Now:",user_live.stdout.strip(),"\n")

disk_total = status_disk.stdout.splitlines()[-1].split()

mem_status=(status_memory.stdout.splitlines()[1])
mem_values = mem_status.split()

mem_usage_percent = float(mem_values[2].replace('Gi',''))
mem_total_percent = float(mem_values[1].replace('Gi',''))
mem_free_percent = float(mem_values[3].replace('Gi',''))
mem_available_percent = float(mem_values[-1].replace('Gi',''))
mem_free_percent = round((mem_free_percent * 100) / mem_total_percent, 2)
mem_usage_percent = round((mem_usage_percent * 100) / mem_total_percent, 2)
mem_available_percent=round((mem_available_percent * 100) / mem_total_percent, 2)

print("Mem Total", mem_values[1])
print(f"Mem Usage {mem_values[2]} ({mem_usage_percent}%)")
print(f"Mem Free {mem_values[3]} ({mem_free_percent}%)")
print(f"Mem Available {mem_values[-1]} ({mem_available_percent}%)\n")

disk_free_percent=100 - int(disk_total[-2].replace('%', ''))
print("Disk Total", disk_total[1])
print(f"Disk Used {disk_total[2]} ({disk_total[-2]})")
print(f"Disk Free {disk_total[3]} ({disk_free_percent}%)\n")

print("CPU Usage", cpu_usage.stdout.strip() if cpu_usage.stdout.strip() != "" else "0", "%","\n")

print("Top Five Processes By CPU:\n")
print(f"{'USER':<10} {'PID':<8} {'%CPU':<6} {'%MEM':<6} COMMAND")
print(top_five_processes_by_cpu,"\n")

print("Top Five Processes By MEM:\n")
print(f"{'USER':<10} {'PID':<8} {'%CPU':<6} {'%MEM':<6} COMMAND")
print(top_five_processes_by_mem)
