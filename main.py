from pathlib import Path
from typing import List, Optional

import pdfkit
from fire import Fire
from sec_edgar_downloader import Downloader
from distutils.spawn import find_executable
from tqdm.contrib.itertools import product


DEFAULT_OUTPUT_DIR = "data/"
SEC_EDGAR_COMPANY_NAME = 'test'
SEC_EDGAR_EMAIL = 'you@example.com'
DEFAULT_CIKS = ["AAPL"]
DEFAULT_FILING_TYPES = ["10-K", "10-Q"]


def download_and_convert_filing(
        cik: str, filing_type: str, output_dir: str, limit=None, before=None, after=None
):
    """Downloads and converts SEC filings to PDFs."""
    downloader = Downloader(SEC_EDGAR_COMPANY_NAME, SEC_EDGAR_EMAIL, output_dir)
    downloader.get(filing_type, cik, limit=limit, before="2024-03-25", after="2017-01-01", download_details=True)
    convert_to_pdf(output_dir)


def convert_to_pdf(output_dir: str):
    """Converts all HTML files in a directory to PDF files."""
    data_dir = Path(output_dir) / "sec-edgar-filings"

    for cik_dir in data_dir.iterdir():
        for filing_type_dir in cik_dir.iterdir():
            for filing_dir in filing_type_dir.iterdir():
                filing_doc = filing_dir / "primary-document.html"
                filing_pdf = filing_dir / "primary-document.pdf"
                if filing_doc.exists() and not filing_pdf.exists():
                    print("- Converting {}".format(filing_doc))
                    input_path = str(filing_doc.absolute())
                    output_path = str(filing_pdf.absolute())

                    try:
                        options = {'enable-local-file-access': None}
                        pdfkit.from_file(input_path, output_path, options=options, verbose=True)
                    except Exception as e:
                        print(f"Error converting {input_path} to {output_path}: {e}")


def main(
        output_dir: str = DEFAULT_OUTPUT_DIR,
        ciks: List[str] = DEFAULT_CIKS,
        file_types: List[str] = DEFAULT_FILING_TYPES,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = 30,
):
    """Main function to download and convert SEC filings."""
    print('Downloading filings to "{}"'.format(Path(output_dir).absolute()))
    print("File Types: {}".format(file_types))
    if find_executable("wkhtmltopdf") is None:
        raise Exception(
            "ERROR: wkhtmltopdf (https://wkhtmltopdf.org/) not found, "
            "please install it to convert HTML to PDF "
            "`sudo apt-get install wkhtmltopdf`"
        )
    for symbol, file_type in product(ciks, file_types):
        try:
            download_and_convert_filing(symbol, file_type, output_dir, limit, before, after)
            print(f"- Downloading and converting filing for {symbol} {file_type}")

        except Exception as e:
            print(f"Error downloading and converting filing for symbol={symbol} & file_type={file_type}: {e}")


if __name__ == "__main__":
    Fire(main)
