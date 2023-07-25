import nox

_PY_VERS = ["3.8"]

_KODI_VERS = [19, 20]


@nox.session(python=_PY_VERS)
@nox.parametrize("kodi", _KODI_VERS)
def lint(session, kodi):
    session.install("-r", "requirements.in", f"kodistubs>={kodi},<{kodi+1}")
    session.run("ruff", ".")
    session.run("mypy", "--explicit-package-bases", "default.py", "resources")


@nox.session(python=_PY_VERS)
@nox.parametrize("kodi", _KODI_VERS)
def test(session, kodi):
    session.install("-r", "requirements.in", f"kodistubs>={kodi},<{kodi+1}")
    session.run("python", "-m", "pytest", "-rAv", "tests/.")
