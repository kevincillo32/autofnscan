from termcolor import colored
import os
import re

class Carpeta:
    def __init__(self, nombre):
        self.nombre = nombre
        
    def crear_carpeta(self, subcarpeta):
        path = self.nombre + "/" + subcarpeta
        os.makedirs(path, exist_ok=True)
        return path

def determinar_sistema_operativo(ip_address):
    sistema_operativo = "Otro"
    ping = os.popen("ping -c 3 " + ip_address + " | grep ttl").read()
    ttl = re.search(r"ttl=(\d+)", ping)
    if ttl:
        ttl = int(ttl.group(1))
        so = {
            0: "Otro",
            64: "Linux",
            128: "Windows"
        }
        for key in so:
            if ttl <= key:
                sistema_operativo = so[key]
                break
    return sistema_operativo

def escanear_puertos(ip_address, folder_name):
    # Escanear todos los puertos TCP
    nmap_cmd = f"nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn {ip_address} -oG {folder_name}/nmap/allPortsTCP"
    os.system(nmap_cmd)

    # Abrir el archivo allPortsTCP y obtener solo los puertos abiertos
    with open(f'{folder_name}/nmap/allPortsTCP', 'r') as file:
        puertos = [line.split()[1] for line in file if line.startswith("Ports:")]
    # Unir los puertos con comas
    puertos = ",".join(puertos)
    # Copiar los puertos a la clipboard
    os.system(f'echo {puertos} | xclip -selection clipboard')

    # Pedir al usuario los puertos a escanear
    puertos_escanear = input("Introduce los puertos a escanear: ")
    nmap_cmd = f"nmap -sCV -p {puertos_escanear} {ip_address} -oN {folder_name}/nmap/targeted"
    os.system(nmap_cmd)

# Crear la carpeta principal
folder_name = input("Introduce el nombre de la carpeta principal: ")
folder = Carpeta(folder_name)

# Crear subcarpetas
folders = ['nmap', 'content', 'exploits', 'scripts']
for folder_name in folders:
    folder.crear_carpeta(folder_name)

# Pedir al usuario la dirección IP
ip_address = input("Introduce la dirección IP: ")

# Determinar el sistema operativo
sistema_operativo = determinar_sistema_operativo(ip_address)
print(colored(f"El sistema operativo de la máquina {ip_address} es: {sistema_operativo}", "green"))

# Escanear puertos
escanear_puertos(ip_address, folder_name)
