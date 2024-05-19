# -*- coding: utf-8 -*-

import openpyxl
from openpyxl.worksheet.worksheet import Worksheet

doc = 'db.user_whitelist.inMany()'

def generateDoc(sheet: Worksheet, account: str, module: str, enabled: str, start_time: str, end_time: str) -> str:
	doc = {
		'account': account,
		'type': module,
		
	}

if __name__ == '__main__':
    workbook = openpyxl.load_workbook('whitelist.xlsx')
    sheet = workbook.active
    # generate db command
    workbook.close() 
    