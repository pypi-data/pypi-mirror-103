"""
Helper for bash SQL Database auto-generating
"""
import json
with open('./json/_credentials/cred.json') as f: 
    db_conn_dict = json.load(f)
    print(db_conn_dict['host'])