from enum import Enum
from fastapi import HTTPException, status

from .call_exception import get_exception

class HttpErrorCode(Enum):
    # 에러 이름 = 에러 메시지, 상태 코드, 헤더
    CREDENTIALS_ERROR = ("Could not validate credentials", status.HTTP_401_UNAUTHORIZED, {"WWW-Authenticate": "Bearer"}) 
    NOT_FOUND = ("The requested resource could not be found", status.HTTP_404_NOT_FOUND, None)
    USER_NOT_FOUND = ("User not found", status.HTTP_404_NOT_FOUND, None)
    EXCHANGE_TOKEN_ERROR = ("Failed to exchange authorization code for tokens", status.HTTP_400_BAD_REQUEST, None)
    RETRIEVE_USER_INFO_ERROR = ("Failed to retrieve user information from Google", status.HTTP_400_BAD_REQUEST, None)
    PROJECT_NOT_FOUND = ("Project not found", status.HTTP_404_NOT_FOUND, None)
    NO_UPLOADED_VOICE = ("No uploaded voice", status.HTTP_404_NOT_FOUND, None)
    UPLOADED_VOICE_DIR_ERROR = ("Uploaded voice directory must be singular", status.HTTP_400_BAD_REQUEST, None)

    def __call__(self):
        return get_exception(self)
    