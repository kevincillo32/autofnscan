import os
import re
from termcolor import colored

# clear the console
os.system('cls' if os.name == 'nt' else 'clear')

# Clase para crear y mostrar informacion de las carpetas
class Carpeta:
    def __init__(self, nombre):
        self.nombre = nombre
        os.mkdir(self.nombre)
    
    def crear_carpeta(self, nombre_carpeta):
        os.mkdir(self.nombre + '/' + nombre_carpeta)
        print(colored(f"Carpeta {nombre_carpeta} creada en {self.nombre}", "green"))
    
    def mostrar_info(self):
        print(colored(f"Información de la carpeta {self.nombre}:", "green"))
        
# Funcion para validar la direccion IP ingresada
def validar_ip(ip_address):
    if re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip_address):
        return True
    else:
        print(colored("Dirección IP no válida. Inténtelo de nuevo.", "red"))
        return False

# Funcion para determinar el sistema operativo de la maquina
def determinar_sistema_operativo(ip_address):
    ping = os.popen("ping -c 3 " + ip_address).read()
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
        print(colored(f"El sistema operativo de la máquina {ip_address} es: {sistema_operativo}", "green"))
    else:
        print(colored("No se pudo determinar el sistema operativo de la máquina", "red"))

# Funcion para escanear todos los puertos TCP
def escanear_puertos(ip_address, folder_name):
    nmap_cmd = "nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn " + ip_address + " -oG " + folder_name + "/nmap/allPortsTCP"
    os.system(nmap_cmd)
    print(colored(f"El resultado del escaneo se ha guardado en {folder_name}/nmap/allPortsTCP", "green"))

# Funcion para escanear solo los puertos abiertos
def escanear_puertos_abiertos(ip_address, folder_name):
    # Get user input for ports
    ports = input("Ingresa los puertos que deseas escanear (separados por comas): ")

    # Replace spaces with commas
    ports = ports.replace(" ", ",")

    # Scan the entered ports
    nmap_cmd = f"nmap -sCV -p {ports} {ip_address} -oN {folder_name}/nmap/targeted"
    os.system(nmap_cmd)
    print(colored(f"El resultado del escaneo se ha guardado en {folder_name}/nmap/targeted", "green"))

    # Read the targeted file and get the open ports
    with open(folder_name + '/nmap/targeted') as f:
        puertos_abiertos = [line.split()[0].split("/")[0] for line in f if "open" in line]
        puertos = ",".join(puertos_abiertos)

    # Copy the open ports to clipboard
    os.system(f'echo {puertos} | xclip -sel clip')
