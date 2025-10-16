

import sys
import os


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from scrapers.graypoint_scraper import scrape_graypoint
from scrapers.graypoint_scraper import scrape_graypoint
from pdf_tools.pdf_parser import parse_pdf
from ocr.aadhaar_ocr import read_aadhaar
from utils.excel_writer import write_to_excel

def main():
    
    print("Scraping data from Graypoint...")
    web_data = scrape_graypoint()

 
    pdf_folder = r"C:\Users\kk\Desktop\Settyl\Assignment\New asign\Test - DS\QA - Supporting Files\QA - 4 - PDF"
    print(f"Parsing PDFs in folder: {pdf_folder}")
    pdf_data = parse_pdf(pdf_folder)

    
    aadhaar_folder = r"C:\Users\kk\Desktop\Settyl\Assignment\New asign\Test - DS\QA - Supporting Files\QA - 5 - Aadhar Cards"
    print(f"Running OCR on Aadhaar images in folder: {aadhaar_folder}")
    ocr_data = read_aadhaar(aadhaar_folder)

    
    combined_data = {
        "web": web_data,
        "pdf": pdf_data,
        "ocr": ocr_data
    }

    
    output_file = "extracted_results.xlsx"
    print(f"Writing data to Excel file: {output_file}")
    write_to_excel(combined_data, output_file)

    print("✅ Extraction complete!")

if __name__ == "__main__":
    main()
