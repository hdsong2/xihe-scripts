# -*- coding: utf-8 -*-

import json
import argparse
import sys

import openpyxl
from openpyxl import Workbook
import pymongo

import utils
import mongo

def generate_promotions(wb: Workbook) -> str:
    sheet = wb.active

    operations = []
    for row in sheet.iter_rows(min_row=sheet.min_row+1, values_only=True):
        (promotion_id, name, desc, start_time, end_time, host, kind, way, priority, poster, intro, need_sign_up) = row
        
        if not any(row): break
        if promotion_id == None: continue

        if isinstance(start_time, str):
            start_time = utils.str_to_datetime(start_time)
        if isinstance(end_time, str):
            end_time = utils.str_to_datetime(end_time)
            
        doc = {
            'id': promotion_id,
            'name': name,
            'desc': desc,
            'start_time': int(start_time.timestamp()),
            'end_time': int(end_time.timestamp()),
            'type': kind,
            'host': host if host else "",
            'way': way,
            'poster': poster,
            'intro': intro,
            'version': 1,
        }

        if priority != None:
            doc['priority'] = priority
        if need_sign_up != None and isinstance(need_sign_up, bool):
            doc['is_static'] = not need_sign_up

        operations.append(pymongo.ReplaceOne(
            {'id': promotion_id},
            doc,
            upsert=True
        ))
        
        db = mongo.db()
        result = db.promotion.bulk_write(operations, ordered=False)
        
        print(result.bulk_api_result)

def main(args):
    wb = openpyxl.load_workbook(args.filename)
    generate_promotions(wb)
    wb.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit(1)
    
    parser.add_argument('-f', '--filename', required=True, help='the excel of promotions')

    config = None
    with open('./mongo.json') as f:
        config = json.load(f)
    mongo.initialize(config)

    args = parser.parse_args()
    main(args)
    
    mongo.close()
