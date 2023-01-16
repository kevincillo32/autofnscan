import os
import re

folder_name = input("Ingrese el nombre de la carpeta principal: ")

while True:
    ip_address = input("Ingrese la dirección IP: ")
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip_address):
        break
    else:
        print("Dirección IP no válida. Inténtelo de nuevo.")

os.mkdir(folder_name)
os.mkdir(folder_name + '/nmap')
os.mkdir(folder_name + '/content')
os.mkdir(folder_name + '/exploits')
os.mkdir(folder_name + '/scripts')
print(f"Carpetas creadas exitosamente en {folder_name}")
print(f"La dirección IP ingresada es: {ip_address}")


ping = os.popen("ping -c 3 " + ip_address).read()
ttl = re.search(r"ttl=(\d+)", ping)

if ttl:
    ttl = int(ttl.group(1))
    if ttl <= 64:
        os = "Windows"
    elif ttl <= 128:
        os = "Linux"
    else:
        os = "Otro"
    print(f"El sistema operativo de la máquina {ip_address} es: {os}")
else:
    print("No se pudo determinar el sistema operativo de la máquina")

nmap_cmd = "nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn " + ip_address + " -oG " + folder_name + "/nmap/allPortsTCP"

os.system(nmap_cmd)
print(f"El resultado del escaneo se ha guardado en {folder_name}/nmap/allPortsTCP")
