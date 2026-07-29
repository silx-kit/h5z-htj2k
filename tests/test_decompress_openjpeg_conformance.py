from pathlib import Path

import imagecodecs
import pooch
import pytest
from utils import assert_decompress

OPENJPEG_DATA_COMMIT = "39524bd3a601d90ed8e0177559400d23945f96a9"
OPENJPEG_DATA_URL = (
    f"https://github.com/uclouvain/openjpeg-data/archive/{OPENJPEG_DATA_COMMIT}.tar.gz"
)


@pytest.fixture
def openjpeg_data_registry(cache):
    return pooch.create(
        path=cache.mkdir("openjpeg_data"),
        base_url=f"https://raw.githubusercontent.com/uclouvain/openjpeg-data/{OPENJPEG_DATA_COMMIT}/",
        registry={
            "input/nonregression/byte.tif": "sha256:e0fad3830408e34fa815d3663eac888595250671616accc28e6e55d1aca6c2f4",
            "input/nonregression/htj2k/byte_causal.jhc": "sha256:8d4a48d1cfff47420203283f3eb1b5c48f92dd1a6c23916a18934a44f154002f",
        },
    )


def test_byte(openjpeg_data_registry):
    codestream = Path(
        openjpeg_data_registry.fetch("input/nonregression/htj2k/byte_causal.jhc")
    ).read_bytes()
    expected = imagecodecs.imread(
        openjpeg_data_registry.fetch("input/nonregression/byte.tif")
    )
    assert_decompress(codestream, expected)
