import os
import click
import sys

from .pymake import PyMake
from . import build_file
from . import utils

@click.command()
@click.option('-c', '--config_file', is_flag=True, default="pymk.yaml")
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
def init(config_file, debug):
    # Check that it is a existing path
    if os.path.exists(config_file):
        utils.debug_print(f"Config file {config_file} already exists", debug)
        exit(3)
    # Build the default config
    build_file.render_template_to_file({}, config_file)
    utils.debug_print(f"Created config file {config_file}", debug)


@click.command()
@click.option('-c', '--config_file', is_flag=True, default="pymk.yaml")
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
@click.option('-c', '--config_file', is_flag=True, default="pymk.yaml")
@click.argument('config_file', required=False, default="pymk.yaml")
@click.option('-d', '--debug', is_flag=True, help="Enable debug mode")
def aigenerate(entry, config_file, debug):
    # generate the yaml file for a pymk project
    pymake = PyMake(config_file, debug)
    pymake.ai_generate(entry)
    

@click.command()
@click.option('-c', '--config_file', default="pymk.yaml")
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode.')
@click.option('-b', '--build', is_flag=True, default=False, help='Build with pymk before running.')
@click.option('-p', '--arguments', default="", help="Tell the pymk linker to parse the script arguments.")
def run(config_file, debug, build, arguments):
    # Run a c/c++ project
    pymake = PyMake(config_file, debug)

    # Get script arguments after run's
    print(arguments)
    # arguments = sys.argv[]

    pymake.run()


@click.command()
@click.option('-c', '--config_file', is_flag=True, default="pymk.yaml")
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
@click.option('-c', '--config_file', is_flag=True, default="pymk.yaml")
@click.argument('which', required=False, default='all')
@click.option('-d', '--debug', is_flag=True, help='Enable debug mode')
def shell(config_file, which, debug):
    pymake = PyMake(config_file, debug)
    pymake.run_shell_commands(which)


@click.command()
def version():
    print('0.1.8')


@click.group()
def cli():
    pass

cli.add_command(init)
cli.add_command(build)
cli.add_command(run)
cli.add_command(update)
cli.add_command(shell)
cli.add_command(version)
cli.add_command(aigenerate)


if __name__ == "__main__":
    cli()