"""
    This File is used for common method and classes used on aother methods
"""

def file_exists(path: str) -> bool:
    try:
        with open(path) as f:
            return True
    except:
        return False