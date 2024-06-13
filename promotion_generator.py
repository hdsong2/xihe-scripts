# -*- encoding: utf-8 -*-

import uuid
import json
from datetime import datetime, timedelta

cmd = 'db.promotion.insert({})'

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
    print()
    print(cmd.format(generate_promotion_info(promotion_id="mindspore_clockin_25" ,name="昇思MindSpore 25天学习打卡营", desc="每天15分钟，25天打通AI任督二脉", 
                                             duration="2024.06.15-2024.07.25")))
    print()
