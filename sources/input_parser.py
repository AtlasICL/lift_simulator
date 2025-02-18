import json

# TODO: add default values for the variables if they are not provided in config.json? 

# TODO: MAKE SURE PROVIDED VALUES ARE >0 AND >1 

def parse_config(file_path: str) -> dict:
    """
    This function reads the configuration from the config.json file
    and returns a dictionary with the provided details (how many floors, etc)
    """
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error reading configuration: {e}") # verify provided json is valid

    # Validate required keys
    required_keys = ["total_floors", "capacity", "num_requests"] # categories to be provided in config.json
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required configuration key in config.json: {key}")

    return config # returns the dictionary with the provided config
