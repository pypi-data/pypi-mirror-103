from typing import List, Optional

import typer

from kapla.cli.globals import repo
from kapla.cli.utils import current_directory, run

app = typer.Typer(
    name="k",
    add_completion=False,
    no_args_is_help=True,
    invoke_without_command=False,
    help="Python monorepo toolkit",
)


@app.command("build")
def build(
    format: Optional[str] = None,
    package: Optional[List[str]] = typer.Argument(None, help="Packages to build"),
    skip: Optional[List[str]] = typer.Option(
        None, "-s", "--skip", help="Packages to skip"
    ),
) -> None:
    """Build all or some packages using poetry."""
    packages = [pkg for pkg in package if pkg not in (skip or [])] if package else []
    print(packages)
    repo.build_packages(packages, format)


@app.command("test")
def test(
    package: Optional[List[str]] = typer.Argument(default=None),
    markers: List[str] = typer.Option(
        [], "--markers", "-m", help="specify markers to run only a subset of tests."
    ),
    exprs: List[str] = typer.Option(
        [],
        "--exprs",
        "-k",
        help="Pytest expression to select tests based on their name.",
    ),
) -> None:
    """Run unit tests using pytest."""
    packages = list(package or [])
    repo.test_packages(packages, markers=markers, exprs=exprs)


@app.command("bump")
def bump(
    version: str = typer.Argument(
        ..., metavar="VERSION", help="New version to bump to."
    )
) -> None:
    """Bump packages to a new version."""
    repo.bump_packages(version)


@app.command("lint")
def lint(
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Lint all source code using flake8."""
    packages = list(package or [])
    repo.lint_packages(packages)


@app.command("typecheck")
def typecheck(
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Run mypy typechecking againt all source code."""
    packages = list(package or [])
    repo.typecheck_packages(packages)


@app.command("format")
def format(
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Format all source code using black."""
    packages = list(package or [])
    repo.format_packages(packages)


@app.command("install")
def install(
    package: Optional[List[str]] = typer.Argument(default=None),
    skip: Optional[List[str]] = typer.Option(None, "--skip", "-s"),
) -> None:
    """Install all packages in editable mode and development dependencies."""
    packages = list(package or [])
    skip = list(skip or [])
    repo.install_packages(packages, skip=skip)


@app.command("clean")
def clean(
    package: Optional[List[str]] = typer.Argument(default=None), dist: bool = True
) -> None:
    """Clean directories."""
    packages = list(package or [])
    repo.clean_packages(packages, no_dist=not dist)


@app.command("update")
def update(package: Optional[List[str]] = typer.Argument(default=None)) -> None:
    """Update all packages dependencies and generate lock file."""
    packages = list(package or [])
    repo.update_packages(packages)


@app.command("export")
def export(
    package: Optional[List[str]] = typer.Argument(default=None),
) -> None:
    """Export all packages for offline installation."""
    if not package:
        repo.export_packages()
    else:
        for project in repo.get_packages(list(package)):
            project.export()


@app.command("coverage")
def coverage() -> None:
    """Start HTML server displaying code coverage."""
    with current_directory(repo.root):
        run("python -m http.server --bind 127.0.0.1 --directory coverage-report")


@app.command("commit")
def commit() -> None:
    """Commit changes to git repository."""
    with current_directory(repo.root):
        run("cz commit")


@app.command("config")
def config() -> None:
    """Print config to console."""
    print(repo.config)
