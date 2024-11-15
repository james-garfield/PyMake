import yaml
from jinja2 import Template

# Jinja2 template for the YAML configuration
yaml_template = """
# This handles building the project

compiler: {{ compiler | default("gcc") }} # Change to whatever will compile your c/c++ code. You can even use emscripten!
name: {{ app_name | default("App name") }} # The name of the project, used for debugging.
output: {{ output | default("app.exe") }} # The output file.

# These are the flags that will be passed to the compiler, such as -std=c++17
{% if flags|length > 0 %}
flags: 
{% for flag in flags %}
    - {{ flag }}
{% endfor %}
{%else%}
#flags:
#  - std=c++17
{%endif%}

# The c/c++ files that will be compiled in order. 
{% if files|length > 0 %}
files: 
{% for file in files %}
    - {{ file }}
{% endfor %}
{%else%}
#files:
#  - main.cpp
{%endif%}

# Where are the header files located?
{% if includes|length > 0 %}
includes:
{% for include in includes %}
    - {{ include }}
{% endfor %}
{%else%}
#includes:
#  - includes/
{%endif%}

# Not to be confused with libraries, these are the paths to the libraries.
{%if libs|length > 0%}
libs:
{% for lib in libs %}
    - {{ lib }}
{% endfor %}
{%else%}
#libs:
#  - path/to/lib
{%endif%}

# These are the libraries that will be linked to the project. Path must be specified in libs.
{% if libraries|length > 0 %}
libraries: 
{% for library in libraries %}
    - {{ library }}
{% endfor %}
{%else%}
#libraries:
#  - libname
{%endif%}

# Shell commands to run before or after building.
shell:
  {% if shell.before|length > 0 %}
  before:
  {% for cmd in shell.before %}
    - {{ cmd }}
  {% endfor %}
  {%else%}
  #before:
  #  - echo hello world
  {%endif%}
  {% if shell.after|length > 0 %}
  after:
  {% for cmd in shell.after %}
    - {{ cmd }}
  {% endfor %}
  {%else%}
  #after:
  #  - echo bye world
  {%endif%}
  {% if shell.misc|length > 0 %}
  misc:
  {% for cmd in shell.misc %}
    - {{ cmd }}
  {% endfor %}
  {%else%}
  #misc:
  #  - echo misc call
  {%endif%}
"""


def render_template_to_file(data, output_file):
    """
    Renders a Jinja2 template with the given data and writes the output to a file.

    :param template_str: The Jinja2 template as a string.
    :param data: A dictionary containing data to fill the template.
    :param output_file: The path to the output file where the rendered template will be written.
    """
    data["flags"] = data.get("flags", [])
    data["files"] = data.get("files", [])
    data["includes"] = data.get("includes", [])
    data["libs"] = data.get("libs", [])
    data["libraries"] = data.get("libraries", [])
    data["shell"] = data.get("shell", {
        'before': [],
        'after': [],
        'misc': []
    })
    template = Template(yaml_template)
    rendered_content = template.render(data)

    with open(output_file, 'w') as f:
        f.write(rendered_content)


def update_yaml_config(config_file, new_data, new_name):
    """
    Updates a YAML configuration file with new data and re-renders the Jinja2 template.

    :param config_file: Path to the YAML configuration file.
    :param new_data: Dictionary containing new data to update the configuration.
    """
    # Load existing YAML data
    with open(config_file, 'r') as f:
        existing_data = yaml.safe_load(f)

    # Update the existing data with new values
    for key, value in new_data.items():
        existing_data[key] = value

    file_path = config_file if new_name == None else new_name

    # Render the updated configuration using the template
    render_template_to_file(existing_data, file_path)
