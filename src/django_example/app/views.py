from dishka import FromDishka
from django.http import HttpRequest, JsonResponse

from dmr_dishka.integration import inject


@inject
async def index(request: HttpRequest, asdf: FromDishka[str]) -> JsonResponse:
    return JsonResponse({"message": asdf})
