"""Class for python plugin and files structure"""

import sys
import logging
import shutil
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class PluginStructure:
    """Class for Rundeck python plugin folder structure"""

    def __init__(self, path: str):
        self.name = ""
        self.path = Path(path)
        self.root_required_files = ["plugin.yaml", "README.md"]

    def __repr__(self):
        return repr(self.name)

    @staticmethod
    def _is_folder(path):
        """Confirm path is a folder"""
        if not path.is_dir():
            sys.exit("Paramether provided is not a folder.\n")
        print(f"Path provided {path} is a folder.")

    @staticmethod
    def _has_required_files(path, required_files: list):
        """Exits if required file is missing from file list"""
        root = path.glob("*")
        items_names = [x.name for x in root]
        if not set(required_files).issubset(items_names):
            print(f"  Folder: {path}")
            print(f"  Items: {items_names}")
            print(f"  Required Items: {required_files}")
            sys.exit("  Folder provided does not contain all required files.")
        print(f"Folder {path} contains all required files: {required_files}")

    @staticmethod
    def _folder_has_contents_folder(path):
        """Exits if folder does not have contents folder."""
        folders = path.glob("*")
        folder_names = [x.name for x in folders if x.is_dir()]
        if "contents" not in folder_names:
            print(folder_names)
            sys.exit(
                f"{path} does not contain subfolder 'contents'. It contains {folder_names}"
            )
        print(f"Folder {path} contains subfolder is named 'contents'.")

    def validate(self):
        """Exits if folder does not have all files required to build a plugin"""
        self._is_folder(self.path)
        self._has_required_files(self.path, self.root_required_files)
        self._folder_has_contents_folder(self.path)
        print("Valid plugin.\n")

    def local_install(self, destination):
        """Makes the plugin and moves to Rundeck plugin folder"""
        print(f" Compressing {self.path}")
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_file_name = shutil.make_archive(
                f"{tmpdir}/{self.path.name}", "zip", self.path
            )
            print(f" Zip file created {zip_file_name}")
            zip_file = Path(zip_file_name)
            zip_file.replace(f"{destination}/{zip_file.name}")
            print(f" Moved {zip_file_name} to {destination}")

    def api_install(self):
        """Makes the plugin and moves to Rundeck plugin folder"""
        print(f"need to install {self.path} \n")

    def create(self):
        """Creates a folder with all required files and folders for a valid plugin"""
        print(f"need to create{self.path}\n")
