from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

AES_KEY = os.urandom(32)
AES_IV = os.urandom(16)

def encrypt_file(input_path, output_path):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)

    with open(input_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(output_path, 'wb') as f:
        f.write(AES_IV + ciphertext)


def decrypt_file(input_path, output_path):
    with open(input_path, 'rb') as f:
        data = f.read()

    iv = data[:16]
    ciphertext = data[16:]

    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(output_path, 'wb') as f:
        f.write(plaintext)


def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()

    with open("private.pem", "wb") as priv_file:
        priv_file.write(private_key)

    with open("public.pem", "wb") as pub_file:
        pub_file.write(public_key)

def rsa_encrypt(data, public_key_path="public.pem"):
    with open(public_key_path, "rb") as pub_file:
        public_key = RSA.import_key(pub_file.read())

    cipher = PKCS1_OAEP.new(public_key)
    return cipher.encrypt(data)

def rsa_decrypt(encrypted_data, private_key_path="private.pem"):
    with open(private_key_path, "rb") as priv_file:
        private_key = RSA.import_key(priv_file.read())

    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(encrypted_data)
