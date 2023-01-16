import os
import re
from termcolor import colored
import subprocess

# clear the console

os.system('cls' if os.name == 'nt' else 'clear')

class Carpeta:
    def __init__(self, nombre):
        self.nombre = nombre
        os.mkdir(self.nombre)
    
    def crear_carpeta(self, list_nombre_carpeta):
        for nombre_carpeta in list_nombre_carpeta:
            if os.path.exists(self.nombre + '/' + nombre_carpeta):
                print(colored(f"La carpeta {nombre_carpeta} ya existe en {self.nombre}", "yellow"))
            else:
                os.mkdir(self.nombre + '/' + nombre_carpeta)
                print(colored(f"Se ha creado la subcarpeta {nombre_carpeta} en {self.nombre}", "green"))

    
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

def escanear_puertos(ip_address, folder_name):
    nmap_cmd = "nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn " + ip_address + " -oG " + folder_name + "/nmap/allPortsTCP"
    os.system(nmap_cmd)
    print(colored(f"El resultado del escaneo se ha guardado en {folder_name}/nmap/allPortsTCP", "green"))
    extractPorts(f"{folder_name}/nmap/allPortsTCP")

def extractPorts(file_path):
    with open(file_path, 'r') as f:
        ports = [re.findall(r'(\d+)\/open', line) for line in f if "open" in line]
    ports = [i[0] for i in ports if i]
    ports_str = ",".join(ports)
    process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
    process.communicate(input=ports_str.encode('utf-8'))
    print(f"Los puertos abiertos se han copiado al portapeles: {ports_str}")

# se llama a la funcion y se pasa el archivo allPortsTCP como argumento
extractPorts("nmap/allPortsTCP")

def escanear_puertos_personalizados(ip_address, folder_name):
    puertos = input("Introduzca los puertos a escanear separados por comas: ")
    nmap_cmd = f"nmap -sCV -p {puertos} {ip_address} -oN {folder_name}/nmap/targeted"
    os.system(nmap_cmd)
    print(colored(f"El resultado del escaneo se ha guardado en {folder_name}/nmap/targeted", "green"))

# Main
nombre_carpeta = input("Introduzca el nombre de la carpeta a crear: ")
carpeta = Carpeta(nombre_carpeta)
carpeta.crear_carpeta(['nmap','content', 'exploits', 'scripts'])
ip_address = input("Introduce la direccion IP a escanear: ")
if validar_ip(ip_address):
    determinar_sistema_operativo(ip_address)
    escanear_puertos(ip_address, nombre_carpeta)
    escanear_puertos_personalizados(ip_address, nombre_carpeta)


