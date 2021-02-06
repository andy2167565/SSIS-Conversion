# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 14:57:41 2020

@author: Andy
"""
import os
import time
from datetime import datetime
import pandas as pd
from random import randrange


def ReplaceText(template, rownum):
    for i in range(rownum):
        with open(os.path.join(output_path, template.iloc[i]['Job ID'] + '.dtsx'), 'w') as file:
            f = open(os.path.join(template_path,'<TEMPLATE_FILENAME>.dtsx'))
            for line in f:
                line = line.replace("EXEC sp_Insert_AuditLog '<SSIS_JOB_FILENAME>', 'System C - <TABLE_NAME>.dtsx', 'COPIA - Import Status Activities Information', 'E', '';", template.iloc[i]['Write Audit Log - Completed'])
                line = line.replace("EXEC sp_Insert_AuditLog '<SSIS_JOB_FILENAME>', 'System C - <TABLE_NAME>.dtsx', 'COPIA - Import Status Activities Information', 'R', 'Execution Stopped - Import Interface failed';", template.iloc[i]['Write Audit Log - Error - Import Failure'])
                line = line.replace("EXEC sp_Insert_AuditLog '<SSIS_JOB_FILENAME>', 'System C - <TABLE_NAME>.dtsx', 'COPIA - Import Status Activities Information', 'S', '';", template.iloc[i]['Write Audit Log - Kick Start'])
                line = line.replace("<SCHEMA_NAME>", template.iloc[i]['Source Schema'])
                line = line.replace("<TABLE_NAME>", template.iloc[i]['Table Name'])
                line = line.replace("SNAP_DATE", "DATA_DATE")
                file.write(line)
        #time.sleep(randrange(480, 781))  # Time gap of 8 ~ 13 mins


def main():
    start_time = datetime.now()
    
    global output_path, template_path
    script_path = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_path, 'Templates')
    output_path = os.path.join(script_path, 'SSIS Jobs')
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    df = pd.read_csv(os.path.join(template_path, '<SOURCE_FILE_LIST>.csv'), header=0)
    r, c = df.shape
    ReplaceText(df, r)
    
    end_time = datetime.now()
    time_diff = end_time - start_time
    print('Execution time:', str(time_diff)[:-7])


if __name__ == '__main__':
    main()
