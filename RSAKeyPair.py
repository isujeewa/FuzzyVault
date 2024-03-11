from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

class ExtendedKeyPairGenerator:
    def __init__(self, key_size=2048):
        self.key_size = key_size
        self.private_key = None
        self.public_key = None

    def generate_key_pair(self):
        # Generate a private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.key_size,
        )

        # Get the public key
        public_key = private_key.public_key()

        # Save private and public keys
        self.private_key = private_key
        self.public_key = public_key

    def save_key_pair(self, private_key_path="private_key.pem", public_key_path="public_key.pem"):
        self.generate_key_pair()

        # Serialize the private key to PEM format
        private_pem = self.private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        # Serialize the public key to PEM format
        public_pem = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Save the private key to a file
        with open(private_key_path, "wb") as private_file:
            private_file.write(private_pem)

        # Save the public key to a file
        with open(public_key_path, "wb") as public_file:
            public_file.write(public_pem)

        print("Public and private keys generated and saved.")

    def encrypt_data(self, data, public_key):
        # Load the recipient's public key
        recipient_public_key = serialization.load_pem_public_key(
            public_key,
            backend=default_backend()
        )

        # Encrypt the data with the recipient's public key
        ciphertext = recipient_public_key.encrypt(
            data.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return ciphertext

    def decrypt_data(self, ciphertext):
        # Decrypt the ciphertext with the private key
        plaintext = self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return plaintext.decode()

if __name__ == "__main__":
    key_pair_generator = ExtendedKeyPairGenerator()
    key_pair_generator.save_key_pair()

    # Example usage:
    data_to_encrypt = "Sensitive information"

    # Encrypt the data using the public key
    encrypted_data = key_pair_generator.encrypt_data(data_to_encrypt, key_pair_generator.public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    print(f"Encrypted data: {encrypted_data}")

    # Decrypt the data using the private key
    decrypted_data = key_pair_generator.decrypt_data(encrypted_data)
    print(f"Decrypted data: {decrypted_data}")
