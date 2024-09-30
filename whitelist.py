# -*- coding: utf-8 -*-

import argparse
import sys
import json

import openpyxl
from openpyxl import Workbook
import pymongo

import utils
import mongo

def str_to_bool(s: str) -> bool:
    if s not in ['true', 'false']:
        raise Exception('input should be "true" or "false"')

    return s == 'true'

def upsert_whitelist(account: str, kind: str, start_time: int, end_time: int, enabled: bool):
    db = mongo.db()

    doc = {
        'account': account,
        'type': kind,
        'enabled': enabled, 
        'start_time': start_time,
        'end_time': end_time,
    }  

    filter = {'account': account, 'type': kind}
    result = db.user_whitelist.replace_one(filter, doc, upsert=True)

    print(result.raw_result)

def bulk_write_whitelist(wb: Workbook):
    sheet = wb.active
    filter = set([])
    operations = []

    for row in sheet.iter_rows(min_row=sheet.min_row+1, values_only=True):
        if not any(row): break

        (account, start_time, end_time, kind, enabled) = row        
        account = account.strip()
        kind = kind.strip()

        key = (account, kind)
        if key in filter:
            continue

        if isinstance(start_time, str):
            start_time = utils.str_to_datetime(start_time)
        if isinstance(end_time, str):
            end_time = utils.str_to_datetime(end_time)
            
        operations.append(pymongo.ReplaceOne(
            {'account': account, 'type': kind},
            {
                'account': account,
                'type': kind,
                'enabled': enabled, 
                'start_time': int(start_time.timestamp()),
                'end_time': int(end_time.timestamp()),
            },
            upsert=True
        ))  
        
        filter.add(key)

    db = mongo.db()
    result = db.user_whitelist.bulk_write(operations, ordered=False)

    print(result.bulk_api_result)

def main(args):
    if hasattr(args, 'filename'):
        wb = openpyxl.load_workbook(args.filename)
        bulk_write_whitelist(wb)
        wb.close()
    else:
        (account, startTime, endTime, cloudType, enabled) = (args.username, args.start_time, args.end_time, args.type, 
                                                         args.enabled)
        upsert_whitelist(account, cloudType, startTime, endTime, enabled) 


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit(1)
    
    subparsers = parser.add_subparsers(title='subcommand')

    manual_parser = subparsers.add_parser('manual', description='insert account manually')
    manual_parser.add_argument('-u', '--username', required=True, help='xihe account')
    manual_parser.add_argument('-t', '--type', default="cloud", help='allowed module')
    manual_parser.add_argument('--start_time', type=utils.str_to_timestamp, required=True, 
                               help='timestamp like "2024-06-12 09:27:00"')
    manual_parser.add_argument('--end_time', type=utils.str_to_timestamp, required=True, 
                               help='timestamp like "2024-06-12 09:27:00"')
    manual_parser.add_argument('--enabled', type=str_to_bool, default=True, help="open or block permission [true/false]")

    batch_parser = subparsers.add_parser('batch', description="insert accounts in batch")
    batch_parser.add_argument('-f', '--filename', type=str, required=True, help="the excel of whitelist")
    
    config = None
    with open('./mongo.json') as f:
        config = json.load(f)
    mongo.initialize(config)

    args = parser.parse_args()         
    main(args)

    mongo.close()
