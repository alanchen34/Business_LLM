"""
Data validation and summary utilities for review analysis.
"""

import pandas as pd
from typing import Dict, Any


def validate_review_data(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform basic validation on review data.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        
    Returns:
        Dict containing validation results and warnings
    """
    warnings = []
    
    # Check for empty reviews
    empty_reviews = df["review_body"].isna().sum()
    if empty_reviews > 0:
        warnings.append(f"{empty_reviews} reviews have empty review_body")
    
    # Check for very short reviews
    if "review_body" in df.columns:
        short_reviews = (df["review_body"].str.len() < 10).sum()
        if short_reviews > 0:
            warnings.append(f"{short_reviews} reviews are very short (< 10 characters)")
    
    # Check for invalid star ratings
    invalid_ratings = ~df["star_rating"].between(1, 5)
    if invalid_ratings.sum() > 0:
        warnings.append(f"{invalid_ratings.sum()} reviews have invalid star ratings")
    
    # Check for missing dates
    missing_dates = df["review_date"].isna().sum()
    if missing_dates > 0:
        warnings.append(f"{missing_dates} reviews have missing dates")
    
    return {
        "is_valid": len(warnings) == 0,
        "warnings": warnings,
        "total_reviews": len(df)
    }


def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get a summary of the loaded data.
    
    Args:
        df (pd.DataFrame): DataFrame to summarize
        
    Returns:
        Dict containing data summary
    """
    return {
        "total_reviews": len(df),
        "date_range": {
            "earliest": df["review_date"].min(),
            "latest": df["review_date"].max()
        },
        "rating_distribution": df["star_rating"].value_counts().sort_index().to_dict(),
        "categories": df["product_category"].value_counts().to_dict(),
        "verified_purchase_rate": df["verified_purchase"].mean()
    }
