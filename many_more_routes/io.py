import openpyxl
from pathlib import Path

from typing import List
from typing import Dict
from typing import Optional


def load_excel(file_path: str|Path, sheet_name: Optional[str] = None) -> List[Dict]:
    """ Loads an excel to a list of dictionaries where the first row is the column headers """

    if isinstance(file_path, str):
        file_path = Path(file_path)
    
    if not file_path.exists():
        raise ValueError(f'File "{file_path}" does not exist')

    workbook = openpyxl.load_workbook(file_path)

    if sheet_name:
        sheet = workbook[sheet_name]

    else:
        sheet = workbook.active

    headers = [col.value for col in sheet[1]]

    return [
        {
            header: col.value for (header, col) in zip(headers, sheet[row])
        } for row in range(2, sheet.max_row + 1)
    ]

if __name__ == '__main__':
    xl = load_excel(r'c:\Users\nnckten\Desktop\Clean Desktop\4 Route_Set-up_bwx3v2yo.xlsx', 'TEMPLATE_V3')

    import pandas as pd

    df = pd.DataFrame(xl)
    print(df)
