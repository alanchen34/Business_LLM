"""
Unified data processing pipeline for review analysis.
Combines data loading, cleaning, and stratified sampling in one place.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from utils.helpers.data_loader import load_and_clean_reviews
from utils.helpers.sampling import add_length_info, stratified_sample_by_month_and_bin
from utils.helpers.summary import validate_review_data, get_data_summary


class ReviewDataPipeline:
    """
    Unified pipeline for processing review data with consistent sampling.
    """
    
    def __init__(self, 
                 target_year: int = 2012,
                 target_samples: int = 400,
                 random_seed: int = 42):
        """
        Initialize the pipeline with processing parameters.
        
        Args:
            target_year (int): Year to filter data to
            target_samples (int): Number of samples to extract per category
            random_seed (int): Random seed for reproducible sampling
        """
        self.target_year = target_year
        self.target_samples = target_samples
        self.random_seed = random_seed
        
        # Standardized length bins (4 bins for consistency)
        self.length_bins = [0, 50, 200, 500, float("inf")]
        self.length_labels = ["short", "medium", "long", "extra_long"]
    
    def process_category(self, 
                        data_path: str, 
                        category_name: str,
                        output_path: Optional[str] = None) -> pd.DataFrame:
        """
        Process a single category of review data.
        
        Args:
            data_path (str): Path to the TSV file
            category_name (str): Name of the category (for logging)
            output_path (str, optional): Path to save the processed data
            
        Returns:
            pd.DataFrame: Processed and sampled data
        """
        print(f"\n=== Processing {category_name} ===")
        
        # Load and clean data
        df = load_and_clean_reviews(data_path)
        
        # Filter to target year
        df_year = df[df["review_date"].dt.year == self.target_year].copy()
        print(f"Found {len(df_year)} reviews from {self.target_year}")
        
        if len(df_year) == 0:
            print(f"Warning: No data found for {category_name} in {self.target_year}")
            return pd.DataFrame()
        
        # Add length information and perform stratified sampling
        df_with_length = add_length_info(df_year)
        sampled_df = stratified_sample_by_month_and_bin(
            df_with_length, 
            target_n=self.target_samples,
            seed=self.random_seed
        )
        
        print(f"Sampled {len(sampled_df)} reviews for {category_name}")
        
        # Add category information
        sampled_df["category"] = category_name
        
        # Save if output path provided
        if output_path:
            sampled_df.to_csv(output_path, index=False)
            print(f"Saved processed data to {output_path}")
        
        return sampled_df
    
    def process_all_categories(self, 
                              data_config: Dict[str, str],
                              output_dir: str = "processed_data") -> Dict[str, pd.DataFrame]:
        """
        Process all categories defined in the configuration.
        
        Args:
            data_config (Dict[str, str]): Mapping of category names to file paths
            output_dir (str): Directory to save processed files
            
        Returns:
            Dict[str, pd.DataFrame]: Processed data for each category
        """
        import os
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        results = {}
        
        for category, file_path in data_config.items():
            output_path = os.path.join(output_dir, f"{category}.csv")
            results[category] = self.process_category(file_path, category, output_path)
        
        return results
    
    def merge_all_data(self, 
                      processed_data: Dict[str, pd.DataFrame],
                      output_path: str = "final_dataset.csv") -> pd.DataFrame:
        """
        Merge all processed category data into a single dataset.
        
        Args:
            processed_data (Dict[str, pd.DataFrame]): Processed data from each category
            output_path (str): Path to save the merged data
            
        Returns:
            pd.DataFrame: Merged dataset
        """
        print(f"\n=== Merging all data ===")
        
        # Filter out empty dataframes
        valid_data = {k: v for k, v in processed_data.items() if not v.empty}
        
        if not valid_data:
            print("Warning: No valid data to merge")
            return pd.DataFrame()
        
        # Merge all data
        merged_df = pd.concat(valid_data.values(), ignore_index=True)
        
        # Shuffle the merged data
        merged_df = merged_df.sample(frac=1, random_state=self.random_seed).reset_index(drop=True)
        
        print(f"Merged {len(merged_df)} total reviews from {len(valid_data)} categories")
        
        # Save merged data
        merged_df.to_csv(output_path, index=False)
        print(f"Saved merged data to {output_path}")
        
        return merged_df
    
    def get_processing_summary(self, processed_data: Dict[str, pd.DataFrame]) -> Dict:
        """
        Get a summary of the processing results.
        
        Args:
            processed_data (Dict[str, pd.DataFrame]): Processed data from each category
            
        Returns:
            Dict: Summary statistics
        """
        summary = {
            "categories_processed": len(processed_data),
            "total_reviews": sum(len(df) for df in processed_data.values()),
            "category_breakdown": {}
        }
        
        for category, df in processed_data.items():
            if not df.empty:
                summary["category_breakdown"][category] = {
                    "review_count": len(df),
                    "length_distribution": df["length_bin"].value_counts().to_dict(),
                    "rating_distribution": df["star_rating"].value_counts().sort_index().to_dict()
                }
        
        return summary


def create_sample_pipeline():
    """
    Create a sample pipeline with default configuration.
    """
    return ReviewDataPipeline(
        target_year=2012,
        target_samples=400,
        random_seed=42
    )
