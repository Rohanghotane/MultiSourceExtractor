import pandas as pd

def write_sheets_to_excel(dfs_dict, out_path):
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for sheet_name, df in dfs_dict.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
