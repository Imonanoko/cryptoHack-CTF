from cryptography import x509
from cryptography.x509 import load_der_x509_certificate
with open('2048b-rsa-example-cert.der', 'rb') as f:
    cert = load_der_x509_certificate(f.read())
pub_numbers = cert.public_key().public_numbers()
print(f"n = {pub_numbers.n}")