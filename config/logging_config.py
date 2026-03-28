import logging
import sys


def configure_logging() -> None:
    """
    Configure application-wide logging.

    Sets:
    - INFO logging level
    - Console output
    - Consistent timestamped format
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True,
    )