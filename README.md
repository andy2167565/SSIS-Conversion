# SSIS Conversion
Automatize manual process of Oracle PL/SQL to MSSQL T-SQL conversion and SSIS job conversion

## Oracle PL/SQL to MSSQL T-SQL
### Directory Structure
    .
    ├── MSSQL
    ├── Oracle
    ├── Templates
    │   └── <TEMPLATE_FILENAME>.sql
    └── Oracle_to_MSSQL.py

* Oracle: Input folder containing Oracle PL/SQL scripts for conversion
* MSSQL: Output folder with generated MSSQL T-SQL files sorted by schema name (automatically generated)
* Templates: MSSQL T-SQL template file

## SSIS Job Conversion
### Directory Structure
    .
    ├── SSIS Jobs
    ├── Templates
    │   ├── <TEMPLATE_FILENAME>.dtsx
    │   └── <SOURCE_FILE_LIST>.csv
    └── Replicate_SSIS_Job.py

* SSIS Jobs: Output folder including generated SSIS job files (automatically generated)
* Templates: Contains sample SSIS job file and a CSV list of required output information

## How to Execute
### In Command Prompt
```
python Oracle_to_MSSQL.py
python Replicate_SSIS_Job.py
```
***
Copyright © 2020 [Andy Lin](https://github.com/andy2167565). All rights reserved.
