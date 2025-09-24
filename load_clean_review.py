import csv
import pandas as pd

def load_and_clean_reviews(path: str) -> pd.DataFrame:
    """
    Load and clean a reviews dataset from a TSV file.

    Args:
        path (str): Path to the .tsv file.

    Returns:
        pd.DataFrame: Cleaned DataFrame with correct dtypes.
    """

    USE_COLS = [
        "marketplace","customer_id","review_id","product_id","product_parent",
        "product_title","product_category","star_rating","helpful_votes",
        "total_votes","vine","verified_purchase","review_headline",
        "review_body","review_date"
    ]

    # --- Load ---
    df = pd.read_csv(
        path, sep="\t", usecols=USE_COLS,
        dtype=str, engine="python",
        quoting=csv.QUOTE_NONE,  # treat " as normal character
        escapechar="\\",         # allow \" if it exists
    )

    # --- Clean up line-separator characters ---
    df = df.replace({u"\u2028": " ", u"\u2029": " "}, regex=True)

    # --- Convert column types ---
    df = df.astype({
        "customer_id": "int64",
        "product_parent": "int64",
        "star_rating": "int8",
        "helpful_votes": "int32",
        "total_votes": "int32"
    })

    # --- Boolean-like (Y/N) to bool ---
    df["vine"] = df["vine"].map({"Y": True, "N": False})
    df["verified_purchase"] = df["verified_purchase"].map({"Y": True, "N": False})

    # --- Dates ---
    df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")

    return df
