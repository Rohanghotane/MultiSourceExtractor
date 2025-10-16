import cv2
import pytesseract
import re
import pandas as pd
from config import TESSERACT_CMD
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD

def ocr_aadhaar_image(path):
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # basic preprocessing
    gray = cv2.bilateralFilter(gray, 9, 75, 75)
    _, th = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    text = pytesseract.image_to_string(th, lang='eng')
    # regex patterns
    aadhaar_pattern = re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b")
    dob_pattern = re.compile(r"\b(?:\d{2}[-/]\d{2}[-/]\d{4}|\d{2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4})\b", re.I)
    name_pattern = re.compile(r"(?<=Name[:\s])([A-Z][A-Z\s\.]+)", re.I)
    pin_pattern = re.compile(r"\b\d{6}\b")

    aadhaar = aadhaar_pattern.search(text)
    dob = dob_pattern.search(text)
    pin = pin_pattern.search(text)
    # crude name extraction: fallback to first capitalized line
    name = ""
    m = name_pattern.search(text)
    if m:
        name = m.group(1).strip()
    else:
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        if lines:
            # heuristic: name likely is one of first 3 lines
            for l in lines[:4]:
                if any(ch.isalpha() for ch in l) and l.isupper():
                    name = l
                    break

    # Gender extraction
    gender = "Unknown"
    if re.search(r"\bMale\b", text, re.I): gender = "Male"
    if re.search(r"\bFemale\b", text, re.I): gender = "Female"

    return {
        "Name": name,
        "Date of Birth": dob.group(0) if dob else "",
        "Gender": gender,
        "Aadhaar Number": aadhaar.group(0) if aadhaar else "",
        "Pincode": pin.group(0) if pin else "",
        "RawText": text
    }

def process_aadhaar_folder(folder_paths):
    import os
    rows = []
    for p in folder_paths:
        rows.append(ocr_aadhaar_image(p))
    return pd.DataFrame(rows)
