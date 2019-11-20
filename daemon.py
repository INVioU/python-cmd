from umbral import umbral, keys, config
from flask import Flask, request, jsonify
from flask_cors import CORS
# config.set_default_curve()
import base64

config.set_default_curve()

app = Flask(__name__)
CORS(app)


		

# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>')
# def catch_all(path):
#     return 'You want path: %s' % path

@app.route('/encryption/')
def hello():
    name = request.args.get("name", "World")
    return 'Hello, {(name)}!'

#Alice
#priv_key": "F-iDA737-dNugH7hd7cVdenvkOrBZve1Q_vMt_Wk_YA=",
#"public_key": "AsrWcmmy3QzTG6DDEs3fdFl9FexWkpOaMTTIT3vziaD3"

#   "capsule": "AyORjN2L9B2FvpUWm+tqnj0cqXu886e6Xsy2EC3WnM99As6P14OTkd76qNhb1/YtHFjlMKGpwYryntCoSzbrZZTiMGQQH8qUqiyc7areFl7wmJrrgCMqSVHtvWDrOrD38c4=",
#     "ciphertext": "FcK+9/l667v/TIIf9n20vIIFgEFGT5HNlJvoLHQc3BugMA7Bvdh0e+WaTOcaw2RO"



#Bob
#  "priv_key": "WOc52rTKVRCpil74plqHBPkgGSJJrfFZs9Lb_HQkdpQ=",
#  "public_key": "AsMjOXvGJJhEQEStOZ5qcCTvgT1uRI7BEnbLFelio3wf"

# Bob's reencrypt

#    "capsule": "AzqOe7wJCSEgFJXs6R/MmedPyTx/PaX64aQgcrUrC5I5AzBudntQdWGJlwPNCOwSVW3tmcjspI79EM/mlvuJ2Tyquv/5aSgVww60obO30Cfs7F7lXA0b4CxEU896vvMa3SsDIScfqytHGk9Ldy4kc7Egkc+6B7XltEqCJVVTJCLuj+0DrHyK0jXxRPjc80UpMTREMK6iOSpWpaFRtXKg3xcdeeMCF3A5l0wkS7Miz7FABleLy3hkekLqANorzGLzrBzkEkQ=",
#    "cipher": "ycU9eZywrIRskZB7ZJR5AAa7+KDXixTjVskQLk5C6TDo",
#    "public_key": "AsrWcmmy3QzTG6DDEs3fdFl9FexWkpOaMTTIT3vziaD3"

@app.route('/encryption/generateKeys', methods=['POST'])
def genereateKeys():

    input_privateKeys = request.json.get('priv')
    if  not input_privateKeys:
        priv_key = keys.UmbralPrivateKey.gen_key()
        pub_key = priv_key.get_pubkey()
    else:
        priv_key = keys.UmbralPrivateKey.from_bytes(input_privateKeys)
        pub_key = priv_key.get_pubkey()

    return jsonify({'private_key': priv_key.to_bytes().decode("utf-8"), 'public_key': pub_key.to_bytes().decode("utf-8")})


@app.route('/encryption/encrypt', methods=['POST'])
def encrypt():

    print('entered');
    
    input_client_public_key = request.json.get('pub_client')
    input_inviou_public_key = request.json.get('pub_inviou')

    intputArray = request.json.get('input')

    
    if  not intputArray:
        return jsonify({'Error': 'Missing required input data to encrypt input = [{id:1,plaintext:123},{id:2,plaintext:222}....]' })

    if  not input_client_public_key:
        return jsonify({'Error': 'Missing required public key'})

    if input_inviou_public_key:
        inviou_public_key = keys.UmbralPublicKey.from_bytes(input_inviou_public_key)

    client_public_key = keys.UmbralPublicKey.from_bytes(input_client_public_key)

    results_inviou = []
    results_client = []
    for item in intputArray:
        input_plaintext = item.get('plaintext');
        # public_key = private_key.get_pubkey()
        ciphertext, umbral_capsule = umbral.encrypt(client_public_key, input_plaintext.encode())

        ciphertext_encoded = base64.b64encode(ciphertext).decode("utf-8")
        umbral_capsule_encoded = base64.b64encode(umbral_capsule.to_bytes()).decode("utf-8")
        results_client.append({'id':item.get('id'),'ciphertext': ciphertext_encoded, 'capsule': umbral_capsule_encoded})

        if input_inviou_public_key: 
            ciphertext_inviou, umbral_capsule_inviou = umbral.encrypt(inviou_public_key, input_plaintext.encode())

            ciphertext_encoded_inviou = base64.b64encode(ciphertext_inviou).decode("utf-8")
            umbral_capsule_encoded_inviou = base64.b64encode(umbral_capsule_inviou.to_bytes()).decode("utf-8")
            results_inviou.append({'id':item.get('id'),'ciphertext': ciphertext_encoded_inviou, 'capsule': umbral_capsule_encoded_inviou})

    # print('ciphertext_encoded:', ciphertext_encoded)
    # print('umbral_capsule_encoded:', umbral_capsule_encoded)

    # return jsonify({'ciphertext': ciphertext_encoded, 'capsule': umbral_capsule_encoded})
    results = []
    results.append({'encrypted':results_client});
    if input_inviou_public_key:
        results.append({'encrypted_inviou':results_inviou});

    return jsonify(results);


@app.route('/encryption/decrypt', methods=['POST'])
def decrypt():

    input_ciphertext = request.json.get('ciphertext')
    input_private_key = request.json.get('priv')
    input_umbral_capsule = request.json.get('capsule')

    if  not input_ciphertext:
        return jsonify({'Error': 'Missing required ciphertext'})

    if  not input_private_key:
        return jsonify({'Error': 'Missing required private key'})
    
    if  not input_umbral_capsule:
        return jsonify({'Error': 'Missing required capsule'})

    # convert capsule input from base64 string to bytes, then to Capsule
    umbral_capsule_decoded_bytes = base64.b64decode(input_umbral_capsule)
    input_umbral_capsule = umbral.Capsule.from_bytes(umbral_capsule_decoded_bytes)

    # convert from base64 string
    private_key = keys.UmbralPrivateKey.from_bytes(input_private_key)
    public_key = private_key.get_pubkey()

    # convert from base64 string
    ciphertext = base64.b64decode(input_ciphertext)

    pub_key = request.json.get('pub')
    if pub_key:
        print('Decrypt reencrypted')
        alice_public_key = keys.UmbralPublicKey.from_bytes(pub_key)    
        decrypted_plaintext = umbral.decrypt(input_umbral_capsule, private_key, ciphertext, alice_public_key)
    else:        
        print('Decrypt encrypted')
        decrypted_plaintext = umbral.decrypt(input_umbral_capsule, private_key, ciphertext, public_key)

    decrypted_plaintext_encoded = decrypted_plaintext.decode("utf-8")

    return jsonify({'decrypted_plaintext': decrypted_plaintext_encoded})

@app.route('/encryption/reencrypt', methods=['POST'])
def reencrypt():
    
    alice_priv = request.json.get('priv')
    pub_key = request.json.get('pub')
    umbral_capsule = request.json.get('capsule')
    input_ciphertext = request.json.get('ciphertext')

    if  not alice_priv:
        return jsonify({'Error': 'Missing required Alice\' Private key - Data owner'})

    if  not pub_key:
        return jsonify({'Error': 'Missing required Bob\'s Public key - Data receiver'})
    
    if  not umbral_capsule:
        return jsonify({'Error': 'Missing required capsule'})

    if  not input_ciphertext:
        return jsonify({'Error': 'Missing required cipher text'})

    alice_priv_key = keys.UmbralPrivateKey.from_bytes(alice_priv)
    alice_public_key = alice_priv_key.get_pubkey()
    bob_pub_key = keys.UmbralPublicKey.from_bytes(pub_key)
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

    # umbral_capsule_encoded = base64.b64encode(bob_capsule.to_bytes()).decode("utf-8")
    
    print('##########')
    print (umbral_capsule_encoded);
    print('##########')
    
    bob_priv = request.json.get('bob_priv')
    bob_priv_key = keys.UmbralPrivateKey.from_bytes(bob_priv)


    decrypted_plaintext = umbral.decrypt(bob_capsule, bob_priv_key, ciphertext, alice_public_key)
    # decrypted_plaintext_encoded = decrypted_plaintext.decode("utf-8")

    print('##########')
    # print (decrypted_plaintext_encoded);
    print('##########')
# 
    umbral_capsule_encoded = bob_capsule.to_bytes().decode("utf-8")

    return jsonify({'capsule': umbral_capsule_encoded, 'cipher': input_ciphertext, 'public_key':alice_public_key.to_bytes().decode("utf-8")})




@app.errorhandler(400)
def bad_request(error=None):
    message = {
        'status': 400,
        'message': 'bad request: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    # app.run(host='0.0.0.0')
    app.run()