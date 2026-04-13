import pathlib,os,secrets,base64,getpass
import cryptography
from cryptography . fernet import Fernet
from cryptography . hazmat . primitives .kdf . scrypt import Scrypt

def make_salt(size=16):
    """_summary_
    Args:
        size (int, optional): _description_. Defaults to 16.
    """
    return secrets.token_bytes(size)
def derive_key(salt,password):
    """_summary_
    Args:
        salt (_type_): _description_
        password (_type_): _description_
    """
    kdf = Scrypt(salt=salt,length=32,n = 2 ** 14,r = 8,p=1)
    return kdf.derive(password.encode())
def load_salt():
    """_summary_
    Returns:
        _type_: _description_
    """
    return open("salt.salt","rb").read()
def generate_key(password,salt_size=16,load_existing_salt=False,save_salt=True):
    """_summary_
    Args:
        password (_type_): _description_
        salt_size (int, optional): _description_. Defaults to 16.
        load_existing_salt (bool, optional): _description_. Defaults to False.
        save_salt (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    if load_existing_salt:
        salt = load_salt()
    elif save_salt:
        salt = make_salt(salt_size)
        with open("salt.salt","wb") as salt_file:
            salt_file.write(salt)
            derived_key = derive_key(salt,password)
    return base64.urlsafe_b64encode(derived_key)
