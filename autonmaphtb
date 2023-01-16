import os

folder_name = input("Nombre del laboratorio: ")
os.makedirs(folder_name+"/nmap/content/script/exploits", exist_ok=True)
ip_address = input("Introduce la dirección IP a escanear: ")
os.system("nmap -p- --open -sS --min-rate 5000 -vvv -n -Pn "+ip_address+" -oG "+folder_name+"/nmap")
ports = os.popen("grep open "+folder_name+"/nmap/allPortsTCP | awk '{print $1}'").read().strip().replace("\n",",")
os.system("nmap -sCV -p"+ports+" "+ip_address+" --oN "+folder_name+"/nmap/targeted")
