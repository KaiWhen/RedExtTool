import json
import time


def save_curr_igt(filepath, data, retries=3, delay=0.05):
    """Save current IGT data with retry logic to handle file locking"""
    for attempt in range(retries):
        try:
            with open(filepath, 'w') as file:
                json.dump(data, file)
            return
        except PermissionError:
            if attempt < retries - 1:
                time.sleep(delay)
            else:
                print(f"Failed to save {filepath} after {retries} attempts")
                raise
