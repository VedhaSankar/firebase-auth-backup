from email.charset import BASE64
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import base64
from firebase_admin import exceptions 
from dotenv import load_dotenv
import os

load_dotenv()

BASE64_SECRET = os.environ.get('BASE64_SECRET')
BASE64_SALT_SEPARATOR = os.environ.get('BASE64_SALT_SEPARATOR')
FILE_PATH = os.environ.get('FILE_PATH')

cred = credentials.Certificate(FILE_PATH)
firebase_admin.initialize_app(cred)

users = [
    auth.ImportUserRecord(
        uid='some-uid',
        email='user@example.com',
        password_hash=b'password_hash',
        password_salt=b'salt'
    ),
]

# All the parameters below can be obtained from the Firebase Console's "Users"
# section. Base64 encoded parameters must be decoded into raw bytes.
hash_alg = auth.UserImportHash.scrypt(
    key=base64.b64decode(BASE64_SECRET),
    salt_separator=base64.b64decode(BASE64_SALT_SEPARATOR),
    rounds=8,
    memory_cost=14
)
try:
    print("trying...")
    result = auth.import_users(users, hash_alg=hash_alg)
    print(result.uid)
    for err in result.errors:
        print('Failed to import user:', err.reason)
except exceptions.FirebaseError as error:
    print('Error importing users:', error)