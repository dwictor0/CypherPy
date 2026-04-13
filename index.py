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