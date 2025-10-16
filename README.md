# MultiSource Data Extractor

A Python project to **extract data from multiple sources**—web scraping, PDF documents, and Aadhaar images—then consolidate the results into an Excel file. Ideal for automating data collection and reporting.

---

## **Features**

- Web scraping from specified websites
- PDF parsing for text and tables
- OCR processing of Aadhaar cards or scanned documents
- Generates a structured Excel file with separate sheets for each source
- Modular architecture for easy extension

---

## **Folder Structure**

project_root/
│
├── main.py
├── scrapers/
│ ├── init.py
│ └── graypoint_scraper.py
├── pdf_tools/
│ ├── init.py
│ └── pdf_parser.py
├── ocr/
│ ├── init.py
│ └── aadhaar_ocr.py
└── utils/
├── init.py
└── excel_writer.py


- `main.py` → Entry point
- `scrapers/` → Web scraping modules
- `pdf_tools/` → PDF parsing modules
- `ocr/` → OCR modules
- `utils/` → Excel writer and helper utilities

---

## **Setup Instructions**

### **1. Clone the repository**

```bash
git clone https://github.com/Rohanghotane/MultiSourceExtractor
cd MultiSource-Data-Extractor


#Create a Python virtual environment
python -m venv venv
# To activate
venv\Scripts\activate

#Install required packages
pip install -r dependency.txt


#Run the script
python main.py  or
python main1.py

