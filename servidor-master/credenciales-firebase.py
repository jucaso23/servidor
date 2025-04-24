import os
import json
from firebase_admin import credentials

def cargar_credenciales_firebase():
    cred_json = os.environ.get("FIREBASE_CREDENTIALS")
    if not cred_json:
        raise ValueError("FIREBASE_CREDENTIALS no está definida en el entorno.")
    cred_dict = json.loads(cred_json)
    return credentials.Certificate(cred_dict)