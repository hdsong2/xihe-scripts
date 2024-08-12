# -*- encoding: utf-8 -*-

import json
import argparse
import sys
from datetime import timezone

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

import utils

cmd = 'db.promotion.insertMany({}, {{ordered: false}})'

def generate_promotion_info(sheet: Worksheet) -> str:
    docs = []
    for row in sheet.iter_rows(min_row=sheet.min_row+1, max_row=sheet.max_row, values_only=True):
        (promotion_id, name, desc, startTime, endTime, host, kind, way, priority, poster, intro, need_sign_up) = row
        
        if promotion_id == None:
            continue

        if isinstance(startTime, str):
            startTime = utils.str_to_datetime(startTime)
        if isinstance(endTime, str):
            endTime = utils.str_to_datetime(endTime)
            
        doc = {
            'id': promotion_id,
            'name': name,
            'desc': desc,
            'start_time': int(startTime.timestamp()),
            'end_time': int(endTime.timestamp()),
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
        
        docs.append(doc)

    return json.dumps(docs)

def main(args):
    workbook = openpyxl.load_workbook(args.filename)
    sheet = workbook.active
    info = generate_promotion_info(sheet)
    workbook.close()

    out = cmd.format(info)

    sys.stdout.write('\n' + out + '\n\n')
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('-f', '--filename', required=True, help='the excel of promotion')

    args = parser.parse_args()

    main(args)
