from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ats.dependencies import get_db
from ats import enums
from ats.security import authenticate_user, CREDENTIALS_EXCEPTION, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    Token

router = APIRouter(
    tags=[enums.Tags.auth]
)


@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise CREDENTIALS_EXCEPTION
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
