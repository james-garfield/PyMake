import yaml
import subprocess
from . import utils


class PyMake:
    command = ""
    debug_mode = False
    config:dict = {}

    def __init__(self, config_file="config.yaml", debug_mode=False):
        self.debug_mode = debug_mode
        self.load_config(config_file)

    def load_config(self, config_file):
        if not config_file.endswith(".yaml"):
            utils.debug_print("Config file must be a .yaml file", self.debug_mode)
            exit(1)

        # Check file exists
        if not utils.file_exists(config_file):
            utils.debug_print(f"File {config_file} does not exist", self.debug_mode)
            exit(1)

        with open(config_file, 'r') as f:
            self.config = yaml.safe_load(f)

    def add_flags(self, flag, arguments, add_slash=True, add_dash=True):
        """
        Add flags to the command.

        Args:
        - flag (str): The flag to add to the command.
        - arguments (list): A list of arguments to add to the command.
        - add_slash (bool): Whether to add a slash after each argument.
        """
        dash = "-" if add_dash else ""
        # Add flags
        for arg in arguments:
            self.command += f' {dash}{flag}{arg}'
            if add_slash:
                self.command += " / \n"
            elif arguments[-1] == arg:
                    break

    def build(self):
        if self.config == {}:
            utils.debug_print("Config is empty", self.debug_mode)
            exit(2)
        
        self.command = f"{self.config['compiler']} -o {self.config['output']} "

        utils.debug_print("Building " + self.config["name"], self.debug_mode)
        actions_in_order = [
            "files",
            "includes",
            "libs",
            "libraries",
            "flags",
        ]
        actions = {
            "compiler": lambda x: f'{x}',
            "files": lambda x: self.add_flags("", x, add_dash=False),
            "includes": lambda x: self.add_flags("I", x),
            "libs": lambda x: self.add_flags("L", x),
            "libraries": lambda x: self.add_flags("l", x),
            "flags": lambda x: self.add_flags("", x, add_slash=False),
        }

        # Apply transformations
        for action in actions_in_order:
            if action in self.config:
                actions[action](self.config[action])

        # Print command
        print(self.command)
        # Remove pretty print
        self.command = self.command.replace("/ \n", " ")
        # Call command and check if command has output
        # If it does, it failed
        res = subprocess.call(self.command, shell=True)
        if res != 0:
            utils.debug_print("Build failed", self.debug_mode)
            exit(3)
        
        # Build succeeded
        utils.debug_print("Build succeeded", self.debug_mode)

    def run(self):
        utils.debug_print("Running program", self.debug_mode)
        # Run program
        build = self.config['output'].replace("/", "\\")
        subprocess.call(build, shell=True)

    def run_shell_commands(self, which:str):
        # This is to run shell commands separately from building
        utils.debug_print("Running shell commands", self.debug_mode)
        if not "shell" in self.config:
            utils.debug_print("No shell in config", self.debug_mode)
            return
        
        shells_to_run = []
        shells: dict = self.config['shell']

        match which:
            case 'all':
                shells_to_run.append(shells.get('before', []))
                shells_to_run.append(shells.get('after', []))
                shells_to_run.append(shells.get('misc', []))
            case 'before':
                shells_to_run.append(shells.get('before', []))
            case 'after':
                shells_to_run.append(shells.get('after', []))
            case 'seq':
                shells_to_run.append(shells.get('before', []))
                shells_to_run.append(shells.get('after', []))
            case 'misc':
                shells_to_run.append(shells.get('misc', []))
            case _:
                utils.debug_print(f"Which: {which} is not a valid option for shell", self.debug_mode)
                return

        self.run_shell(shells_to_run)

    def run_shell(self, shells):
        for shell in shells:
            utils.debug_print(shell, self.debug_mode)
            subprocess.call(shell, shell=True)
    
    def build_with_shell(self):
        # Run the before shell commands
        # run build
        # Run the after shell commands
        shells = self.config.get("shell", [])
        before = shells.get("before", [])
        after = shells.get("after", [])

        # Run before shell commands
        self.run_shell(before)
        # Build
        self.build()
        # Run after shell commands
        self.run_shell(after)