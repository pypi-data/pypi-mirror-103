import psycopg2, psycopg2.extras, json
import pandas as pd

from sqlalchemy import create_engine
from getpass import getpass
from db import returnDB

class SQLTools:
    """
    SQLTools Class
    --------------

    Wrapper for SQL and databasing tools. Contains functions for querying non-local and local databases,
    flexible schema mapping and data storage.
    """
    def __init__(self):
        """
        Initializes the tools instance with required metadata and a connection. Redefine self.db to
        any desired internal naming standards, defualt is the database name specified in cred.json.
        """
        self.conn = SQLTools().connect(credentials)
        self.db = returnDB()
    
    def query(self, sqlcmd:str, args=None, msg=False, returntype='tuple'):
        """
        Utility function for packaging SQL statements from python.

        Parameters
        ----------
        sqlcmd : str
            query to send to remote database
        args : dict
            optional arguements for querying remote database
        msg : str 
            return message from server
        returntype : str 
            demarkation of expected query return type

        Returns
        -------
        str
            return message from the server
        """
        returnval = None
        with self.conn:
            cursortype = None if returntype != 'dict' else psycopg2.extras.RealDictCursor
            with self.conn.cursor(cursor_factory=cursortype) as cur:
                try:
                    if args is None:
                        cur.execute(sqlcmd)
                    else:
                        cur.execute(sqlcmd, args)
                    if (cur.description != None ):
                        returnval = cur.fetchall()
                    if msg != False:
                        print("success: " + msg)
                except psycopg2.DatabaseError as e:
                    if e.pgcode != None:
                        if msg: print("db read error: "+msg)
                        print(e)
                except Exception as e:
                    print(e)
        return returnval

    def connect(self, credential_filepath:str):
        """
        Connection terminal from python to SQL server

        Parameters
        ----------
        credential_filepath : str
            filepath to credentials json file

        Returns
        -------
        conn psycopg2.connection
            port connection to remote database
        """
        try:
            with open(credential_filepath) as f:
                db_conn_dict = json.load(f)
                db_conn_dict['password'] = getpass()
            self.conn = psycopg2.connect(**db_conn_dict)
            print('Connection successful')
        except Exception as e:
            print("Connection unsuccessful... Try again")
            print(e)
            return None
    
    def sqlInject(self, data:pd.DataFrame, query:str):
        """
        Pipeline for uploading data to SQL server

        Parameters
        ----------
        data : pd.DataFrame
            data to push to database
        query : str
            SQL query, insert statement

        Returns
        -------
        None
        """
        count = 0
        if isinstance(data, list):
            for df in data:
                print(f'Element {count} data injection commenced')
                
                for _, area in df.iterrows():
                    SQLTools.query(insert_stmt, args=area, msg="inserted ")
                
                count += 1
                
        else:
            for _, area in data.iterrows():
                SQLTools.query(insert_stmt, args=area, msg="inserted ")

    @staticmethod
    def feed_schema(data:pd.DataFrame):
        """
        Flexible schema mapping for incoming data. Allows non-fixed axis 1 dimension

        Parameters
        ----------
        data : pd.DataFrame
            data to push to database
        query : str
            SQL query, insert statement

        Returns
        -------
        ___ : str
            segemnt of schema, used by parse_and_upload
        """
        schema_segment = [
            f'{col} NUMERIC,\n' if col != data.columns()[-1] else f'{col} NUMERIC' for col in data.columns()
        ]
        return ''.join(schema_segment)

    def parse_and_upload(self, data:pd.DataFrame, **kwargs):
        """
        Parses data from local directories to relational database.

        Parameters
        ----------
        credfilepath : dict
            database credentials
        data : pd.DataFrame
            data to push to database
        kwargs : dict
            optional query mapping

        Returns
        -------
        None
        """
        if not kwargs:
            insert_stmt = f"""
                INSERT INTO {self.db} VALUES ( {', '.join([col for col in data.columns()])} )
            """
            
            _schema = f"""
                    CREATE TABLE {self.db}(
                        date DATETIME PRIMARY KEY,
                        {SQLTools.feed_schema(data)}
                    );
            """
        else:
            insert_stmt, _schema = [kwargs[key] for key in kwargs]

        SQLTools.query(f"DROP TABLE IF EXISTS {self.db} CASCADE", msg="cleared old table")
        SQLTools.query(_schema, msg=f"created {self.db} table")
        SQLTools.sqlInject(data, insert_stmt)