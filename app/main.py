import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers.graypoint_scraper import scrape_graypoint
from scrapers.rightmove_scraper import scrape_rightmove
from scrapers.amazon_scraper import scrape_amazon_table_fans
from pdf_tools.pdf_table_extract import extract_tables_from_pdf
from ocr.aadhaar_ocr import process_aadhaar_folder
from utils.excel_writer import write_sheets_to_excel
import pandas as pd

def main():
    
    print("Scraping Gray Point...")
    try:
        df_gray = scrape_graypoint("https://www.gray-point.com/properties/")
    except Exception as e:
        print("Graypoint error:", e)
        df_gray = pd.DataFrame()

    
    print("Scraping Rightmove (first 40 items)...")
    try:
        df_right = scrape_rightmove("https://www.rightmove.co.uk/commercial-property-to-let.html", max_items=40)
    except Exception as e:
        print("Rightmove error:", e)
        df_right = pd.DataFrame()

    
    print("Scraping Amazon (table fans)...")
    try:
        df_amazon = scrape_amazon_table_fans("table fan", max_results=20)
    except Exception as e:
        print("Amazon error:", e)
        df_amazon = pd.DataFrame()

    
    print("Extracting tables from PDF pages 11-55...")
    pdf_path =  r"C:\Users\kk\Desktop\Settyl\Assignment\New asign\Test - DS\QA - Supporting Files\QA - 4 - PDF\input.pdf"  # place your PDF here
    try:
        pdf_tables = extract_tables_from_pdf(pdf_path, 11, 55)
        
        pdf_combined = pd.concat([df for df in pdf_tables], ignore_index=True) if pdf_tables else pd.DataFrame()
    except Exception as e:
        print("PDF error:", e)
        pdf_combined = pd.DataFrame()

    
    print("Processing Aadhaar images...")
    try:
        aadhaar_paths =  r"C:\Users\kk\Desktop\Settyl\Assignment\New asign\Test - DS\QA - Supporting Files\QA - 5 - Aadhar Cards"  # replace with actual paths
        df_aadhaar = process_aadhaar_folder(aadhaar_paths)
    except Exception as e:
        print("Aadhaar OCR error:", e)
        df_aadhaar = pd.DataFrame()

    
    sheets = {
        "GrayPoint": df_gray,
        "RightMove": df_right,
        "Amazon_TableFans": df_amazon,
        "PDF_Tables_11-55": pdf_combined,
        "Aadhaar_Data": df_aadhaar
    }
    write_sheets_to_excel(sheets, "extracted_results.xlsx")
    print("Done. Output written to extracted_results.xlsx")

if __name__ == "__main__":
    main()
