import hashlib

import requests


def derive_id_from_public_key(public_key: bytes) -> str:
    return bytes_to_string(hashlib.sha256(public_key))


def send_federated_cloud_request(domain: str, tail: str) -> str:
    return requests.get("http://" + domain + "/federated-cloud/" + tail).text


def sign_message(message: str, private_sign_key: bytes) -> str:
    pass


def check_signature(message: str, signature: str, public_sign_key: bytes) -> bool:
    pass


def bytes_to_string(b: bytes) -> str:
    return b.hex()


def string_to_bytes(s: str) -> bytes:
    return bytes.fromhex(s)
