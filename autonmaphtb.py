import os
import re
from termcolor import colored

folder_name = input(colored("Ingrese el nombre de la carpeta principal: ", "cyan"))
while True:
    ip_address = input(colored("Ingrese la dirección IP: ", "cyan"))
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip_address):
        break
    else:
        print(colored("Dirección IP no válida. Inténtelo de nuevo.", "red"))

os.mkdir(folder_name)
os.mkdir(folder_name + '/nmap')
os.mkdir(folder_name + '/content')
os.mkdir(folder_name + '/exploits')
os.mkdir(folder_name + '/scripts')
print(colored(f"Carpetas creadas exitosamente en {folder_name}", "green"))
print(colored(f"La dirección IP ingresada es: {ip_address}", "green"))


ping = os.popen("ping -c 3 " + ip_address).read()
ttl = re.search(r"ttl=(\d+)", ping)

if ttl:
    ttl = int(ttl.group(1))
    if ttl <= 64:
        sistema_operativo = "Windows"
    elif ttl <= 128:
        sistema_operativo = "Linux"
    else:
        sistema_operativo = "Otro"
    print(colored(f"El sistema operativo de la máquina {ip_address} es: {sistema_operativo}", "green"))
else:
    print(colored("No se pudo determinar el sistema operativo de la máquina", "red"))

nmap_cmd = "nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn " + ip_address + " -oG " + folder_name + "/nmap/allPortsTCP"

os.system(nmap_cmd)
print(colored(f"El resultado del escaneo se ha guardado en {folder_name}/nmap/allPortsTCP", "green"))
