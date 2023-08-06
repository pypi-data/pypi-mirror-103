"""Class for python plugin and files structure"""

import sys
import logging
import zipfile
import tempfile
from pathlib import Path

logger = logging.getLogger(__name__)


class PluginStructure:
    """Class for Rundeck python plugin folder structure"""

    def __init__(self, path: str):
        self.path = Path(path).resolve()
        self.root = self.path.parent
        self.plugin = self.path.relative_to(self.root)
        self.name = self.path.name
        self.root_required_files = ["plugin.yaml", "README.md"]

    def __repr__(self):
        return repr(self.name)

    @staticmethod
    def _is_folder(path):
        """Exits is path is not a folder"""
        if not path.is_dir():
            sys.exit("Paramether provided is not a folder.\n")
        print(f"Path provided {path} is a folder.")

    @staticmethod
    def _has_required_files(path, required_files: list):
        """Exits if required file is missing from file list"""
        items_names = [x.name for x in path.iterdir()]
        if not set(required_files).issubset(items_names):
            print(f"  Folder: {path}")
            print(f"  Items: {items_names}")
            print(f"  Required Items: {required_files}")
            sys.exit("  Folder provided does not contain all required files.")
        print(f"Folder {path} contains all required files: {required_files}")

    @staticmethod
    def _folder_has_contents_folder(path):
        """Exits if folder does not have contents folder."""
        folders = [x.name for x in path.iterdir() if x.is_dir()]
        if "contents" not in folders:
            sys.exit(
                f"{path} does not contain subfolder 'contents'. It contains {folders}"
            )
        print(f"Folder {path} contains subfolder named 'contents'.")

    def validate(self):
        """Exits if folder does not have all files required to build a plugin"""
        self._is_folder(self.path)
        self._has_required_files(self.path, self.root_required_files)
        self._folder_has_contents_folder(self.path)
        # WIP
        # Add resources folder to validation
        # Validate if contents folder has file
        # Validate if YAML is ok
        # Validate if script described in YAML is in contents folder
        # Change zip to only include necessary items (ignore readme, tests)
        # Run plugin tests
        print("Valid plugin.\n")

    @staticmethod
    def _move_file_local(path, destination):
        """Moves file in path to destination"""
        print(path, destination)

    @staticmethod
    def _move_file_remote(path, destination, server, username, password):
        """Moves file in path to destination"""
        print(path, destination, server, username, password)

    def local_install(self, destination):
        """Makes the plugin and moves to Rundeck plugin folder"""
        print(f" Compressing {self.path}")
        # WIP
        # Add install plugin requirements if it exists.
        with tempfile.TemporaryDirectory() as tmpdir:
            zip_file_name = self.name + ".zip"
            zip_file_path = tmpdir + "/" + zip_file_name
            zip_file = zipfile.ZipFile(zip_file_path, "w")
            with zip_file:
                for item in self.path.rglob("*"):
                    print(f"  {item.relative_to(self.root)}")
                    zip_file.write(item, item.relative_to(self.root))
            print(f" Zip file created {zip_file.filename}")
            zip_file = Path(zip_file.filename)
            zip_file.replace(f"{destination}/{zip_file.name}")
            print(f" Moved {zip_file_name} to {destination}")

    def remote_install(self, destination, server, username, password):
        """Makes the plugin and moves to Rundeck plugin folder"""
        print(f"need to install {self.path} in:")
        print(f" {destination} {server} {username} {password[0-2]}")

    def create(self):
        """Creates a folder with all required files and folders for a valid plugin"""
        print(f"need to create{self.path}\n")
