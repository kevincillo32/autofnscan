import os

def create_folders(folder_name):
    """
    Crea las carpetas necesarias para guardar los resultados del escaneo
    """
    os.makedirs(folder_name+"/nmap/content/script/exploits", exist_ok=True)

def nmap_scan(folder_name,ip_address):
    """
    Realiza el escaneo con nmap y guarda los puertos escaneados en un archivo
    """
    os.system("nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn "+ip_address+" -oG "+folder_name+"/nmap")
    os.system("grep open "+folder_name+"/nmap/allPortsTCP | awk '{print $1}' > "+folder_name+"/nmap/ports")

def nmap_scan_targeted(folder_name,ip_address):
    """
    Realiza el escaneo detallado de los puertos escaneados y guarda el resultado en un archivo
    """
    with open(folder_name+"/nmap/ports") as f:
        ports = f.read().strip().replace("\n",",")
    os.system("nmap -sCV -p"+ports+" "+ip_address+" --oN "+folder_name+"/nmap/targeted")
    os.system("xclip -sel clip < "+folder_name+"/nmap/targeted")

def main():
    folder_name = input("Nombre del laboratorio: ")
    os.makedirs(folder_name)
    create_folders(folder_name)
    ip_address = input("Introduce la dirección IP a escanear: ")
    nmap_scan(folder_name,ip_address)
    nmap_scan_targeted(folder_name,ip_address)
