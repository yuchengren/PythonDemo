import json
import requests
import base64
from io import BytesIO
from PIL import Image
from sys import version_info


def img_recognise(username, pwd, img_path):
    img = Image.open(img_path)
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {"username": username, "password": pwd, "image": b64}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    print("img_path=%s, result=%s" % (img_path, result))
    if result['success']:
        return result["data"]["result"]
    return None

