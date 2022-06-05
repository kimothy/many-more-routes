# -*- coding: utf-8 -*-
"""
smartdata.py

Part of Route Configuration Program
Use in conjunction with template files .xlsx with sheet name TEMPLATE_V2

Based on the template SmartData tool excel sheets are created to be
uploaded into Infor M3 using the API's.

This files handles the export of dataframes to excel files that can
be used with SmartDataTool.

Author: Kim Timothy Engh
Maintainer: Kim Timothy Engh
Copyright: 2022, Kim Timothy Engh
Licence: GPL v3

Created for the More program template
"""


import pandas as pd
from tempfile import NamedTemporaryFile
from typing import Optional, List
from os import system


def to_smart_format(df: pd.DataFrame, desc: Optional[List[str]] = None, mandetory: Optional[List[str]] = None) -> pd.DataFrame:
    '''Take a DataFrame and create a message column, then add description and
    mandetory row to conform with the smart datatool layout of the excel files
    The dataframe columns names needs to conform to fields used in the
    smartsheet.'''
    df = df.copy()

    df = df.astype({col: str for col in df.keys()}, errors='raise') 

    df.insert(0, 'Message', '')

    if not mandetory:
        mandetory = (['no'] + (['yes'] * (len(df.columns) - 1)))

    if not desc:
        desc = ('' * len(df.columns))

    df.loc[-2] = desc
    df.loc[-1] = mandetory

    df.index = df.index + 2
    df.sort_index(inplace=True)

    return df


def open_in_excel(excelFile: str) -> None:
    '''
    Opens the given file in Microsoft Excel
    '''
    system('start EXCEL.EXE %s' %excelFile)


def to_excel(df: pd.DataFrame, sheet: str) -> None:
    ''' Takes a DataFrame and export to a temporary excel file
    with a specified sheet name, then opens it up in excel.
    Normally the sheet name should correspond to the sheet name
    used for a specific smartsheet.
    '''

    with NamedTemporaryFile(prefix=sheet, suffix='.xlsx', delete=False) as f:
        df.to_excel(f, index=False, sheet_name = sheet)
        open_in_excel(f.name)


def export(df: pd.DataFrame, sheet: str, desc: Optional[List[str]] = '', mandetory: Optional[List[str]] = None) -> None:
    '''Converts df to smartdata format then exports to excel.
    Wrapper around to_smart_format and to_excel functions that creates
    default values for "description" and "mandetory" if not given.
    '''

    df = to_smart_format(df, desc, mandetory)
    to_excel(df, sheet)


def export_many(dfs: List[pd.DataFrame], sheets: List[str], filepath: str = None):
    '''Takes a lists of dataframes and a list of sheet names and adds all of them to
    a single excel file to be used with SmartDataTool. Normally the sheet name should
    corresond with the sheet name SmartDataTool is looking for per specific API.
    '''

    if filepath:
        with open(filepath, 'wb') as f:
            with pd.ExcelWriter(f.name, engine='openpyxl') as w:
                for df, sheet in zip(dfs, sheets):
                    df.to_excel(w, index=False, sheet_name = sheet)

    else:
        with NamedTemporaryFile(prefix='Route_Set-up_', suffix='.xlsx', delete=False) as f:
            with pd.ExcelWriter(f.name, engine='openpyxl') as w:
                for df, sheet in zip(dfs, sheets):
                    df.to_excel(w, index=False, sheet_name = sheet)

            open_in_excel(f.name)
