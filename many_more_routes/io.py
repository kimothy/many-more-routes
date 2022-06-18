import openpyxl

from pathlib import Path

from typing import List
from typing import Dict
from typing import Optional
from typing import Protocol

class OutputRecord(Protocol):
    _api: str
    
    def dict(self) -> Dict: ...


def load_excel(file_path: str|Path, sheet_name: Optional[str] = None) -> List[Dict]:
    """ Loads an excel to a list of dictionaries where the first row is the column headers """

    if isinstance(file_path, str):
        file_path = Path(file_path)
    
    if not file_path.exists():
        raise ValueError(f'File "{file_path}" does not exist')

    workbook = openpyxl.load_workbook(str(file_path.absolute()))

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


def write_excel(records: List[OutputRecord], file_path: str|Path) -> None:
    if isinstance(file_path, str):
        file_path = str(Path(file_path).absolute())
    else:
        file_path = str(file_path.absolute())

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = records[0]._api

    counts: Dict = {}
    for record in records:
        if record._api in workbook.sheetnames and record._api in counts.keys():
            sheet = workbook[record._api]
            counts[record._api] += 1

        else:
            if record._api not in workbook.sheetnames:
                workbook.create_sheet(title=record._api)

            sheet = workbook[record._api]
            sheet.cell(1, 1, 'Message')
            sheet.cell(3, 1, 'no')

            for index, value in enumerate(iterable=record.dict().keys(), start=2):
                sheet.cell(1, index, value)
                sheet.cell(3, index, 'yes')

            counts[record._api] = 4

        for index, value in enumerate(iterable=record.dict().values(), start=2):
            sheet.cell(counts[record._api], index, value)


    workbook.save(filename=file_path)