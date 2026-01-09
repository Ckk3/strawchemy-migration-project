#!/usr/bin/env python3
"""
Generate GraphQL schema SDL files from the strawberry-sqlalchemy-mapper project.

This script exports all GraphQL schemas defined in the strawberry-sqlalchemy-project
to .graphql files containing the Schema Definition Language (SDL).

Usage:
    This script is designed to be run via the main generate_schemas.py orchestrator,
    but can also be run standalone:

        cd strawberry-sqlalchemy-project
        uv run python ../utils/generate_strawberry_sqlalchemy_mapper.py <output_dir>

Example:
    uv run python ../utils/generate_strawberry_sqlalchemy_mapper.py ../schemas/strawberry-sqlalchemy-mapper
"""

import argparse
import importlib
import sys
from dataclasses import dataclass
from pathlib import Path

# Add current working directory to Python path so we can import the schema modules
sys.path.insert(0, str(Path.cwd()))

from strawberry.printer import print_schema


# =============================================================================
# Configuration
# =============================================================================


@dataclass
class SchemaConfig:
    """Configuration for a single schema to export.

    Attributes:
        module_name: The Python module containing the schema (e.g., "schema")
        schema_attribute: The name of the schema variable in the module (e.g., "schema")
        output_filename: The filename for the exported SDL (e.g., "main.graphql")
        description: Human-readable description of what this schema demonstrates
    """

    module_name: str
    schema_attribute: str
    output_filename: str
    description: str


# List of all schemas to export from this project
SCHEMAS_TO_EXPORT = [
    SchemaConfig(
        module_name="schema",
        schema_attribute="schema",
        output_filename="main.graphql",
        description="Main schema with basic Employee and Department types",
    ),
    SchemaConfig(
        module_name="schema_relay",
        schema_attribute="schema_with_relay",
        output_filename="relay.graphql",
        description="Schema demonstrating Relay-style cursor pagination (EXCLUSIVE FEATURE)",
    ),
    SchemaConfig(
        module_name="schema_polymorphic",
        schema_attribute="schema_with_polymorphic",
        output_filename="polymorphic.graphql",
        description="Schema demonstrating polymorphic type hierarchies (EXCLUSIVE FEATURE)",
    ),
]


# =============================================================================
# Functions
# =============================================================================


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments with output_dir as a Path object
    """
    parser = argparse.ArgumentParser(
        description="Generate GraphQL SDL files from strawberry-sqlalchemy-mapper schemas",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python generate_strawberry_sqlalchemy_mapper.py ../schemas/strawberry-sqlalchemy-mapper
        """,
    )
    parser.add_argument(
        "output_dir",
        type=Path,
        help="Directory where the .graphql files will be written",
    )
    return parser.parse_args()


def load_schema(config: SchemaConfig):
    """Load a Strawberry schema from a Python module.

    Args:
        config: Configuration specifying which module and attribute to load

    Returns:
        The Strawberry schema object

    Raises:
        ImportError: If the module cannot be imported
        AttributeError: If the schema attribute doesn't exist in the module
    """
    module = importlib.import_module(config.module_name)
    schema = getattr(module, config.schema_attribute)
    return schema


def export_schema_to_file(schema, output_path: Path) -> None:
    """Export a Strawberry schema to a .graphql file.

    Args:
        schema: The Strawberry schema to export
        output_path: Path where the SDL file will be written
    """
    sdl_content = print_schema(schema)
    output_path.write_text(sdl_content)


def generate_schema(config: SchemaConfig, output_dir: Path) -> bool:
    """Generate a single schema file.

    Args:
        config: Configuration for the schema to generate
        output_dir: Directory to write the output file

    Returns:
        True if successful, False if an error occurred
    """
    output_path = output_dir / config.output_filename

    try:
        # Step 1: Load the schema from the module
        schema = load_schema(config)

        # Step 2: Export the schema to a file
        export_schema_to_file(schema, output_path)

        # Step 3: Report success
        print(f"  Generated: {config.output_filename}")
        print(f"             ({config.description})")
        return True

    except Exception as error:
        print(f"  Error generating {config.output_filename}: {error}")
        return False


def generate_all_schemas(output_dir: Path) -> bool:
    """Generate all configured schema files.

    Args:
        output_dir: Directory to write the output files

    Returns:
        True if all schemas generated successfully, False otherwise
    """
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate each schema
    all_successful = True
    for config in SCHEMAS_TO_EXPORT:
        success = generate_schema(config, output_dir)
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
    args = parse_arguments()
    success = generate_all_schemas(args.output_dir)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
