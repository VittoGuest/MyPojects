from cryptography.fernet import Fernet
from time import sleep

def generate_key(key_name):
    key = Fernet.generate_key()

    # string the key in a file
    with open(key_name, 'wb') as filekey:
        filekey.write(key)

    return '[+] Key generated successfully! '


def encrypt(filename, key):

    # opening the key
    with open(key, 'rb') as filekey:
        key = filekey.read()

    # using the generated key
    fernet = Fernet(key)

    # opening the original file to encrypt
    with open(filename, 'rb') as file:
        original = file.read()
        
    # encrypting the file
    encrypted = fernet.encrypt(original)

    # opening the file in write mode and 
    # writing the encrypted data
    with open(filename, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
    
    return '[+] File encrypted successfully!'


def decrypt(filename, key):
    # using the key
    with open(key, 'rb') as k:
        
        key_value=k.read()
        fernet = Fernet(key_value)

    # opening the encrypted file
    with open(filename, 'rb') as enc_file:
        encrypted = enc_file.read()

    # decrypting the file
    decrypted = fernet.decrypt(encrypted)

    # opening the file in write mode and
    # writing the decrypted data
    with open(filename, 'wb') as dec_file:
        dec_file.write(decrypted)
    
    return '[+] File dencrypted successfully!'


def main():
    choice = input('[*] Select choice:\n1) Generate new Key\n2) Encrypt a file\n3) Decrypt file\n\n>>> ')
    #try:
    if int(choice) == 1:
            keyname = input('[*] Save key file as :\n>>> ')
            generate_key(keyname)
            main() 
    if int(choice)==2:
            key = input('[*] Put key path:\n>>>')
            filepath = input('[*] Put the path of the file to be encrypted:\n>>> ')
            encrypt(filepath, key)
            sleep(2) 
            exit()
    if int(choice)==3:
            key = input('[*] Put key path:\n>>>')
            filepath = input('[*] Put the path of the file to be dencrypted:\n>>> ')
            decrypt(filepath, key)
            sleep(2) 
            exit()
    #except Exception as e:
        #print(e)

main()
