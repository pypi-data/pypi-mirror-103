<p align="center">
  <h3 align="center">pg-quickstart</h3>
  <p align="center">
    This package is aimed at beginners and students looking to deploy a relational database remotely on a hosted linux server. It contains streamlined one-line setup and is packaged with prebaked functions to wrap
    and send SQL queries to the database.
    <br>
  </p>
</p>


## Table of contents

- [Quick start](#quick-start)
- [Usage](#usage)
- [Copyright and license](#copyright-and-license)


## Quick start

The package can be installed using pip
```
pip install pg-quickstart
```

## Usage

Import the package.
```
import pg_quickstart as pgQ
```

The package requires some credentials for your server to form a connection. They can be loaded using `pgQ.write_credentials`.
```
ip = "129.0.0.1"
host = 5000
dbName = "database"

pgQ.write_credentials(ip, host, dbName)
```
The database can be created by calling `pgQ.initialize_database()`. This function takes no arguements and reads from the credentials specified before
```
pgQ.initialize_database()
```
Now the database is created, the packaged helper tools can be used to add tables and handle queries to the database. First we need a connection to our database. To initialize a connection use SQLTools.
```
from pg_quickstart.utils.tools import SQLTools

connection = SQLTools()
```

Now a connection has been established, you can use the packaged `SQLTools.query()` function to send general queries to the database in any form you like. Otherwise, additional helper functions allow easy schema creation based on the data given.
```
data = pd.read_csv('data.csv')
connecttion.parse_and_upload(data)

connection.query("""SELECT * FROM database""")
```

## Copyright and license

Code released under the [MIT Licence](https://github.com/je-c/pixel_reshaper/blob/main/LICENSE).