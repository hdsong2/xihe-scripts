# -*- coding: utf-8 -*-

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

import json
from datetime import datetime

cmd = 'db.user_whitelist.insertMany({})'

def string_to_timestamp(date_string, format="%Y-%m-%d %H:%M:%S"):
    dt_object = datetime.strptime(date_string, format)  
    timestamp = dt_object.timestamp()  
    return timestamp  

def generateDocs(sheet: Worksheet) -> str:
    docs = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        (account, cloudType, enabled, startTime, endTime) = row
        doc = {
            'account': account,
            'type': cloudType,
            'enabled': bool(enabled),
            'start_time': int(startTime.timestamp()),
            'end_time': int(endTime.timestamp()),
        }
        docs.append(doc)

    return json.dumps(docs)

if __name__ == '__main__':
    workbook = openpyxl.load_workbook('./whitelist.xlsx')
    sheet = workbook.active
    docs_string = generateDocs(sheet)
    workbook.close()
    with open('./cmd.js', 'w') as f:
        f.write(cmd.format(docs_string))
    