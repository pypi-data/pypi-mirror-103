import subprocess
import json

def write_credentials(ip:str, port:int, dbName:str):
    """
    Writes a credentials file

    Parameters
    ----------
    ip : str
        target server address
    port : int
        host connection port
    dbName : str 
        name of database

    Returns
    -------
    None
    """
    js_temp = {'host':ip, 'port':port, 'database':dbName, 'password':""}
    credentials = open('./utils/_credentials/cred.json', 'w')
    credentials.write(json.load(js_temp))
    
def initialize_database():
    """
    Calls a bash script that ssh's into a remote server with supplied and inputted credentials
    to initialise a PostgreSQL database on the target remote server

    Parameters
    ----------
    None
    
    Returns
    -------
    None
    """
    try:
        with open('./utils/_credentials/cred.json') as credentials:
            if len(json.load(credentials)) < 1:
                raise ValueError "Empty credentials encountered. Please check ./utils/_credentials/cred.json"
        
        return subprocess.call("./utils/setup")
    except FileNotFoundError:
        print('Credentials does not exist. Have you renamed ./utils/_credentials/cred.json?')