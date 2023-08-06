import json
def returnDB():
    """
    Returns the database name
    """
    with open('./utils/_credentials/cred.json') as f: 
        return json.load(f)['database']