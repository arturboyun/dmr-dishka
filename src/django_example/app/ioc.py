from dishka import Provider, Scope, provide


class AppProvider(Provider):
    @provide(scope=Scope.SESSION)
    def provide_asdf(self) -> str:
        return "Hello from Dishka!"
