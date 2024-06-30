from fastapi import FastAPI
from app.controller.user_controller import user_route
from app.filter.exception_filter import validation_exception_handler

app = FastAPI()
app.include_router(user_route)

app.add_exception_handler(Exception, validation_exception_handler)
