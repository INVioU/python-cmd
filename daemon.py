from umbral import umbral, keys, config
from flask import Flask, request, jsonify
from flask_cors import CORS
# config.set_default_curve()
import base64

config.set_default_curve()

app = Flask(__name__)
CORS(app)

@app.route('/reencrypt', methods=['POST'])
def reencrypt():
    alice_priv = request.form['alice_priv']    
    alice_priv_key = keys.UmbralPrivateKey.from_bytes(alice_priv)
    alice_public_key = alice_priv_key.get_pubkey()

    bob_priv = request.form['bob_priv'] 
    bob_priv_key = keys.UmbralPrivateKey.from_bytes(bob_priv)
    bob_pub_key = bob_priv_key.get_pubkey()

    umbral_capsule = request.form['capsule'] 
    input_ciphertext = request.form['cipher']

    # convert capsule input from base64 string to bytes, then to Capsule
    umbral_capsule_decoded_bytes = base64.b64decode(umbral_capsule)
    input_umbral_capsule = umbral.Capsule.from_bytes(umbral_capsule_decoded_bytes)


    ciphertext = base64.b64decode(input_ciphertext)


    # Have Ursula re-encrypt the shares and attach them to the capsule:
    kfrags, _ = umbral.split_rekey(alice_priv_key, bob_pub_key, 10, 20)

    bob_capsule = input_umbral_capsule
    for kfrag in kfrags:
        cfrag = umbral.reencrypt(kfrag, input_umbral_capsule)
        bob_capsule.attach_cfrag(cfrag)
    
    decrypted_plaintext = umbral.decrypt(bob_capsule, bob_priv_key, ciphertext, alice_public_key )
    decrypted_plaintext_encoded = decrypted_plaintext.decode("utf-8")

    print('##########')
    print (decrypted_plaintext_encoded);
    print('##########')

    umbral_capsule_encoded = base64.b64encode(bob_capsule.to_bytes()).decode("utf-8")


    return jsonify({'capsule': umbral_capsule_encoded, 'cipher': input_ciphertext, 'enc_public_key':alice_public_key.to_bytes().decode("utf-8")})



@app.route('/genereateKeys', methods=['POST'])
def genereateKeys():
    priv_key = keys.UmbralPrivateKey.gen_key()
    public_key = priv_key.get_pubkey()
    return jsonify({'priv_key': priv_key.to_bytes().decode("utf-8"), 'public_key': public_key.to_bytes().decode("utf-8")})


@app.route('/encrypt', methods=['POST'])
def encrypt():
    input_plaintext = request.form['plaintext']     # any plain text
    input_private_key = request.form['priv']    # expected as base64 encoded string
    # input_private_key = "effIKT60Ei8M9EtLGb36Gt6+ZjXn7uj8okftqEjlKCE="

    private_key = keys.UmbralPrivateKey.from_bytes(input_private_key)
    public_key = private_key.get_pubkey()
    ciphertext, umbral_capsule = umbral.encrypt(public_key, input_plaintext.encode())

    ciphertext_encoded = base64.b64encode(ciphertext).decode("utf-8")
    umbral_capsule_encoded = base64.b64encode(umbral_capsule.to_bytes()).decode("utf-8")

    print('ciphertext_encoded:', ciphertext_encoded)
    print('umbral_capsule_encoded:', umbral_capsule_encoded)

    return jsonify({'ciphertext': ciphertext_encoded, 'capsule': umbral_capsule_encoded})


@app.route('/decrypt', methods=['POST'])
def decrypt():
    input_ciphertext = request.form['ciphertext']   # expected as base64 encoded string
    input_private_key = request.form['priv']    # expected as base64 encoded string
    input_umbral_capsule = request.form['capsule']  # expected as base64 encoded string
    # input_private_key = "effIKT60Ei8M9EtLGb36Gt6+ZjXn7uj8okftqEjlKCE="

    # convert capsule input from base64 string to bytes, then to Capsule
    umbral_capsule_decoded_bytes = base64.b64decode(input_umbral_capsule)
    input_umbral_capsule = umbral.Capsule.from_bytes(umbral_capsule_decoded_bytes)

    # convert from base64 string
    private_key = keys.UmbralPrivateKey.from_bytes(input_private_key)
    public_key = private_key.get_pubkey()

    # convert from base64 string
    ciphertext = base64.b64decode(input_ciphertext)

    decrypted_plaintext = umbral.decrypt(input_umbral_capsule, private_key, ciphertext, public_key)
    decrypted_plaintext_encoded = decrypted_plaintext.decode("utf-8")

    return jsonify({'decrypted_plaintext': decrypted_plaintext_encoded})
