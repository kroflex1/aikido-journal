from datetime import timedelta, datetime
from http.client import HTTPException

from jose import jwt, JWTError

from src.config import SECRET_KEY


class TokenManager:
    __SECRET_KEY = SECRET_KEY
    __ALGORITHM = "HS256"
    __ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 60

    @staticmethod
    def create_token(user_id: int, user_role: str):
        to_encode = {"user_id": str(user_id), "user_role": str(user_role),
                     "exp": datetime.utcnow() + timedelta(minutes=TokenManager.__ACCESS_TOKEN_EXPIRE_MINUTES)}
        encoded_jwt = jwt.encode(to_encode, TokenManager.__SECRET_KEY, algorithm=TokenManager.__ALGORITHM)
        return encoded_jwt

    @staticmethod
    def check_token(token: str):
        try:
            jwt.decode(token, TokenManager.__SECRET_KEY, algorithms=[TokenManager.__ALGORITHM])
        except JWTError:
            raise HTTPException(status_code=407, detail="Invalid token")

    @staticmethod
    def get_user_id_from_token(token: str) -> int:
        TokenManager.check_token(token)
        payload = jwt.decode(token, TokenManager.__SECRET_KEY, algorithms=[TokenManager.__ALGORITHM])
        if datetime.fromtimestamp(int(payload.get("exp"))) < datetime.now():
            raise HTTPException(status_code=407, detail="Token expire")
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise HTTPException(status_code=407, detail="User id is empty")
        return int(user_id)
