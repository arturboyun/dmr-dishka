import uuid

import msgspec
from dishka import FromDishka
from dmr import Body, Controller
from dmr.plugins.msgspec import MsgspecSerializer

from dmr_dishka.integration import inject


class UserCreateModel(msgspec.Struct):
    email: str


class UserModel(UserCreateModel):
    uid: uuid.UUID
    meta: dict[str, str] = {}


class UserCreateBlueprint(
    Controller[MsgspecSerializer],
    Body[UserCreateModel],
):
    async def post(self, x: FromDishka[str]) -> UserModel:
        return UserModel(
            uid=uuid.uuid4(),
            email=self.parsed_body.email,
            meta={"from_dishka": x},
        )


class UserListBlueprint(Controller[MsgspecSerializer]):
    @inject
    async def get(self, x: FromDishka[str]) -> list[UserModel]:
        return [
            UserModel(
                uid=uuid.uuid4(),
                email="asdf@example.com",
                meta={"from_dishka": x},
            ),
        ]


class UsersController(Controller[MsgspecSerializer]):
    blueprints = (
        UserListBlueprint,
        UserCreateBlueprint,
    )
