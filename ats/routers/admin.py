from fastapi import APIRouter, Depends

import DB
from ats.models.general import Tags
from ats.models.users import RegisterUser
from ats.security import admin_permission, create_user

router = APIRouter(
    prefix='/admin',
    tags=[Tags.admin],
    dependencies=[Depends(admin_permission)]
)


@router.post('/users')
async def register_new_user(reg_user: RegisterUser):
    user = create_user(reg_user)
    DB.USERS[user.username] = user.dict()
    return {'username': user.username}
