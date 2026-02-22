import nox

PYTHON_VERSIONS = ["3.11", "3.12", "3.13", "3.14"]

# django-modern-rest is developed alongside this package; fall back to GitHub
_DMR_GH = "django_modern_rest@git+https://github.com/wemake-services/django-modern-rest"

TEST_DEPS = [
    "pytest",
    "pytest-asyncio",
    "pytest-cov",
    "pytest-django",
    "msgspec",
]


@nox.session(python=PYTHON_VERSIONS, venv_backend="uv")
def tests(session: nox.Session) -> None:
    """Run the test suite on all supported Python versions."""
    session.install(".", *TEST_DEPS)
    session.install(_DMR_GH)
    session.run("pytest", ".", "-p", "no:cacheprovider", *session.posargs)
