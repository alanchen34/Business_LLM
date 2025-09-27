# IEOR 4573 Capstone Project

Analyze unstructured customer reviews with LLMs. Perform sentiment classification and aspect-based extraction (e.g., shipping, pricing, quality, support) to surface strengths and pain points. Summarize insights and visualize trends in an interactive dashboard for actionable business decisions.

## Prerequisites

Download Amazon customer review datasets and store them in `./data/` directory
  - [Ebook](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Ebook_Purchase_v1_01.tsv)
  - [Music](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Music_Purchase_v1_00.tsv)
  - [Software](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Software_v1_00.tsv)
  - [Videos](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Video_Download_v1_00.tsv)
  - [Video Games](https://www.kaggle.com/datasets/cynthiarempel/amazon-us-customer-reviews-dataset/data?select=amazon_reviews_us_Digital_Video_Games_v1_00.tsv)

## Installation

1. (Optional) Create and activate a virtual environment:
	```powershell
	python -m venv .venv
	.\.venv\Scripts\activate
	```

2. Install all required packages:
	```powershell
	pip install -r requirements.txt
	```
3. Set your OpenAI API key (do NOT share this key or commit it to the repo):

	 - **Option 1: Environment variable (recommended)**
		 - In PowerShell:
			 ```powershell
			 $env:OPENAI_API_KEY = "your-api-key-here"
			 ```
		 - In bash:
			 ```bash
			 export OPENAI_API_KEY="your-api-key-here"
			 ```

	 - **Option 2: .env file**
		 - Copy `.env.example` to `.env` and add your key:
			 ```
			 cp .env.example .env
			 # Then edit .env and set your key
			 ```

Each user should use their own API key from the OpenAI dashboard. Never commit your real key to the repository.
