from fastapi import APIRouter


class BaseRouter(APIRouter):
    def __init__(self):
        super().__init__()


