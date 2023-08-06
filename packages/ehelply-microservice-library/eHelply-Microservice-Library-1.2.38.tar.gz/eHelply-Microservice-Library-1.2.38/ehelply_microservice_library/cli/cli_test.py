import typer
import pytest
import os
from pathlib import Path

cli = typer.Typer()


# https://docs.pytest.org/en/documentation-restructure/how-to/writing_plugins.html#well-specified-hooks
class eHelplyPytest:
    pass
    # def pytest_sessionfinish(self):
    #     print("", "*** starting coverage report ***")


@cli.command()
def units(

):
    root_path = Path(os.getcwd())

    docs_location = Path(root_path).resolve().joinpath('test-results')
    docs_location.mkdir(exist_ok=True)

    pytest.main(
        [
            "-s",
            "--cov-report", "term-missing",
            "--cov-report", f"html:{str(docs_location)}",
            "--cov=src",
            "tests/"
        ]
    )
