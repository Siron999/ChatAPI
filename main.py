from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.controller.user_controller import user_route

app = FastAPI()
app.include_router(user_route)


@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "detail": (
                f"Failed method {request.method} at URL {request.url}."
                f" Exception message is {exc!r}."
            )
        },
    )
