"""nox configuration file."""
import nox

# ruff: noqa: ANN001, ANN201

_PY_VERS = ["3.8", "3.10"]
_KODI_VERS = [19, 20]  # all supported versions
_KODI_CUR_VER = 20  # current one

_PYTEST_BASE_CMDLINE = "python -m pytest -q ./tests/"
_PYTEST_UT_CMDLINE = _PYTEST_BASE_CMDLINE + "unittests/"
_PYTEST_IT_CMDLINE = _PYTEST_BASE_CMDLINE + "integrationtests/"

_COV_TGT = 99


def __upgrade_deps(session: nox.session) -> None:
    """Go through the commands to upgrade dependencies.

    This is needed because I cannot find a way to create a venv with `--upgrade-deps`
    So, we explicitily always guarantee that `pip` and `wheel` are up to date.

    Args:
    ----
        session (nox.session): the NOX session

    """
    session.install("-U", "pip")
    session.install("-U", "pip", "wheel")


@nox.session(python=_PY_VERS)
@nox.parametrize("kodi", _KODI_VERS)
def lint(session, kodi) -> None:
    """Lint the code."""
    __upgrade_deps(session)
    session.install("-r", "requirements.in", f"kodistubs=={kodi}.*")
    session.run("ruff", "format", "--check", ".")
    session.run("ruff", ".")
    # TODO: re-enable mypy once understood how to make kodistubs work
    # mypy --explicit-package-bases main.py resources/


@nox.session(python=_PY_VERS)
@nox.parametrize("kodi", _KODI_VERS)
def tests_unit(session, kodi) -> None:
    """Run unit tests."""
    __upgrade_deps(session)
    session.install("-r", "requirements.in", f"kodistubs=={kodi}.*")
    session.run(*_PYTEST_UT_CMDLINE.split(" "))


@nox.session(python=_PY_VERS)
# @nox.parametrize("kodi", _KODI_VERS)
def tests_integration(session) -> None:
    """Run integration tests."""
    __upgrade_deps(session)
    session.install("-r", "requirements.in", f"kodistubs=={_KODI_CUR_VER}.*")
    session.run(*_PYTEST_IT_CMDLINE.split(" "))


@nox.session(python=_PY_VERS[-1])
def coverage(session):
    """Verify test coverage does not fall below target."""
    __upgrade_deps(session)
    session.install("-r", "requirements.in", f"kodistubs=={_KODI_CUR_VER}.*")
    cmd_coverage = _PYTEST_UT_CMDLINE.replace("python", "coverage run")
    session.run(*cmd_coverage.split(" "))
    cmd_report = f"coverage report --fail-under {_COV_TGT}"
    session.run(*cmd_report.split(" "))
