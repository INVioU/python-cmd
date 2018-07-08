#1
# Sets a default curve (secp256k1)
import random
from umbral import umbral, keys, config

config.set_default_curve()

#2
# Generate keys for Alice and Bob
alice_priv_key = keys.UmbralPrivateKey.from_bytes("effIKT60Ei8M9EtLGb36Gt6+ZjXn7uj8okftqEjlKCE=")
alice_pub_key = alice_priv_key.get_pubkey()

# print("Alice priv: ", alice_priv_key.to_bytes().hex())
# print("Alice pub: " , alice_pub_key.to_bytes().hex())

bob_priv_key = keys.UmbralPrivateKey.gen_key()
bob_pub_key = bob_priv_key.get_pubkey()

#3
# Encrypt some data for Alice
plaintext = b'good aaaaaaaapppppppppppppppppppppppppppppppppppppppaaaaaaaa and bad and stuff like this i dont know if we should or shouldnt'
alice_ciphertext, umbral_capsule = umbral.encrypt(alice_pub_key, plaintext)
new_plainText = b'shit'
alice_new_ciphertext, new_umbral_capsule = umbral.encrypt(alice_pub_key, plaintext)
print("Alice cyppher: ", alice_ciphertext)
print("Plain Text Hex Size: ", len(plaintext))
print("Cypher Text Size: ",len(alice_ciphertext.hex()))

#4
# Decrypt data for Alice
alice_decrypted_data = umbral.decrypt(umbral_capsule, alice_priv_key, alice_ciphertext, alice_pub_key)
print(alice_decrypted_data)

#5
# Bob receives a capsule through a side channel (s3, ipfs, Google cloud, etc)
bob_capsule = umbral_capsule

#6
# Attempt Bob's decryption (fail)
try:
    fail_decrypted_data = umbral.decrypt(bob_capsule, bob_priv_key, alice_ciphertext, alice_pubkey)
except:
    print("Decryption failed!")

#7
# Generate threshold split re-encryption keys via Shamir's Secret Sharing
# verification not ready yet, don't store vKeys
# Use Alice's private key, and Bob's public key.
# Use a minimum threshold of 10, and create 20 total shares
kfrags, _ = umbral.split_rekey(alice_priv_key, bob_pub_key, 10, 20)

#8
# Have Ursula perform re-encrypton.
# Pick 10 random shares:
rand_min_shares = random.sample(kfrags, 10)

# Have Ursula re-encrypt the shares and attach them to the capsule:
for kfrag in kfrags:
    cfrag = umbral.reencrypt(kfrag, umbral_capsule)
    bob_capsule.attach_cfrag(cfrag)

#9
# Bob reconstructs the capsule and decrypts the ciphertext:
bob_plaintext = umbral.decrypt(bob_capsule, bob_priv_key, alice_ciphertext, alice_pub_key)
print("this is bob: ", bob_plaintext)
new_bob_plaintext = umbral.decrypt(bob_capsule, bob_priv_key, alice_new_ciphertext, alice_pub_key) 
