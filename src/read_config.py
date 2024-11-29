import yaml
# This reads a YAML file and parses it into a Python dictionary.
# The top level keys correspond to the sections in the YAML file.
# For this, you need to 'pip install pyyaml' if you haven't already done so.

def read_config(file_path):
    with open(file_path, 'r') as file:
        settings = yaml.safe_load(file)
    return settings

if __name__ == "__main__":
    config_file = 'config.yaml'  # Replace with the path to your config file
    settings = read_config(config_file)
    print(settings)  # This will print the settings as a dictionary

