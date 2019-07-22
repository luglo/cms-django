import hashlib

import requests


def derive_id_from_public_key(public_key: str) -> str:
    return hashlib.sha256(string_to_bytes(public_key)).hexdigest()


def send_federated_cloud_request(domain: str, tail: str) -> str:
    return requests.get("http://" + domain + "/federated-cloud/" + tail).text


def sign_message(message: str, private_key: str) -> str:
    pass


def check_signature(message: str, signature: str, public_key: str) -> bool:
    pass


def bytes_to_string(b: bytes) -> str:
    return b.hex()


def string_to_bytes(s: str) -> bytes:
    return bytes.fromhex(s)
