import string
import hashlib
import random
import socket
import base64
import sys
import requests
from urllib3.exceptions import InsecureRequestWarning
import urllib3

urllib3.disable_warnings(category=InsecureRequestWarning)

# requests.packages.urllib3.disable_warnings(  # pylint: disable=no-member
#     category=InsecureRequestWarning
# )

ALPHABET = f"_-~.{string.ascii_letters}{string.digits}"
CODE_LENGTH = 128


def random_char(alphabet: str) -> str:
    return alphabet[random.randrange(0, len(alphabet))]


def random_code(alphabet: str, length: int) -> str:
    return "".join([random_char(alphabet) for _ in range(0, length)])


def code_challenge(code_verifier: str) -> str:
    sha256_hash = hashlib.sha256()
    sha256_hash.update(code_verifier.encode())
    digest = sha256_hash.digest()
    sha256_hash_as_base64 = (
        base64.urlsafe_b64encode(digest).rstrip(b"=").decode("us-ascii")
    )
    return sha256_hash_as_base64


def send_challenge(ip_address: str, code_verifier: str) -> str:
    auth_url = f"https://{ip_address}:8443/v1/oauth/authorize"
    params = {
        "audience": "homesmart.local",
        "response_type": "code",
        "code_challenge": code_challenge(code_verifier),
        "code_challenge_method": "S256",
    }
    response = requests.get(auth_url, params=params, verify=False, timeout=10)
    response.raise_for_status()
    return response.json()["code"]


def get_token(ip_address: str, code: str, code_verifier: str) -> str:
    data = str(
        "code="
        + code
        + "&name="
        + socket.gethostname()
        + "&grant_type="
        + "authorization_code"
        + "&code_verifier="
        + code_verifier
    )
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_url = f"https://{ip_address}:8443/v1/oauth/token"

    response = requests.post(
        token_url, headers=headers, data=data, verify=False, timeout=10
    )
    response.raise_for_status()
    return response.json()["access_token"]


def main() -> None:
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
    else:
        ip_address = input("Input the ip address of your Dirigera then hit ENTER ...\n")
    code_verifier = random_code(ALPHABET, CODE_LENGTH)
    code = send_challenge(ip_address, code_verifier)
    input("Press the action button on Dirigera then hit ENTER ...")
    token = get_token(ip_address, code, code_verifier)
    print("Your TOKEN :")
    print(token)
