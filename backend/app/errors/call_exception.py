from enum import Enum
from fastapi import HTTPException, status

def get_exception(error_code):
    message, code, headers = error_code.value
    return HTTPException(
        status_code=code,
        detail=message,
        headers=headers
    )