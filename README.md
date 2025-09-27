# IEOR 4573 Capstone Project

Analyze unstructured customer reviews with LLMs. Perform sentiment classification and aspect-based extraction (e.g., shipping, pricing, quality, support) to surface strengths and pain points. Summarize insights and visualize trends in an interactive dashboard for actionable business decisions.

## Prerequisites

- Download Amazon customer review datasets and store them in `./data/` directory
    - [Ebook](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Ebook_Purchase_v1_01.tsv)
    - [Music](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Music_Purchase_v1_00.tsv)
    - [Software](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Software_v1_00.tsv)
    - [Videos](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Video_Download_v1_00.tsv)
    - [Video Games](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Video_Games_v1_00.tsv)
- Install necessary Python packages 

```
pip install -r requirements.txt
```