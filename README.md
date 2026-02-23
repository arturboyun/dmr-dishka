# Django Modern REST integration for Dishka

[![test](https://github.com/arturboyun/dmr-dishka/actions/workflows/tests.yml/badge.svg?event=push)](https://github.com/arturboyun/dmr-dishka/actions/workflows/tests.yml)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/arturboyun/dmr-dishka/tests.yml)](https://github.com/arturboyun/dmr-dishka/actions)
[![License](https://img.shields.io/github/license/arturboyun/dmr-dishka)](https://github.com/arturboyun/dmr-dishka/blob/main/LICENSE)
![Version](https://img.shields.io/pypi/v/dmr-dishka)
![Python Version](https://img.shields.io/pypi/pyversions/dmr-dishka)

> PyPi version and python version is cached now! Sorry for that.

This package provides integration of [Dishka](http://github.com/reagento/dishka/) dependency injection framework and [Modern REST framework for Django](https://github.com/wemake-services/django-modern-rest) with types and async support!

## Installation

```bash
pip install dmr-dishka
```

```bash
uv add dmr-dishka
```

## How to use async

1. Import

```python
from dishka import Provider, provide, Scope

class YourProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_x(self, request: Request) -> X:
         ...
```

2. Create provider.

```python
class YourProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def create_x(self) -> X:
         ...
```

3. Mark those of your handlers parameters which are to be injected with `FromDishka[]` and decorate them using `@inject`

```python
from dmr_dishka.integration import inject

class ExampleBlueprint(Controller[MsgspecSerializer]):
    @inject
    async def get(self, x: FromDishka[X])
        ...
```

1. Make container

```python
container = make_async_container(YourProvider())
```

2. Setup dishka integration in your `asgi.py`

```python
# asgi.py
from dishka import make_async_container
from django_example.app.ioc import AppProvider
from dmr_dishka.integration import setup_dishka

container = make_async_container(AppProvider())
setup_dishka(container)
```

## How to use sync

1. Steps 1 and 2 is identical to async
2. In step 3 you need to decorate your handlers with `@inject_sync` and their parameters should be marked with `FromDishka[]` as well

```python
from dmr_dishka.integration import inject_sync

class ExampleBlueprint(Controller[MsgspecSerializer]):
    @inject_sync
    def get(self, x: FromDishka[X])
        ...
```

3. Step 4 is identical to async
4. In step 5 need to setup dishka in your `wsgi.py` instead of `asgi.py`

```python
# wsgi.py
from dishka import make_container
from django_example.app.ioc import AppProvider
from dmr_dishka.integration import setup_dishka

container = make_container(AppProvider())
setup_dishka(container)
```

| Check src/django_example for more examples of usage.
