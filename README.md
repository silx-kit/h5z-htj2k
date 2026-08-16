# h5z-htj2k

HDF5 filter plugin for [High-Throughput JPEG2000 compression](https://jpeg.org/jpeg2000/htj2k.html) (a.k.a. htj2k).

This version of the compression filter supports:

- Array datasets of integer elements of type: signed or unsigned, 1 or 2 bytes wide (i.e., int8, uint8, int16, uint16).
- Chunk shapes with at most 2 non-unity dimensions.

This filter currently accepts no user parameter through HDF5 filter options `cd_values` and compresses data in a reversible way (lossless).
To configure the compression, e.g., to save data in an irreversible way (lossy), compress chunks with a library supporting htj2k and use HDF5 direct chunk write (see [H5Dwrite_chunk](https://support.hdfgroup.org/documentation/hdf5/latest/group___h5_d.html)) to save them in a HDF5 dataset (see [`direct_chunk_write.py` sample code](./examples/direct_chunk_write.py)).

The chunks contain a bare high-throughput jpeg2000 codestream.

This repository contains a reference implementation of the filter based on [OpenJPH](https://github.com/aous72/OpenJPH).

## Filter `cd_values`

This filter currently accepts no user-defined HDF5 filter options `cd_values`.

However, HDF5 filter options `cd_values` are computed automatically and stored by the filter's `set_local` function when creating HDF5 datasets:

- 0: Filter version = 1
- 1: Data type: `(0x80 if is_signed else 0x00) | data_type_size_in_bytes`:
  | Size | Unsigned | Signed |
  |---|---|---|
  | 1 byte | uint8: `0x01` | int8: `0x81` |
  | 2 bytes | uint16: `0x02` | int16: `0x82` |

  If set to `0x00` or missing, the decompression infers the data type size from the bitdepth stored in the jpeg2000 codestream.
  Other values are not supported by this filter.

- 2: Width
- 3: Height
- 4: Number of components (1 or 3)

For decompression, the first 2 `cd_values` only are used to retrieve the dataset's data type size.
Signedness and dimensions are retrieved from the jpeg2000 codestream.

## Build

```bash
mkdir build && cd build
cmake ..
make
```

### Options

| Option | Default | Description |
|---|---|---|
| `-DDECODE_ONLY=ON` | `OFF` | Build in decode-only mode (encoder disabled). |
| `-DCMAKE_BUILD_TYPE=<type>` | `Release` | `Debug`, `Release`, `RelWithDebInfo`, or `MinSizeRel`. |
| `-DHDF5_PLUGIN_INSTALL_DIR=<path>` | `<libdir>/hdf5/plugin` | Override the HDF5 plugin install directory. |
| `-DBACKEND_INCLUDE_DIR=<path>` | *(empty)* | Directory containing the backend's headers. Must be set together with `BACKEND_LIB_DIR`, or not at all. Default: Use vendored openjph library |
| `-DBACKEND_LIB_DIR=<path>` | *(empty)* | Directory containing the backend's shared libraries. Must be set together with `BACKEND_INCLUDE_DIR`, or not at all. Default: Use vendored openjph library. |

## Install

```bash
make install
```

## Development

Use `pixi` to build and test the filter:

- Build the filter: `pixi run build`
- Build and test the filter: `pixi run test`
- Run tests with the Python implementation of the filter: `pixi run test-py`
- Remove the build folder: `pixi run distclean`
- Build the filter with some configuration options, e.g. `DECODE_ONLY`: `pixi run build "-DDECODE_ONLY=ON"`

And to check code formatting and linting: `pixi run check`

## Credits

- A. Mirone for benchmark&evaluation of jpeg2000 libraries
- Existing HDF5 filters: bitshuffle, blosc, bzip2, zfp
