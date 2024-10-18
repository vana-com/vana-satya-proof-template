import base64
import json
from collections import OrderedDict
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Helper function to convert hex string to bytes
def hextoBytes(hex_string):
    return bytes.fromhex(hex_string)

# Helper function to convert bytes to hex string
def bytesToHex(byte_data):
    return byte_data.hex()

# AES-GCM decryption (used for the second layer)
def decryptAESGCM(encrypted_data, symmetric_key, iv):
    aesgcm = AESGCM(symmetric_key)
    decrypted_data = aesgcm.decrypt(iv, encrypted_data, None)
    return decrypted_data

# Main decryption function
def decryptData(encrypted_data, iv, signed_message):
    # Parse the encrypted data from the JSON format
    print("inside decryptingData fct...")
    # Decode the base64-encoded IV and encrypted data
    encrypted_data_bytes = base64.b64decode(encrypted_data)
    iv_bytes = base64.b64decode(iv)
    encryption_key_bytes = hashlib.sha256(bytes.fromhex(signed_message)).digest()
    

    # Decrypt the second layer data using AES-GCM
    decrypted_second_layer = decryptAESGCM(encrypted_data_bytes, encryption_key_bytes, iv_bytes)

    # Decode the decrypted data from bytes to a string
    decrypted_data_str = decrypted_second_layer.decode('utf-8')
    # Parse the decrypted data string into a Python dictionary
    decrypted_data = json.loads(decrypted_data_str)
    
    return decrypted_data


def serializeData(decrypted_data):
    # Ensure the data is an OrderedDict to preserve key order
    if not isinstance(decrypted_data, OrderedDict):
        decrypted_data = json.loads(json.dumps(decrypted_data), object_pairs_hook=OrderedDict)
    
    # Serialize to JSON string
    json_string = json.dumps(
        decrypted_data,
        separators=(',', ':'),
        ensure_ascii=False
    )
    return json_string

def encodeToBytes(json_string):
    json_bytes = json_string.encode('utf-8')
    return json_bytes

def computeSha256Hash(json_bytes):
    hash_digest = hashlib.sha256(json_bytes).hexdigest()
    return hash_digest

def verifyDataHash(decrypted_data, data_hash):
    browsing_data_array = decrypted_data.get('browsingDataArray', [])
    json_string = serializeData(browsing_data_array)
    json_bytes = encodeToBytes(json_string)
    computed_hash = computeSha256Hash(json_bytes)
    
    is_match = computed_hash == data_hash
    if is_match:
        print("Data hash matches.")
    else:
        print("Data hash does not match.")
        print(f"Computed hash: {computed_hash}")
        print(f"Provided hash: {data_hash}")
    return is_match