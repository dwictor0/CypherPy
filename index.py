import pathlib
import os
import secrets
import base64
import getpass
import cryptography

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

SALT_FILE = "salt.salt"

def make_salt(size=16):
    """_summary_
    Args:
        size (int, optional): _description_. Defaults to 16.

    Returns:
        _type_: _description_
    """
    return secrets.token_bytes(size)
def derive_key(salt, password):
    """_summary_
    Args:
        salt (_type_): _description_
        password (_type_): _description_

    Returns:
        _type_: _description_
    """
    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    return kdf.derive(password.encode())
def save_salt(salt):
    """_summary_
    Args:
        salt (_type_): _description_
    """
    with open(SALT_FILE, "wb") as f:
        f.write(salt)
def load_salt():
    """_summary_
    Raises:
        FileNotFoundError: _description_

    Returns:
        _type_: _description_
    """
    if not os.path.exists(SALT_FILE):
        raise FileNotFoundError("Salt não encontrado. Use -s na primeira criptografia.")
    with open(SALT_FILE, "rb") as f:
        return f.read()
def generate_key(password, salt_size=16, new_salt=False):
    """_summary_
    Args:
        password (_type_): _description_
        salt_size (int, optional): _description_. Defaults to 16.
        new_salt (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    if new_salt:
        salt = make_salt(salt_size)
        save_salt(salt)
    else:
        salt = load_salt()
    derived_key = derive_key(salt, password)
    return base64.urlsafe_b64encode(derived_key)
def encrypt(filename, key):
    """_summary_
    Args:
        filename (_type_): _description_
        key (_type_): _description_
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = f.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
def decrypt(filename, key):
    """_summary_
    Args:
        filename (_type_): _description_
        key (_type_): _description_
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    try:
        decrypted_data = f.decrypt(encrypted_data)
    except cryptography.fernet.InvalidToken:
        print(f"[ERRO] Falha ao descriptografar: {filename}")
        print("Motivo: senha incorreta ou salt diferente.")
        return

    with open(filename, "wb") as file:
        file.write(decrypted_data)
def encrypt_folder(foldername, key):
    """_summary_
    Args:
        foldername (_type_): _description_
        key (_type_): _description_
    """
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[++] Criptografando: {child}")
            encrypt(child, key)
        elif child.is_dir():
            encrypt_folder(child, key)
def decrypt_folder(foldername, key):
    """_summary_
    Args:
        foldername (_type_): _description_
        key (_type_): _description_
    """
    for child in pathlib.Path(foldername).glob("*"):
        if child.is_file():
            print(f"[++] Descriptografando: {child}")
            decrypt(child, key)
        elif child.is_dir():
            decrypt_folder(child, key)
if __name__ == "__main__":
    """_summary_
    Raises:
        TypeError: _description_
        TypeError: _description_
        FileNotFoundError: _description_
    """
    import argparse
    parser = argparse.ArgumentParser(
        description="Criptografia de arquivos e diretórios com senha"
    )
    parser.add_argument("path", help="Arquivo ou diretório alvo")
    parser.add_argument("-e", "--encrypt", action="store_true", help="Criptografar")
    parser.add_argument("-d", "--decrypt", action="store_true", help="Descriptografar")
    parser.add_argument(
        "-s",
        "--salt-size",
        type=int,
        help="Gera novo salt (use apenas na primeira criptografia)",
    )
    args = parser.parse_args()
    if not args.encrypt and not args.decrypt:
        raise TypeError("Use -e (criptografar) ou -d (descriptografar)")
    if args.encrypt and args.decrypt:
        raise TypeError("Use apenas uma opção: -e ou -d")
    password = getpass.getpass("Senha: ")
    new_salt = True if args.salt_size else False
    key = generate_key(
        password,
        salt_size=args.salt_size if args.salt_size else 16,
        new_salt=new_salt,
    )
    if os.path.isfile(args.path):
        if args.encrypt:
            encrypt(args.path, key)
        else:
            decrypt(args.path, key)
    elif os.path.isdir(args.path):
        if args.encrypt:
            encrypt_folder(args.path, key)
        else:
            decrypt_folder(args.path, key)
    else:
        raise FileNotFoundError("Arquivo ou diretório não encontrado")