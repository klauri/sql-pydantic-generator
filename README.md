# SQL Table and Pydantic Generator
Generates SQL tables and pydantic models based off a json file. Please see `tables_json/EXAMPLE.json` for template. 

## Prerequisites

- Database with python connectivity
- Connection class:  Define a class with an "execute" method for executing SQL statements on the database