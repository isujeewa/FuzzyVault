from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_keys():
    """ Generate RSA private and public keys """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_private_key(private_key):
    """ Serialize the private key to PEM format """
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    return private_pem

def serialize_public_key(public_key):
    """ Serialize the public key to PEM format """
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return public_pem

def deserialize_public_key(public_pem):
    """ Deserialize a public key from PEM format """
    public_key = serialization.load_pem_public_key(
        public_pem,
        backend=default_backend()
    )
    return public_key

def encrypt_message(public_key, message):
    """ Encrypt a message using the public key """
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def decrypt_message(private_pem, ciphertext):
    """ Decrypt a message using a serialized private key """
    private_key = serialization.load_pem_private_key(
        private_pem,
        password=None,
        backend=default_backend()
    )
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

# Example usage
private_key, public_key = generate_keys()
private_pem = serialize_private_key(private_key)
public_pem = serialize_public_key(public_key)
message = "Hello, secure world!"
print("private_pem:", private_pem)
print("public_pem:", public_pem)


# Encrypt the message using the serialized and then deserialized public key
deserialized_public_key = deserialize_public_key(public_pem)
encrypted_message = encrypt_message(deserialized_public_key, message)
print("encrypted_message:",  encrypted_message)
# Decrypt the message using the serialized private key
decrypted_message = decrypt_message(private_pem, encrypted_message)
print("Decrypted message:", decrypted_message)

kye= b'\x88\xc5\x94\x93\xc1\xd3e\x1f-\xe2\x80\xc2\xe82\xa2\xc9C\x98\xd49\xbbc\xe4**\x9a\xeeT\xb3\x1f\xea`5\xff\\@z\xa2\x8ec\xae\xdc~qY\x8b\x1eQ?\x85\xda\xf2\x02\xa7W\x87\xd2\xb2\xc1\xbd-\x82\x9a\x10\x01\xa2\x1e\xe9Lu\xdb\xc8+\xba"d\xbb\xaec\x95Q\x84O\x1d\t\xa4\xecK\xb0\xd3\xc7`/\x04G\xc13\xb5\xf5X\xa0\x05\xf6\xb9\x13M\xbf\xd2\x0e>gd[\xd8\x18v\xe4$\xb4=\xf9Ql\xa4`\xa6/u\x85\x9fV@M\xf2\x98\x97\x08\x8b\xe2:\xe9+\x84\xe1\x14\x0c\xa1\xb0R_\xec5k\x18\xc7)\x8a"\xa8J\r\xd6\x10\xe3\xbb\x008\x10\x97\x12\x018X\x1ao\x83\xd1vq\xbe\xaa\x13\xe2\xa0\x16H\x91\x8f\xb7\xee\x87\xd0\xdbQ\xf2w\x9d\xae\x1c,3\x1a\xb4\xcf\xe6hUO\x9c\r\xbe\x9dw\xd4\x15R\x9c\'\xf7I\x86\r\xb9\x02;\xfe\xd1\x91\x85t\x06a\x1b\xaa\x196<\xc5d\x9e\xc6\xedbFp0>M\xa8r! \x06\x90\x88\xee'
pk= b'-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxzoXTl0iufBVH\n0rsHfWvJwAkdNEFQiiawjsUA+FgQuK6UhyUwaJG4uyyIb0LfbEiRVUPhqm9COKp6\n0GN4V2fCFYja6bNIUzVLngyOdYoCS3hbRcHaJ6zn0ZFDKt+4EVpmm5rodODvf2bA\n6MLwjY5kVZ8UxMi6g7tBhHnVhWDFZRAyLQUEqRujasrSUZU09LfGKCmckmbj+dXc\nM6aAtEWLKP7xpxlVagX/upTyb5JStP/nulUWtbsxHlbjB3HjyUmggYK0BaVol4/Z\nw4xt2xY/lTbjpOQtyYCureSVKlzycT45McrpSQ+HCLsYds+2msQZKFErVaU3niAz\nK3y8Z/ItAgMBAAECggEAC+BhFQCKZMk5/KmpP3dTr06p7S7z2+bWbb2jkAyGiVtk\nodwjEkgxz5aFA3n3DAhmEnsRBS5GrzQswvZPZpbkAdVBZmnsxTx1l17vtMZKGRwk\nZmhS6fjzdiqL2uIuvlM+aBMltjg0XBr06JbDiqDR7YbAkPkR9U9ePyKTprz5eUXJ\nl4+X0SRzNcwYGP9WwQX6oQrNgWCHzCy2Acpt0cV/QtIzqUcrunEXg2eJ03cN8VW/\nMVPVRM4zF3VWeF3f647xPP4lTD449hQBTVNFcIDeuw40fln4uRXrg9B9RVA+fcov\nzMhyqw+/1XdaZ2jlkOn1Ka9MAVRlyPppJUTG/sG3sQKBgQD1Ltm1Ep5WZo6R06RE\nLkMM15vkRZs7x8OZS1tqC/ZE9KRnLmu66HyF+oiLhfvljOTfCt4i+OpuEJ2K7LLW\nWi1vU5wHZwaEqqzQDb8Hg5BpsAlGZGZCMdu0G67w4MxbTitM8FHSNYryCBmHN9Nx\nNS7PX8AHLsUv1i4/bU9Ha7l9SQKBgQC5prXNHClzyeX3QcmbRpIbvXyJZqLjIzMn\n3QyKdTEIQnQwof7PwT0JZF67YXblkGiskbXxkxvOY8KfAfot60em9T2Jbi7sjzFX\ntf7NROs/s/Rpowl4Iz+5lV032KdaU3E2jplM2wRx0AlSaxpwCBoMi//UwRhNiH2k\nnWVcFgNBxQKBgQCs5Jq0qypodu12O64MPisd9TSC5eqvXxC5GoCd6U2CFpmQARYK\nuUKGH8MF0DdvCcmi1sEKHEkD0Een3X3G1dRQOr8+IRJhnxE5rVfV7pp5TJ9duhK5\n/vqUqSjVx0+T2y2Blb284/DU94044s8Bd6VIqpZ4+iwmrXvzUhujm30zsQKBgQCB\n02kzRExgooHkxOa9ZT5rk7jxRQsHl+gAKn7InGdrhT1HfSF6G4IZfU0Z8HB63N+2\nPjdj9iHt1KmXFITlc7EpujoMTzcVSpWQ5r6GwXlZlPiInvDSSKQZnbAQi7uMWOnE\n4zelHUwgYwEB19AnJCNDPuvq1hWuspJaeY8WNHaWmQKBgHWwkbMhHoAOYc1dP0QG\nZtEj61vTf33RBJhjf2mQqudJaXqt6Lxei2navU6ajr814snACoJ+VYCZvdwejUG3\nF/uW1LEjD1bCEjLpHciVXHLaSSKGcHn2AEshHUhYE8Bkiyy86JOPuf+9qrBf3sHW\nKgE6JWbW07Vrq0vFHXKMhHSx\n-----END PRIVATE KEY-----\n'

decrypted_message = decrypt_message(pk, kye)
print("Decrypted message:", decrypted_message)
