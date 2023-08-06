"""Rundeckpy CLI."""
import logging
from pathlib import Path
import click
from .rd_plugin import PluginStructure

logger = logging.getLogger(__name__)


@click.group()
def cli():
    """RundeckPy version 0.2  """


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--all",
    "all_plugins",
    is_flag=True,
    help="Path is a folder with multiple plugin folders. Validate all.",
)
def validate(path, all_plugins):
    """Validate plugin in a given path"""
    print("Plugin Validation:\n")
    if all_plugins:
        folders = Path(path).glob("*")
        folder_names = [x.name for x in folders if x.is_dir()]
        for folder in folder_names:
            print(folder)
            try:
                plugin = PluginStructure(f"{path}/{folder}")
                plugin.validate()
            except SystemExit as error:
                print(error)
            print("")
    else:
        plugin = PluginStructure(path)
        plugin.validate()
    print("")


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--all",
    "all_plugins",
    is_flag=True,
    help="Path is a folder with multiple plugin folders. Install all.",
)
@click.option(
    "--libext-path",
    "libext_path",
    default="",
    help="Path for Rundeck plugins folder libext (including /libext)",
)
def local_install(path, all_plugins, libext_path):
    """Install plugin from a given path via local file system"""
    rd_plugins = Path("/home/rundeck/libext")
    if Path("/var/lib/rundeck/libext").is_dir():
        rd_plugins = Path("/var/lib/rundeck/libext")
    if libext_path:
        rd_plugins = Path(libext_path)
    if all_plugins:
        folders = Path(path).glob("*")
        folder_names = [x.name for x in folders if x.is_dir()]
        for folder in folder_names:
            print(path + folder)
            try:
                plugin = PluginStructure(f"{path}/{folder}")
                plugin.validate()
                plugin.local_install(rd_plugins)
            except SystemExit as error:
                print(error)
    else:
        plugin = PluginStructure(path)
        plugin.validate()
        plugin.local_install(rd_plugins)


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "--all",
    "all_plugins",
    is_flag=True,
    help="Path is a folder with multiple plugin folders. Install all.",
)
def remote_install(path, all_plugins):
    """Install plugin from a given path in a remote server"""
    if all_plugins:
        folders = Path(path).glob("*")
        folder_names = [x.name for x in folders if x.is_dir()]
        for folder in folder_names:
            print(path + folder)
            try:
                plugin = PluginStructure(f"{path}/{folder}")
                plugin.validate()
                plugin.remote_install("destination", "server", "username", "password")
            except SystemExit as error:
                print(error)
    else:
        plugin = PluginStructure(path)
        plugin.validate()
        plugin.remote_install("destination", "server", "username", "password")


cli.add_command(validate)
cli.add_command(local_install)
cli.add_command(remote_install)
