import base64
import json
from Cryptodome.Cipher import ARC4


def stj_decrypt(filepath, key):
    with open(filepath, "r", encoding="utf-8") as f:
        jaon_data = json.load(f)
    data = base64.b64decode(jaon_data["data"]['data'])
    json_bytes = ARC4.new(key.encode()).decrypt(data)
    return json_bytes


escaped_text = stj_decrypt(filepath='long_json.json',
                           key='a52ef1332c4770ef87493628c3b0ac3a6a56e42b6de5d366b68d198b4686557c7431ee57865691e0b1d299ef30d8e68b31cd22941af1d9898bc5ba70303e7d27')

print(escaped_text.decode('utf-8'))
