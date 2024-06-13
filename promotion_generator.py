# -*- encoding: utf-8 -*-

import uuid
import json
from datetime import datetime, timedelta
import argparse
import sys

def generate_promotion_info(promotion_id="", name="", desc="", duration="", poster="") -> str:
    if promotion_id == "":
        promotion_id = "mindSpore_competition_{}".format(str(uuid.uuid4())[:6])

    if duration == "":
        start = datetime.now()
        end = start + timedelta(days=7)
        duration = datetime.strftime(start, '%Y.%m.%d') + '-' + datetime.strftime(end, '%Y.%m.%d')
        
    return json.dumps({
        'id': promotion_id,
        'name': name,
        'desc': desc,
        'reg_users': [],
        'duration': duration,
        'version': 1,
        'poster': poster,
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pid', required=True, help='promotion id')
    parser.add_argument('-n', '--name', required=True, help='promotion name')
    parser.add_argument('--desc', required=True, help='promotion desc')
    parser.add_argument('-d', '--duration', required=True, help='promotion duration')

    args = parser.parse_args()

    out = 'db.promotion.insert({})'.format(generate_promotion_info(promotion_id= args.pid, name=args.name, 
                                                                   desc=args.desc, duration=args.duration))
    
    sys.stdout.write('\n' + out + '\n\n')
