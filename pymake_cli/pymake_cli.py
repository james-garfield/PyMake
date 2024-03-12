import os
import click

from .pymake import PyMake
from . import build_file
from . import utils


@click.command()
@click.argument('config_file', required=False, default="pymk.yaml")
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
def init(config_file, debug):
    # Check that it is a existing path
    if os.path.exists(config_file):
        utils.debug_print(f"Config file {config_file} already exists", debug)
        exit(3)
    # Build the default config
    build_file.build_file(config_file)
    utils.debug_print(f"Created config file {config_file}", debug)


@click.command()
@click.argument('config_file', required=False, default="pymk.yaml")
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
@click.option('-s', '--shell', is_flag=True, help='Run shell commands before building')
def build(config_file, debug, shell):
    # Build a c/c++ project
    pymake = PyMake(config_file, debug)
    if not shell:
        pymake.build()
    else:
        pymake.build_with_shell()


@click.command()
@click.argument('config_file', required=False, default="pymk.yaml")
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
def run(config_file, debug):
    # Run a c/c++ project
    pymake = PyMake(config_file, debug)
    pymake.run()


@click.command()
@click.argument('config_file', required=False, default="pymk.yaml")
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
@click.option('-n', '--new', is_flag=True, help='Create a new config file')
def update(config_file, debug, new):
    # Update the config file
    if new:
        # Create a new config file
        utils.debug_print(f"Creating config file {config_file}", debug)
        os.remove(config_file)
        init(config_file, debug)
    else:
        # Tries it's best to reload the config file with the new structure
        utils.debug_print(f"Updating config file {config_file}", debug)
        build_file.build_file_with_data(config_file)


@click.command()
@click.argument('config_file', required=False, default="pymk.yaml")
@click.argument('which', required=False, default='all')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
def shell(config_file, which, debug):
    pymake = PyMake(config_file, debug)
    pymake.run_shell_commands(which)


@click.group()
def cli():
    pass

cli.add_command(init)
cli.add_command(build)
cli.add_command(run)
cli.add_command(update)
cli.add_command(shell)


if __name__ == "__main__":
    cli()