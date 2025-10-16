import camelot
import pandas as pd

def extract_tables_from_pdf(pdf_path, start_page=11, end_page=55):
    pages = ",".join(map(str, range(start_page, end_page+1)))
    tables = camelot.read_pdf(pdf_path, pages=pages, flavor='lattice') 
    dfs = []
    for t in tables:
        dfs.append(t.df)
    
    return dfs  
