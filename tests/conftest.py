import htj2k_filter


def pytest_addoption(parser):
    parser.addoption(
        "--use-python-filter",
        action="store_true",
        help="Run tests with the Python implementation of the filter",
    )


def pytest_configure(config):
    if config.getoption("--use-python-filter"):
        if not htj2k_filter.register(force=True):
            raise RuntimeError("Failed to register Python filter")
