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
    if all_plugins:
        folders = Path(path).glob("*")
        folder_names = [x.name for x in folders if x.is_dir()]
        for folder in folder_names:
            print(path + folder)
            plugin = PluginStructure(f"{path}/{folder}")
            plugin.validate()
    else:
        plugin = PluginStructure(path)
        plugin.validate()


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
            plugin = PluginStructure(f"{path}/{folder}")
            plugin.validate()
            plugin.local_install(rd_plugins)
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
def api_install(path, all_plugins):
    """Install plugin from a given path via Rundeck API"""
    if all_plugins:
        folders = Path(path).glob("*")
        folder_names = [x.name for x in folders if x.is_dir()]
        for folder in folder_names:
            print(path + folder)
            plugin = PluginStructure(f"{path}/{folder}")
            plugin.validate()
            plugin.api_install()
    else:
        plugin = PluginStructure(path)
        plugin.validate()
        plugin.api_install()


cli.add_command(validate)
cli.add_command(api_install)
cli.add_command(local_install)
