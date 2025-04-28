import time

import requests

cookies = {
    'cuid': 'B456A352201353A80CB4B82EA49BA5A3%7C0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 2201123C Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/101.0.4951.61 Mobile Safari/537.36',
    # 'Accept-Encoding': 'identity',
    'x-wap-proxy-cookie': 'none',
    'if-modified-since': 'Mon, 17 Mar 2025 02:17:43 GMT',
    'x-zyb-trace-id': '8219c376dd96cdbd:8219c376dd96cdbd:0:1',
    'x-zyb-trace-t': f'{int(time.time() * 1000)}',
    'zyb-cuid': 'B456A352201353A80CB4B82EA49BA5A3|0',
    'zyb-did': '038d71f8694000020adee00040000007',
    'zyb-adid': '922eba45f74389fb5fe4c798a032bbc29abb4fe4',
    'na__zyb_source__': 'college',
    'dp-ticket': '9JncYE1/+VZj4srMUvquJOwZE2VxarMBSesT5MazXlWlcJSBjxa+s7J/6gnX9kbRvzLdihHZNBxpMBE+t/bB0ziWtPBUVHv9ZXHsYzNGUFYoaZZeGGLMicvqEDdNbC7Z2HBYUBDJe1abfgqYETuQbvIL2yLOJGBcc6u+5qA1oJH3hvsfp1+EPqLcGUKg7MCszsI0w51O6jCQC7RctsIj10p2b4v41BPzkQCkKb4+PeKmbVv5+iApcrnPBWshTuisAUTt6kcCD3K/2ami1SbchK832APVZPBltHqDOp5VUdsNRx6+JW7iukI/rPi8Y41/cFG3drE7aivpzqfSt4R0neGVKCatdB8cBIICsYpFibCtbgDh5CU3ympNm/fUl7dkprdIdcaaDJe2dflNv38sRejobci5p94lvhgdx5AasZy8d0EmB81fhy7CJDTq3fSR9NFDXOMQ7sXZAbh6crYjIIG/cgaSZT0+SFW6mDjXCksMFSATZyKhyDpOJBb9oGN03itWaaoyUZqkschmZ2Wq1y/hUFw==',
    'content-type': 'multipart/form-data; boundary=I9XYCtAhJFfqBPPbgkmOSufQRMERnNcWKrxP',
    # 'Cookie': 'cuid=B456A352201353A80CB4B82EA49BA5A3%7C0',
}
image_file = open('image1.jpg', 'rb')
files = {
    ('image', image_file, 'null')
}
data = {
    'data': 'tItXAzg0B2R+NOhynAf/RzzWpqgeEYePOFIfCBvGg2CIPZ43FsQqApriH3D9iHD388yb/5z2DfLnLiOKKH3ljvne2uppij6Xn54VR0Mv0sIXWs0D/ZNgwFCPfvkM4ZDLlAUqqy7tcThTuD/GYJqjBM+8eEbWJ3oNMzdeVDv6Dks1vcPmKLupiqUGykJnZtlzYS6Mtu+1GbBKUemQXiCqVovwSQ==',
    'area': '',
    'screensize': '1920x1080',
    'cuid': 'B456A352201353A80CB4B82EA49BA5A3|0',
    'os': 'android',
    'city': '',
    'abis': '0',
    'channel': 'taobaozhushou',
    'appBit': '32',
    'vc': '845',
    'deviceId': '',
    'token': '1_XPXQH3c5HRPtFHkSwi3sCCURmT25QfxM',
    'adid': '922eba45f74389fb5fe4c798a032bbc29abb4fe4',
    'province': '',
    'pkgName': 'com.zmzx.college.search',
    'appId': 'college',
    'vcname': '2.31.8',
    'sdk': '32',
    'operatorid': '460000',
    'device': '2201123C',
    'brand': 'Xiaomi',
    'did': '038d71f8694000020adee00040000007',
    'nt': 'wifi',

    'sign': 'aa90825cdcd03c4666a316e5441cdac9',
    # 'sign': sign,
    '_t_': f'{int(time.time())}',
    'kakorrhaphiophobia': '24989'
}
response = requests.post(
    'https://www.daxuesoutijiang.com/dxtools/search/wholesearch',
    cookies=cookies,
    headers=headers,
    files=files,
    data=data
)
print(response.text)
