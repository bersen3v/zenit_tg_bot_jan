import uuid


def generate_unique_key():
    while True:
        key = str(uuid.uuid4().int)[:8]
        yield key


key_generator = generate_unique_key()
