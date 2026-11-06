import os
import sys
from cryptography.fernet import Fernet

target_dir = "/home/wilf/datos_criticos"
key_path = os.path.join(target_dir, "clave.key")

if not os.path.exists(key_path):
    print("[-] Error: No se encontro el archivo 'clave.key'. Imposible descifrar.")
    sys.exit(1)

with open(key_path, "rb") as key_file:
    key = key_file.read()

cipher = Fernet(key)
print("[*] Clave cargada. Restaurando archivos...")

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith('.locked'):
            file_path = os.path.join(root, file)
            original_file_path = file_path.replace('.locked', '')
            try:
                with open(file_path, 'rb') as f:
                    datos_cifrados = f.read()
                datos_originales = cipher.decrypt(datos_cifrados)
                with open(original_file_path, 'wb') as f:
                    f.write(datos_originales)
                os.remove(file_path)
                print(f"[+] Recuperado: {file} -> {os.path.basename(original_file_path)}")
            except Exception as e:
                print(f"[-] Error al descifrar {file}: {e}")

nota_path = os.path.join(target_dir, "RESCATE.txt")
if os.path.exists(nota_path):
    os.remove(nota_path)
if os.path.exists(key_path):
    os.remove(key_path)
print("[+] Sistema restaurado con exito.")
