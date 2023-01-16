import os
import re
import pyperclip

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
            64: "Windows",
            128: "Linux"
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
    pyperclip.copy(puertos)
    print("Los puertos abiertos se han copiado a la clipboard")
    # Pedir al usuario que ingrese los puertos escaneados
    puertos = input("Ingresa los puertos escaneados (separados por comas): ")
    # Ejecutar el segundo escaneo con nmap
    nmap_cmd = f"nmap -sCV -p {puertos} {ip_address} -oN {folder_name}/nmap/targeted"
    os.system(nmap_cmd)
    print("Escaneado completado")

# Pedir al usuario el nombre de la carpeta principal y la dirección IP
folder_name = input('Ingresa el nombre de la carpeta principal:')
ip_address = input('Ingresa la dirección IP a escanear:')

# Crear la carpeta principal
carpeta = Carpeta(folder_name)
folders = ['nmap', 'content', 'exploits', 'scripts']
for folder in folders:
    carpeta.crear_carpeta(folder)

# Determinar el sistema operativo de la máquina
sistema_operativo = determinar_sistema_operativo(ip_address)
print(f"El sistema operativo de la máquina {ip_address} es: {sistema_operativo}")

# Escanear los puertos
escanear_puertos(ip_address, folder_name)

