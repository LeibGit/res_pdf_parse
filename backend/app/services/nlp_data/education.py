import pandas as pd
import re
import os
from dotenv import load_dotenv

load_dotenv()

list_of_universities = []
_initialized = False

def get_universities():
    """
    Get list of universities from CSV file.
    Returns empty list if file not found or environment variable not set.
    """
    global list_of_universities, _initialized
    
    # Only load once
    if _initialized:
        return list_of_universities
    
    csv_path = os.getenv("COLLEGE_DOWNLOAD")
    
    # If no path provided, return empty list (graceful degradation)
    if not csv_path:
        _initialized = True
        return list_of_universities
    
    try:
        # Check if file exists
        if not os.path.exists(csv_path):
            _initialized = True
            return list_of_universities
        
        # Read CSV file
        df = pd.read_csv(csv_path, quotechar='"', engine='python', sep=None)
        
        if "NAME" in df.columns:
            uni_names = df["NAME"]
            for name in uni_names:
                list_of_universities.append(str(name))
        
        _initialized = True
    except Exception as e:
        # If any error occurs, return empty list (don't crash the app)
        _initialized = True
        pass
    
    return list_of_universities