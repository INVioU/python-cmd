from umbral import umbral, keys, config
from flask import Flask, request, jsonify
from flask_cors import CORS
# config.set_default_curve()
import base64


app = Flask(__name__)
CORS(app)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    input_ciphertext = request.form['ciphertext']
    input_private_key = request.form['priv']
    input_umbral_capsule = request.form['capsule']
    # input_private_key = "effIKT60Ei8M9EtLGb36Gt6+ZjXn7uj8okftqEjlKCE="

    priv_b = bytes.fromhex(input_private_key)
    private_key = base64.b64encode(priv_b)

    private_key = keys.UmbralPrivateKey.from_bytes(private_key)
    public_key = private_key.get_pubkey()
    decrypted_plain_text = umbral.decrypt(input_umbral_capsule, private_key, input_ciphertext, public_key)


    return jsonify({'decrypted_plain_text': decrypted_plain_text})
