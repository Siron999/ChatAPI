
from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse
from app.service.user_service import UserService
from ..model.user_model import UserModel
from ..dto.user_dto import LoginDTO
from ..dto.request_response_dto import get_response
from ..config.logger_config import logger
from ..filter.jwt_filter import jwt_filter

user_route = APIRouter()
user_service = UserService()


@user_route.get("/user/current-user", status_code=status.HTTP_200_OK)
def get_current_user(current_user: dict = Depends(jwt_filter)):
    logger.info("Inside get_current_user")
    username = current_user["username"]
    user = user_service.get_current_user(username)
    return get_response(status=200, data=user)


@user_route.post("/user/login", status_code=status.HTTP_200_OK)
def login(user: LoginDTO):
    logger.info(f'Inside Login for user {user.username}')
    access_token = user_service.login(user)
    response = JSONResponse(content=access_token)
    response.set_cookie(
        key="access_token", value=access_token["access_token"], secure=True)
    return response


@user_route.post("/user/register", status_code=status.HTTP_201_CREATED)
def register(user: UserModel):
    logger.info(f'Inside Register for user {user.username}')
    user_id = user_service.register(user)
    return get_response(201, detail="User registered successfully", data={"_id": user_id})
