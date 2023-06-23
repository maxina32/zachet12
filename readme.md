# Apache logger

This programm allows you to save Apache access.log in PostgreSQL database. It creates API, which can help you access database. Also, it can work with cron, and have web interface.


## Creating table

```console
foo@bar:~$ sudo -i -u postgres
postgres@bar:~$ psql -U username -d myDataBase -a -f path/to/table.sql
postgres@bar:~$ exit
```

## Running server with pipenv

```console
foo@bar:~$ pip install pipenv
foo@bar:~$ pipenv install
foo@bar:~$ pipenv run python3 main.py
```

## Request format

- `DataBase_update` - **POST** method. Returns `{"status" : "ok"}`. Used to update database with log files. 
- `DataBase_get_log`- **GET** method. Takes two arguments: `from` and `to`, which corresponds to start and end of timeframe. Returns array of **JSON**, each of them have `{"address" : "192.168.0.1", "date" : "2023-06-22-13-00-00}` structure. Date must be in **YYYY-MM-DD-HH-mm-dd** format. You can get all entries in database, by providing `from=all` argument. 
## Request example

```http
POST http://127.0.0.1:5000/DataBase_update
{"status" : "ok"}

GET http://127.0.0.1:5000/DataBase_get_log?from=2023-06-22-12-45-10&to=2023-06-24-15-34-00
[{"address" : "192.168.0.1", "date" : "2023-06-22-13-00-00}, ...]

GET http://127.0.0.1:5000/DataBase_get_log?from=all
[{"address" : "192.168.0.1", "date" : "2023-06-22-13-00-00}, ...]
```

