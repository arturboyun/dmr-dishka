class DishkaIsNotSetupError(RuntimeError):
    def __init__(self) -> None:
        super().__init__(
            "Dishka container is not set up. "
            "Please call setup_dishka(container) during initialization.",
        )
