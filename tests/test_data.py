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


@pytest.mark.decode_only
@pytest.mark.parametrize("groupname", ["v0", "v1"])
def test_versions(subtests, groupname: str):
    with h5py.File(DATA_PATH / "versions.h5") as h5f:
        ref_data = {}
        for name, entity in h5f["uncompressed"].items():
            if isinstance(entity, h5py.Group):
                ref_data[name] = entity["data"][()]
            else:
                ref_data[name] = entity[()]

        for name, entity in h5f[groupname].items():
            with subtests.test(msg=name):
                if isinstance(entity, h5py.Group):
                    dataset = entity["data"]
                else:
                    dataset = entity
                decompressed_data = dataset[()]
                expected_rmse = dataset.attrs["RMSE"]
                expected_max_error = dataset.attrs["MAX_ABS_ERROR"]

                ref_name = name.split("_", 1)[-1]
                if ref_name.startswith("be_"):
                    ref_name = ref_name[3:]
                diff = decompressed_data.astype(np.float64) - ref_data[ref_name].astype(
                    np.float64
                )

                rmse = float(np.sqrt(np.mean(diff * diff)))
                rmse_tolerance = 0.01 * expected_rmse
                assert rmse <= expected_rmse + rmse_tolerance, (
                    f"name: {name}, RMSE: {rmse} > {expected_rmse}"
                )

                max_abs_error = np.max(np.abs(diff))
                assert max_abs_error <= expected_max_error, (
                    f"name: {name}, Max Error: {max_abs_error} > {expected_max_error}"
                )
