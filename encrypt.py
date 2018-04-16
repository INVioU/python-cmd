from umbral import umbral, keys, config

config.set_default_curve()

input_private_key = "effIKT60Ei8M9EtLGb36Gt6+ZjXn7uj8okftqEjlKCE="
input_plain_text = "hello"

private_key = keys.UmbralPrivateKey.from_bytes(input_private_key)

public_key = private_key.get_pubkey()

ciphertext, umbral_capsule = umbral.encrypt(public_key, input_plain_text.encode())

print("Chiper test: ", ciphertext.hex())