#--PHYTON-FLASK CODE FOR 'NOTIFS' BY: RYRUBIO--#
#===============================================================================================================================>
from cryptography.fernet import Fernet

def generate_and_save_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)
    print(f"Generated Key: {key.decode()} (saved in 'secret.key')")

if __name__ == "__main__":
    generate_and_save_key()
    
#===============================================================================================================================>