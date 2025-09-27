import csv
import pandas as pd
import os
from typing import Optional, Dict, Any
from .summary import validate_review_data

def load_and_clean_reviews(path: str, validate: bool = True) -> pd.DataFrame:
    """
    Load and clean a reviews dataset from a TSV file.

    Args:
        path (str): Path to the .tsv file.
        validate (bool): Whether to perform basic data validation.

    Returns:
        pd.DataFrame: Cleaned DataFrame with correct dtypes.
        
    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If data validation fails.
    """
    
    # Check if file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    USE_COLS = [
        "marketplace","customer_id","review_id","product_id","product_parent",
        "product_title","product_category","star_rating","helpful_votes",
        "total_votes","vine","verified_purchase","review_headline",
        "review_body","review_date"
    ]

    try:
        # --- Load ---
        df = pd.read_csv(
            path, sep="\t", usecols=USE_COLS,
            dtype=str, engine="python",
            quoting=csv.QUOTE_NONE,  # treat " as normal character
            escapechar="\\",         # allow \" if it exists
        )
        
        print(f"Loaded {len(df)} reviews from {path}")
        
    except Exception as e:
        raise ValueError(f"Error loading file {path}: {str(e)}")

    # --- Clean up line-separator characters ---
    df = df.replace({u"\u2028": " ", u"\u2029": " "}, regex=True)

    # --- Convert column types ---
    try:
        df = df.astype({
            "customer_id": "int64",
            "product_parent": "int64",
            "star_rating": "int8",
            "helpful_votes": "int32",
            "total_votes": "int32"
        })
    except Exception as e:
        print(f"Warning: Error converting column types: {e}")

    # --- Boolean-like (Y/N) to bool ---
    df["vine"] = df["vine"].map({"Y": True, "N": False})
    df["verified_purchase"] = df["verified_purchase"].map({"Y": True, "N": False})

    # --- Dates ---
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
    
    # --- Basic validation ---
    if validate:
        validation_results = validate_review_data(df)
        if not validation_results["is_valid"]:
            print("Data validation warnings:")
            for warning in validation_results["warnings"]:
                print(f"  - {warning}")
    
    return df


