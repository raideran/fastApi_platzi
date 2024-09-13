from jwt import encode, decode

secret = "my_secret_key"

def create_token(data: dict):
    token = encode(payload=data, key=secret, algorithm="HS256")
    return token


def validate_token(token:str) -> dict:
    data = decode(token, key=secret, algorithms=["HS256"])
    return data