from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ats import enums
from ats.models.users import RegisterUser
from ats.security import admin_permission, create_user
from ats.dependencies import get_db
from database.models import UserModel

router = APIRouter(
    prefix='/admin',
    tags=[enums.Tags.admin],
    dependencies=[Depends(admin_permission)]
)


@router.post('/users/')
async def register_new_user(reg_user: RegisterUser, db: Session = Depends(get_db)):
    user = create_user(reg_user)
    user_to_db = UserModel(**user.dict())
    db.add(user_to_db)
    db.commit()
    return {'username': user.username}
