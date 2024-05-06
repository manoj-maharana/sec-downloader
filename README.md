# SEC Filing Downloader and Converter

This Python script downloads SEC filings using the `sec_edgar_downloader` library and converts them to PDFs using `pdfkit`. It also utilizes `tqdm` for progress bars and `fire` for command-line interface management.

## Requirements

- Python 3.6 or higher
- sec_edgar_downloader
- wkhtmltopdf (https://wkhtmltopdf.org/)
- pdfkit
- tqdm
- fire

## Installation

1. Clone the repository to your local machine:

 git clone https://github.com/yourusername/sec-filing-downloader.git 
Install the required Python packages using pip:pip install sec_edgar_downloader pdfkit tqdm fire
## Usage
bash cd sec-filing-downloader
python main.py [options]

# Options:

--output_dir: Output directory for files.

--ciks: List of CIKs (Central Index Keys) for companies.

--file_types: Types of filings to download (e.g., 10-K, 10-Q).

--before: Date before which filings should be downloaded (YYYY-MM-DD).

--after: Date after which filings should be downloaded (YYYY-MM-DD).

--limit: Limit number of filings to download.

Example usage:
``` bash
python main.py --output_dir data/output --ciks AAPL GOOGL --file_types 10-K 10-Q --before 2023-01-01 --after 2018-01-01 --limit 50

