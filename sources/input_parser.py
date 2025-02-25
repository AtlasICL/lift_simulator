import json

def parse_config(file_path: str) -> dict:
    """
    Reads configuration from a JSON file and returns a dictionary.

    This function verifies the following conditions:
        - total_floors >= 2, because a lift in a building with 1 floor (or fewer) does not make sense
        - capacity >= 1, because a lift which cannot hold at least 1 person does not make sense
        - num_requests >= 0, because we cannot have a negative number of requests
    
    If the user fails to provide any keys, they will be replaced by the following defaults:
        total_floors: 10
        capacity: 4
        num_requests: 30
    """

    defaults = {
        "total_floors": 10,
        "capacity": 4,
        "num_requests": 30
    }
    
    try:
        with open(file_path, 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error reading configuration: {e}")
    
    for key, default_value in defaults.items():
        if key not in config:
            config[key] = default_value
    
    if not isinstance(config["total_floors"], int) or config["total_floors"] < 2:
        raise ValueError("total_floors must be an integer >= 2. We cannot have a building with 1 floor!")
    if not isinstance(config["capacity"], int) or config["capacity"] < 1:
        raise ValueError("Capacity must be an int > 0 (cannot have a lift with 0 capacity)")
    if not isinstance(config["num_requests"], int) or config["num_requests"] < 0:
        raise ValueError("num_requests must be a positive integer!")
    
    return config
