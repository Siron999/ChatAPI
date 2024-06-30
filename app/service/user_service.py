from bson import ObjectId
import datetime
from fastapi import HTTPException, status
from app.config.db_config import user_collections
from ..model.user_model import UserModel
from ..dto.user_dto import LoginDTO, UserDTO
from ..config.logger_config import logger
from ..filter.jwt_filter import sign_jwt


class UserService:
    def get_current_user(self, username: str):
        logger.info(f'get_current_user called for username {username}')
        user = user_collections.find_one({"username": username})

        if user:
            logger.info(f'Details for {username} fetched successfully')
            return UserDTO.from_user_collection(user)
        logger.error(f'HTTPException: {username} not found')
        raise HTTPException(status_code=404, detail="Item not found")

    def login(self, user: LoginDTO):
        logger.info(f'Login called for username {user.username}')

        user_in_db = user_collections.find_one({"username": user.username})

        if user_in_db:
            logger.info(f'Username found {user.username}')
            user_model = UserModel.from_user_collection(user_in_db)

            if user_model.verify_password(plain_password=user.password):
                logger.info(f'Login successful for {user.username}')
                access_token = sign_jwt(
                    username=user_in_db["username"], role=user_in_db["role"])
                return access_token

        logger.error(f'Invalid credentials for {user.username}')
        raise HTTPException(status_code=400, detail="Invalid credentials")

    def register(self, user: UserModel):
        logger.info(f'Register called for user {user.username}')

        # hash password
        user.hash_password()

        user_dict = dict(user)

        # checking if username or email exists
        user_in_db = user_collections.find_one({
            "$or": [
                {"username": user_dict["username"]},
                {"email": user_dict["email"]}
            ]
        })

        if user_in_db:
            logger.error(f'Exception: {user_dict["username"]} or {
                         user_dict["email"]} already exists')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

        user_dict["created_at"] = datetime.date.today().isoformat()
        saved_user = user_collections.insert_one(user_dict)
        logger.info(f'User saved successfully. User: {saved_user.inserted_id}')
        return str(saved_user.inserted_id)
