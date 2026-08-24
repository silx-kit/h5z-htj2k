from pathlib import Path

import h5py
import numpy as np
import pytest

DATA_PATH = (Path(__file__).parent / "data").resolve()


@pytest.mark.decode_only
@pytest.mark.parametrize("filename", ["bamboo_hercules.h5", "bamboo_hercules_be.h5"])
def test_bamboo_hercules(filename: str):
    with h5py.File(DATA_PATH / filename) as h5f:
        ref_data = h5f["raw"][()]
        decompressed_data = h5f["htj2k"][()]
        expected_rmse = h5f["htj2k"].attrs["RMSE"]
        expected_max_error = h5f["htj2k"].attrs["MAX_ABS_ERROR"]

    diff = decompressed_data.astype(np.float64) - ref_data.astype(np.float64)

    rmse = float(np.sqrt(np.mean(diff * diff)))
    rmse_tolerance = 0.01 * expected_rmse
    assert rmse <= expected_rmse + rmse_tolerance, f"RMSE: {rmse} > {expected_rmse}"

    max_abs_error = np.max(np.abs(diff))
    assert max_abs_error <= expected_max_error, (
        f"Max Error: {max_abs_error} > {expected_max_error}"
    )
