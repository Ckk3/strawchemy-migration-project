#!/usr/bin/env python3
"""
Generate GraphQL schema SDL files from both projects.

This is the main orchestrator script that runs the individual schema generators
for each project. It handles running each generator in the correct virtual
environment using `uv run`.

Usage:
    Run from the project root directory:

        python utils/generate_schemas.py

Output:
    Generated schema files are written to:
        - schemas/strawberry-sqlalchemy-mapper/*.graphql
        - schemas/strawchemy/*.graphql

Why subprocess?
    Each project has different dependencies (strawberry-sqlalchemy-mapper vs strawchemy),
    so we need to run each generator in its own virtual environment to have access
    to the correct libraries.
"""

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


# =============================================================================
# Configuration
# =============================================================================


@dataclass
class ProjectConfig:
    """Configuration for a project whose schemas we want to generate.

    Attributes:
        name: Human-readable name for display
        project_dir: Path to the project directory (where uv run will execute)
        generator_script: Path to the generator script for this project
        output_dir: Path where generated .graphql files will be written
    """

    name: str
    project_dir: Path
    generator_script: Path
    output_dir: Path


def get_project_configs() -> list[ProjectConfig]:
    """Get the configuration for all projects.

    Returns:
        List of ProjectConfig objects for each project to generate schemas from
    """
    # Resolve paths relative to this script's location
    project_root = Path(__file__).parent.parent.resolve()
    utils_dir = Path(__file__).parent.resolve()
    schemas_dir = project_root / "schemas"

    return [
        ProjectConfig(
            name="strawberry-sqlalchemy-mapper",
            project_dir=project_root / "strawberry-sqlalchemy-project",
            generator_script=utils_dir / "generate_strawberry_sqlalchemy_mapper.py",
            output_dir=schemas_dir / "strawberry-sqlalchemy-mapper",
        ),
        ProjectConfig(
            name="strawchemy",
            project_dir=project_root / "strawchemy-migrated-project",
            generator_script=utils_dir / "generate_strawchemy.py",
            output_dir=schemas_dir / "strawchemy",
        ),
    ]


# =============================================================================
# Functions
# =============================================================================


def print_header() -> None:
    """Print the script header."""
    print("=" * 60)
    print("GraphQL Schema Generator")
    print("=" * 60)


def print_footer(all_successful: bool) -> None:
    """Print the script footer with status summary."""
    print("\n" + "=" * 60)
    if all_successful:
        print("Schema generation complete!")
    else:
        print("Schema generation completed with errors.")
    print("Output directory: schemas/")
    print("=" * 60)


def run_generator(config: ProjectConfig) -> bool:
    """Run a generator script in its project's virtual environment.

    This function uses `uv run` to execute the generator script within the
    project's virtual environment, ensuring access to the correct dependencies.

    Args:
        config: Configuration for the project to generate schemas from

    Returns:
        True if the generator succeeded, False otherwise
    """
    # Build the command to run
    command = [
        "uv",
        "run",
        "python",
        str(config.generator_script),
        str(config.output_dir),
    ]

    # Run the generator in the project directory
    result = subprocess.run(
        command,
        cwd=config.project_dir,
        capture_output=True,
        text=True,
    )

    # Print any output from the generator
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="")

    return result.returncode == 0


def ensure_output_directory_exists(config: ProjectConfig) -> None:
    """Create the output directory if it doesn't exist.

    Args:
        config: Configuration containing the output directory path
    """
    config.output_dir.mkdir(parents=True, exist_ok=True)


def generate_schemas_for_project(config: ProjectConfig) -> bool:
    """Generate all schemas for a single project.

    Args:
        config: Configuration for the project

    Returns:
        True if successful, False otherwise
    """
    print(f"\nGenerating {config.name} schemas...")

    ensure_output_directory_exists(config)
    success = run_generator(config)

    return success


def generate_all_schemas() -> bool:
    """Generate schemas for all configured projects.

    Returns:
        True if all projects succeeded, False if any failed
    """
    configs = get_project_configs()

    all_successful = True
    for config in configs:
        success = generate_schemas_for_project(config)
        if not success:
            all_successful = False

    return all_successful


# =============================================================================
# Main Entry Point
# =============================================================================


def main() -> int:
    """Main entry point for the script.

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    print_header()

    all_successful = generate_all_schemas()

    print_footer(all_successful)

    return 0 if all_successful else 1


if __name__ == "__main__":
    sys.exit(main())
