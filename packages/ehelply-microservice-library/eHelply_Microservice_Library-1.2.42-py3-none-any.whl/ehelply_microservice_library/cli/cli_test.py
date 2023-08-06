import typer
import pytest
from pytest import ExitCode
import os
from pathlib import Path
import coverage

cli = typer.Typer()


# https://docs.pytest.org/en/documentation-restructure/how-to/writing_plugins.html#well-specified-hooks
class eHelplyPytest:
    pass
    # def pytest_sessionfinish(self):
    #     print("", "*** starting coverage report ***")

COVERAGE_THRESHOLD: int = 80


@cli.command()
def units(

):
    root_path = Path(os.getcwd())

    docs_location = Path(root_path).resolve().joinpath('test-results')
    docs_location.mkdir(exist_ok=True)

    result: ExitCode = pytest.main(
        [
            "-s",
            "--cov-report", "term-missing",
            "--cov-report", f"html:{str(docs_location)}",
            "--cov=src",
            "tests/"
        ]
    )

    if result != ExitCode.OK:
        raise typer.Exit(code=result)

    cov = coverage.Coverage()
    cov.load()

    coverage_amount: float = cov.json_report()

    if coverage_amount < COVERAGE_THRESHOLD:
        raise Exception(f"Test coverage is {int(coverage_amount)}% which is below {COVERAGE_THRESHOLD}%. Thus, build has failed.")
