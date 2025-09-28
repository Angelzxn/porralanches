from datetime import datetime, timezone, timedelta
from config import Config
from jose import jwt, ExpiredSignatureError, JWTError


def criar_token(id):
    data_expiracao = datetime.now(timezone.utc)+ timedelta(minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES)

    dic_info = {
        "sub": str(id),
        "exp": data_expiracao
    }
    encoded_jwt = jwt.encode(dic_info, Config.SECRET_KEY, Config.ALGORITHM)

    return encoded_jwt


def decodificar_token(token_user):
    try:
        decoded = jwt.decode(token_user, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        
        sub = decoded.get("sub")
        exp_timestamp = decoded.get("exp")
        
        exp = None
        if exp_timestamp:
            exp = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
        
        return {
            "sub": sub,
            "exp": exp
        }
    
    except ExpiredSignatureError:
        raise PermissionError("Token expirado")
    except JWTError:
        raise RuntimeError("Erro ao decodificar token")
