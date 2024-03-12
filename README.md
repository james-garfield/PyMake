# PyMakeCli

Build C/C++ projects easily using YAML and Python.

### Why did I build this?
I built this because I use C/C++ daily in my ecosystem. CMake is a complex and painful concept to learn. And the best part is, once you learned CMake and you can write quite complex build scripts, you still hate it. This is why PyMakeCli exists. PyMakeCli replaces CMake and allows you to worry about your projects code and not it's build script. PyMakeCli is cross-platform to the extent that the platform has Python >= 3.6 installed.

**Note:** This is still in development and may not work as expected.

## Installation

```bash
pip install pymake-cli
```

## Usage

```bash
pymake-cli --help
```

## Example

To use this you need to create a `.yaml` file in the root of your project.
**hint**: You can also specify the path of the `.yaml` file in each command.
**hint**: The `config_file_path` is optional and will default to `config.yaml` in the current directory.

### Init
    
```bash
pymake-cli init <config_file_path> [-d]
```

### Build
    
```bash
pymake-cli build <config_file_path> [-d] [-s]
```

### Run
```bash
pymake-cli run <config_file_path>
```

### Update
This command will update the `.yaml` file with the current config structure.
```bash
pymake-cli update <config_file_path> 
```

### Options
On each command you can specify the following options:
- `<config_file_path>`: The path to the `.yaml` file.
- `-d` or `--debug`: This will print debug information.

The `-s` or `--shell` option allows you to run shell commands as defined in the config file.
### Try it out
You can try it out by cloning this repo and running the following commands:
```bash
# Clone repo
git clone https://github.com/james-garfield/PyMakeCli.git

# Change directory
cd PyMakeCli

# Install package
pip install -e .

# Change into example directory
cd example

# Run commands
pymake-cli build
pymake-cli run
```


### Things I am working on
- [ ] Update command. The current command leaves the new config file disorganized.
- [ ] Add tests.
- [ ] Init should have specific templates you can choose from. i.e. (wasm, )
- [ ] Add a pymkenv/ folder to save C/C++ projects
    - [ ] Download into pymkenv using `pymk install`