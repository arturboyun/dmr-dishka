import logging
import uuid

import msgspec
from dishka import AsyncContainer, FromDishka
from django.http import HttpRequest
from dmr import Body, Controller
from dmr.plugins.msgspec import MsgspecSerializer

from dmr_dishka.integration import inject

logger = logging.getLogger(__name__)


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
    async def get(
        self,
        x: FromDishka[str],
        container: FromDishka[AsyncContainer],
        request: FromDishka[HttpRequest],
    ) -> list[UserModel]:
        logger.info(
            "Got container in get method: %s, with scope: %s",
            container,
            container.scope,
        )
        logger.info("Got request in get method: %s", request)
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
