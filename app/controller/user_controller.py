from bson import ObjectId
import datetime
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from app.config.db_config import user_collections
from ..model.user_model import UserModel
from ..dto.user_dto import LoginDTO, UserDTO
from ..dto.request_response_dto import get_response
from ..config.logger_config import logger
from ..auth.jwt_handler import sign_jwt, jwt_filter

user_route = APIRouter()


@user_route.get("/user/current-user", status_code=status.HTTP_200_OK)
def get_current_user(current_user: dict = Depends(jwt_filter)):
    logger.info(f'get_current_user called for username{
                current_user["username"]}')
    user = user_collections.find_one({"username": current_user["username"]})

    if user:
        logger.info(f'Details for {
                    current_user["username"]} fetched successfully')
        return get_response(status=200, data=UserDTO.from_user_collection(user))
    logger.error(f'HTTPException: {current_user["username"]} not found')
    raise HTTPException(status_code=404, detail="Item not found")


@user_route.post("/user/login", status_code=status.HTTP_200_OK)
def login(user: LoginDTO):
    logger.info(f'Login called for username{user.username} {user.password}')

    user_in_db = user_collections.find_one({"username": user.username})

    if user_in_db:
        logger.info(f'Username found {user.username}')
        user_model = UserModel.from_user_collection(user_in_db)

        if user_model.verify_password(plain_password=user.password):
            logger.info(f'Login successfull for {user.username}')
            access_token = sign_jwt(
                username=user_in_db["username"], role=user_in_db["role"])
            response = JSONResponse(content=access_token)
            response.set_cookie(
                key="access_token", value=access_token["access_token"], secure=True)
            return response

    logger.error(f'Invalid credentials for {user.username}')
    raise HTTPException(status_code=400, detail="Invalid credentials")


@user_route.post("/user/register", status_code=status.HTTP_201_CREATED)
def register(user: UserModel):
    logger.info(f'Inside register for user {
                dict(user)["username"]}')

    # hashpassowrd
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
    logger.info(f'User saved succesfully. User: {
                saved_user.inserted_id}')
    return get_response(201, detail="User registered successfully", data={"_id": str(saved_user.inserted_id)})
