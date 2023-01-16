import os

def create_main_folder():
    folder_name = input("Nombre del laboratorio: ")
    os.makedirs(folder_name, exist_ok=True)
    return folder_name

def create_subfolders(folder_name):
    os.makedirs(folder_name+"/nmap/content/script/exploits", exist_ok=True)

def get_ip():
    ip_address = input("Introduce la dirección IP a escanear: ")
    return ip_address

def nmap_scan_1(folder_name,ip_address):
    os.system("nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn "+ip_address+" -oG "+folder_name+"/nmap")

def get_open_ports(folder_name):
    return os.popen("grep open "+folder_name+"/nmap/allPortsTCP | awk '{print $1}'").read().strip().replace("\n",",")

def nmap_scan_2(folder_name,ip_address,ports):
    os.system("nmap -sCV -p"+ports+" "+ip_address+" --oN "+folder_name+"/nmap/targeted")

def main():
    folder_name = create_main_folder()
    create_subfolders(folder_name)
    ip_address = get_ip()
    nmap_scan_1(folder_name,ip_address)
    ports = get_open_ports(folder_name)
    nmap_scan_2(folder_name,ip_address,ports)

