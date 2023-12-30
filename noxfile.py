"""nox configuration file."""
import nox

# ruff: noqa: ANN001, ANN201

_PY_VERS = ["3.8"]
_KODI_VERS = [19, 20]

_PYTEST_BASE_CMDLINE = "python -m pytest ./tests/"
_PYTEST_UT_CMDLINE = _PYTEST_BASE_CMDLINE + "unittests/"
_PYTEST_IT_CMDLINE = _PYTEST_BASE_CMDLINE + "integrationtests/"

_COV_TGT = 99


@nox.session(python=_PY_VERS)
@nox.parametrize("kodi", _KODI_VERS)
def lint(session, kodi) -> None:
    """Lint the code."""
    session.install("-r", "requirements.in", f"kodistubs>={kodi},<{kodi+1}")
    session.run("ruff", "format", "--check", ".")
    session.run("ruff", ".")
    session.run("mypy", "--explicit-package-bases", "main.py", "resources")


@nox.session(python=_PY_VERS)
@nox.parametrize("kodi", _KODI_VERS)
def tests_unit(session, kodi) -> None:
    """Run unit tests."""
    session.install("-r", "requirements.in", f"kodistubs>={kodi},<{kodi+1}")
    session.run(*_PYTEST_UT_CMDLINE.split(" "))


@nox.session(python=_PY_VERS)
# @nox.parametrize("kodi", _KODI_VERS)
def tests_integration(session) -> None:
    """Run integration tests."""
    kodi = _KODI_VERS[-1]
    session.install("-r", "requirements.in", f"kodistubs>={kodi},<{kodi+1}")
    session.run(*_PYTEST_IT_CMDLINE.split(" "))


@nox.session(python=_PY_VERS[-1])
def coverage(session):
    """Verify test coverage does not fall below target."""
    kodi = _KODI_VERS[-1]
    session.install("-r", "requirements.in", f"kodistubs>={kodi},<{kodi+1}")

    cmd_coverage = _PYTEST_UT_CMDLINE.replace("python", "coverage run")
    session.run(*cmd_coverage.split(" "))
    cmd_report = f"coverage report --fail-under {_COV_TGT}"
    session.run(*cmd_report.split(" "))
