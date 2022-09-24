from datetime import timedelta
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import DB
from ats.models.enums import Tags
from ats.security import authenticate_user, CREDENTIALS_EXCEPTION, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(
    prefix='/auth',
    tags=[Tags.auth]
)


@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db=DB.USERS, username=form_data.username, password=form_data.password)
    if not user:
        raise CREDENTIALS_EXCEPTION
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username}, expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
