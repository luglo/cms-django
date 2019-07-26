import requests
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode


def send_federated_cloud_request(domain: str, tail: str, params=None) -> str:
    return requests.get("http://" + domain + "/federated-cloud/" + tail, params).text


def gen_key_pair_strings():
    key_pair = RSA.generate(2048, Random.new().read)
    priv_key_string = key_pair.exportKey('PEM').decode()
    pub_key_string = key_pair.publickey().exportKey('PEM').decode()
    return priv_key_string, pub_key_string


def derive_id_from_public_key(public_key_string: str) -> str:
    digest = SHA256.new()
    digest.update(public_key_string.encode())
    return digest.hexdigest()[:20]


def sign_message(message: str, private_key_string: str) -> str:
    private_key = RSA.import_key(private_key_string)
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(message.encode())
    signature_bytes = signer.sign(digest)
    return b64encode(signature_bytes).decode()


def verify_signature(message: str, signature: str, public_key_string: str) -> bool:
    signature_bytes = b64decode(signature.encode())
    public_key = RSA.importKey(public_key_string.encode())
    signer = PKCS1_v1_5.new(public_key)
    digest = SHA256.new()
    digest.update(message.encode())
    return signer.verify(digest, signature_bytes)


def bytes_to_string(b: bytes) -> str:
    return b.hex()


def string_to_bytes(s: str) -> bytes:
    return bytes.fromhex(s)
