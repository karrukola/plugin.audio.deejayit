"""Test the function to retrieve a pic's URL."""
from __future__ import annotations

from json import loads
from pathlib import Path

import pytest

from resources.lib.deejayit import DeejayIt

# ruff: noqa: INP001, S101, B011, ANN201, ANN001


@pytest.mark.parametrize(
    ("input_data", "exp_out"),
    [
        (
            "test_safe_get_pic_w_art.json",
            "https://cdn.gelestatic.it/deejay/sites/2/2023/07/Elio-carpi-puntata-1200x627.jpg",
        ),
        (
            "test_safe_get_pic_wo_art.json",
            None,
        ),
    ],
)
def test_safe_get_pic(
    input_data: str,
    exp_out: str | None,
):
    """Test the private function to get the URL of a pic."""
    deejay = DeejayIt()
    test_data = input_data
    file_path = Path(__file__).parent / test_data
    print(file_path.absolute())
    url = deejay._safe_get_pic(loads(file_path.read_text()), "size_1200x675")  # noqa:SLF001
    assert url == exp_out
