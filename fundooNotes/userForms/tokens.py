import datetime

from fundooNotes.settings import SECRET_KEY
import jwt

def token_activation(username, password=None):
   
    data = {
        'username': username,
        'password': password,
        'exp': datetime.datetime.now()+datetime.timedelta(minutes=2)
    }
    
    token = jwt.encode(data, SECRET_KEY, algorithm="HS256").decode('utf-8')
    return token