from umbral import umbral, keys, config
from flask import Flask, request, jsonify
from flask_cors import CORS
# config.set_default_curve()
import base64


app = Flask(__name__)
CORS(app)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    input_plain_text = request.form['plaintext']
    input_private_key = request.form['priv']
    # input_private_key = "effIKT60Ei8M9EtLGb36Gt6+ZjXn7uj8okftqEjlKCE="

    priv_b = bytes.fromhex(input_private_key)
    private_key = base64.b64encode(priv_b)

    private_key = keys.UmbralPrivateKey.from_bytes(private_key)
    public_key = private_key.get_pubkey()
    ciphertext, umbral_capsule = umbral.encrypt(public_key, input_plain_text.encode())

    return jsonify({'ciphertext': ciphertext.hex(), 'capsule': umbral_capsule.hex()})