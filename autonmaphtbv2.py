import os
import re
from termcolor import colored

class Carpeta:
    def __init__(self, nombre):
        self.nombre = nombre
        os.mkdir(self.nombre)
    
    def crear_carpeta(self, nombre_carpeta):
        os.mkdir(self.nombre + '/' + nombre_carpeta)
        print(colored(f"Carpeta {nombre_carpeta} creada en {self.nombre}", "green"))
    
    def mostrar_info(self):
        print(colored(f"Información de la carpeta {self.nombre}:", "green"))
        
def validar_ip(ip_address):
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip_address):
        return True
    else:
        print(colored("Dirección IP no válida. Inténtelo de nuevo.", "red"))
        return False

def determinar_sistema_operativo(ip_address):
    ping = os.popen("ping -c 3 " + ip_address).read()
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
        print(colored(f"El sistema operativo de la máquina {ip_address} es: {sistema_operativo}", "green"))
    else:
        print(colored("No se pudo determinar el sistema operativo de la máquina", "red"))

def escanear_puertos(ip_address, folder_name):
    nmap_cmd = "nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn " + ip_address + " -oG " + folder_name + "/nmap/allPortsTCP"
    os.system(nmap_cmd)
    print(colored(f"El resultado del escaneo se ha guardado en {folder_name}/nmap/allPortsTCP", "green"))

folder_name = input(colored("Ingrese el nombre de la carpeta principal: ", "cyan"))
carpeta_principal = Carpeta(folder_name)

folders = ['nmap', 'content', 'exploits', 'scripts']
for folder in folders:
    carpeta_principal.crear_carpeta(folder)
carpeta_principal.mostrar_info()

while True:
    ip_address = input(colored("Ingrese la dirección IP: ", "cyan"))
    if validar_ip(ip_address):
        break
determinar_sistema_operativo(ip_address)
escanear_puertos(ip_address, folder_name)

