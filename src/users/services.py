from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .. import models
from ..auth import hash_password
from ..exceptions import BadRequestException
from .schemas import UserCreate, UserUpdate, UserUpdatePassword


class UserService:
    def __init__(self, db_session: AsyncSession):
        self._db = db_session

    async def create_user(self, user_data: UserCreate):
        user_exists = await self.get_user_by_email(user_data.email)
        if user_exists:
            raise BadRequestException(detail="User already exists")

        new_user = models.User(
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
        )

        self._db.add(new_user)
        await self._db.commit()
        await self._db.refresh(new_user)

        return new_user

    async def update_current_user(self, user: models.User, user_data: UserUpdate):
        user_data_dict = user_data.model_dump(by_alias=False, exclude_unset=True)
        for field, value in user_data_dict.items():
            setattr(user, field, value)
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def update_current_user_password(
        self, user: models.User, password_data: UserUpdatePassword
    ):
        hashed_password = hash_password(password_data.new_password)
        user.password_hash = hashed_password
        await self._db.commit()
        await self._db.refresh(user)

    async def delete_user(self, user: models.User):
        await self._db.delete(user)
        await self._db.commit()

    async def get_user_by_email(self, email: str):
        result = await self._db.execute(
            select(models.User).where(models.User.email == email)
        )
        user = result.scalars().first()
        return user
