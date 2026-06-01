from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

from config import API_USERNAME, API_PASSWORD

security = HTTPBasic()

def authenticate(
    credentials: HTTPBasicCredentials = Depends(security)
):
    valid_user = secrets.compare_digest(
        credentials.username,
        API_USERNAME
    )

    valid_pass = secrets.compare_digest(
        credentials.password,
        API_PASSWORD
    )

    if not (valid_user and valid_pass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed"
        )

    return credentials.username
