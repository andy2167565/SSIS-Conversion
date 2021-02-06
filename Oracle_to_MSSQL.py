# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 11:44:05 2020

@author: Andy
"""

import os
import re
import time
from datetime import datetime
from random import randrange

# Extract table content in each Oracle script
def LoadTableContent(filename):
    with open(os.path.join(oracle_path, filename), 'r') as oracle:
            upper_parenthesis = lower_parenthesis = None
            lines = oracle.readlines()
            content = []
            for i in range(len(lines)):
                line = lines[i]
                # Detect content lines by first pair of parentheses
                if line == '(\n' and not upper_parenthesis:
                    upper_parenthesis = line
                    first_index = i + 1
                if line == ')\n' and not lower_parenthesis:
                    lower_parenthesis = line
                    last_index = i
                if upper_parenthesis and lower_parenthesis:
                    content = lines[first_index:last_index]
                    break
            return content

# Replace texts in template as required
def ReplaceText(filenum, filelist):
    for i in range(filenum):
        schema = filelist[i].split('.')[0]
        table = filelist[i].split('.')[1]
        
        # Create output folder for each schema
        schema_path = os.path.join(output_path, schema)
        if not os.path.exists(schema_path):
            os.mkdir(schema_path)
        
        content = LoadTableContent(filelist[i])
        with open(os.path.join(schema_path, table + '.sql'), 'w') as file:
            first_indent = True
            f = open(os.path.join(template_path,'<TEMPLATE_FILENAME>.sql'))
            for line in f:
                # Check if specific line is not empty
                if line not in ['\n', '\r\n']:
                    # Check if specific line has leading spaces
                    if re.match(r'\s', line):
                        # Check if it's the first line with indent
                        if first_indent:
                            for j in content:
                                # Replace the leading spaces with tab
                                line = '\t' + j.lstrip(' ')
                                # NUMBER(p,0) and NUMBER(p), p >= 0
                                pattern_1 = re.compile(r'NUMBER\((?:[0-9]+,0|[0-9]+)\)')
                                if pattern_1.search(line):
                                    nums = [int(k) for k in re.split(r'\(|,|\)', line) if k.isdigit()]
                                    line = re.sub(r'NUMBER\((?:[0-9]+,0|[0-9]+)\)', 'DECIMAL(%s)' % nums[0], line)
                                # NUMBER(p,s), p >= 0, s > 0
                                pattern_2 = re.compile(r'NUMBER\([0-9]+,(?:[1-9]|[1-9][0-9]|[1-9][0-9][0-9])\)')
                                if pattern_2.search(line):
                                    nums = [int(l) for l in re.split(r'\(|,|\)', line) if l.isdigit()]
                                    line = re.sub(r'NUMBER\([0-9]+,(?:[1-9]|[1-9][0-9]|[1-9][0-9][0-9])\)', 'DECIMAL(%s,%s)' % (nums[0], nums[1]), line)
                                # VARCHAR2 to NVARCHAR
                                line = line.replace(' VARCHAR2', ' NVARCHAR')
                                # NVARCHAR2 to NVARCHAR
                                line = line.replace(' NVARCHAR2', ' NVARCHAR')
                                # Remove BYTE in VARCHAR2
                                line = line.replace(' BYTE', '')
                                # Lowercase sysdate to getdate()
                                line = line.replace('sysdate', 'getdate()')
                                # Uppercase SYSDATE to GETDATE()
                                line = line.replace(' SYSDATE', ' GETDATE()')
                                # TIMESTAMP to DATETIME2
                                line = line.replace(' TIMESTAMP', ' DATETIME2')
                                line = line.replace("to_number(to_char(getdate(),'YYYYMMDDHH24MISS'))", 'CONVERT(CHAR(20),GETDATE(),120)')
                                file.write(line)
                            # Set first_indent as False after all the contents are written
                            first_indent = False
                        else:
                            pass
                    # Check if line starts with '/'
                    elif line.startswith('/'):
                        pass
                    else:
                        # TEMPLATE_FILENAME to table name
                        line = line.replace("<TEMPLATE_FILENAME>", table)
                        file.write(line)
                else:
                    file.write(line)
        #time.sleep(randrange(480, 781))  # Time gap of 8 ~ 13 mins


def main():
    start_time = datetime.now()
    
    # Set all relevant paths
    global output_path, oracle_path, template_path
    script_path = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(script_path, 'Templates')
    oracle_path = os.path.join(script_path, 'Oracle')
    output_path = os.path.join(script_path, 'MSSQL')
    # Create output path if not exists
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    
    # Number of files
    filenum = len(os.listdir(oracle_path))
    # List of filename
    filelist = os.listdir(oracle_path)
    ReplaceText(filenum, filelist)
    
    end_time = datetime.now()
    time_diff = end_time - start_time
    print('Execution time:', str(time_diff))


if __name__ == '__main__':
    main()
