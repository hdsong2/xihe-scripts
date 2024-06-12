# -*- coding: utf-8 -*-

import argparse
import json
from datetime import datetime
import sys
from typing import Dict, Union

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

manual_cmd = 'db.user_whitelist.insert({})'
batch_cmd = 'db.user_whitelist.insertMany({})'

def str_to_timestamp(date_string: str, format='%Y-%m-%d %H:%M:%S') -> int:
    dt_object = datetime.strptime(date_string, format) 
    return int(dt_object.timestamp())  

def str_to_bool(s: str) -> bool:
    if s not in ['true', 'false']:
        raise Exception('input should be "true" or "false"')

    return s == "true"

def generateDoc(username: str, kind: str, start_time: int, end_time: int, enabled: bool) \
    -> Dict[str, Union[str, int, bool]]:
    return {
        'account': username,
        'type': kind,
        'enabled': enabled, 
        'start_time': start_time,
        'end_time': end_time,
    }  

def generateDocs(sheet: Worksheet) -> str:
    docs = []
    for row in sheet.iter_rows(min_row=sheet.min_row+2, max_row=sheet.max_row-1, values_only=True):
        (account, startTime, endTime, cloudType, enabled) = row
        docs.append(generateDoc(account, cloudType, int(startTime.timestamp()), int(endTime.timestamp()), enabled))

    return json.dumps(docs)

def main(args):
    if hasattr(args, 'filename'):
        workbook = openpyxl.load_workbook(args.filename)
        sheet = workbook.active
        docs_string = generateDocs(sheet)
        workbook.close()
        with open('./output/cmd.js', 'w') as f:
            f.write(batch_cmd.format(docs_string))
        
        return
    
    
    (account, startTime, endTime, cloudType, enabled) = (args.username, args.start_time, args.end_time, args.type, 
                                                         args.enabled)
    print(manual_cmd.format(generateDoc(account, cloudType, startTime, endTime, enabled)))
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit(1)
    
    subparsers = parser.add_subparsers(title='subcommand')

    manual_parser = subparsers.add_parser('manual', description='insert account manually')
    manual_parser.add_argument('-u', '--username', required=True, help='xihe account')
    manual_parser.add_argument('-t', '--type', required=True, help='allow module')
    manual_parser.add_argument('--start_time', type=str_to_timestamp, required=True, 
                               help='timestamp like "2024-06-12 09:27:00"')
    manual_parser.add_argument('--end_time', type=str_to_timestamp, required=True, 
                               help='timestamp like "2024-06-12 09:27:00"')
    manual_parser.add_argument('--enabled', type=str_to_bool, required=True, help="open or block permission")

    batch_parser = subparsers.add_parser('batch', description="insert accounts in batch")
    batch_parser.add_argument('-f', '--filename', type=str, required=True, help="the excel of whitelist")
    
    args = parser.parse_args()
        
    main(args)