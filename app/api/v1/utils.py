"""
    This File is used for common method and classes used on aother methods
"""

from fastapi import HTTPException, status
from datetime import datetime
from typing import Dict

def file_exists(path: str) -> bool:
    try:
        with open(path) as f:
            return True
    except:
        return False

def check_file_id_exists(file_id: str) -> str:
    """
        Check file exists on file path, if not raise error, if yes, return route
    """
    # Found file
    csv_route = "files/%s.csv" % (file_id)
    if not file_exists(csv_route):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={"Error": "File not exists or has been deleted"})
    return csv_route

def convert_python_types_to_string(csv_types: Dict[str, type]) -> Dict[str, str]:
    """
    Converts a dictionary of Python types to their corresponding string representations
    used in CSV type inference.

    Args:
        csv_types (Dict[str, type]): A dictionary where keys are column names and 
                                     values are Python types (e.g., int, float, datetime).

    Returns:
        Dict[str, str]: A new dictionary with the same keys but with type values converted 
                        to strings: "integer", "float", "datetime", or "text".
    """
    for key, py_type in csv_types.items():
        if py_type == datetime:
            csv_types[key] = "datetime"
        elif py_type == str or py_type == None:
            csv_types[key] = "text"
    
    return csv_types
