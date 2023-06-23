import configparser
from apachelogs import LogParser
import psycopg2
import os
from flask import Flask, jsonify, request
from datetime import datetime

config = configparser.ConfigParser()
config.read('apachelog.conf')
parser = LogParser(config['DEFAULT']['ApacheLogFormat'])
app = Flask(__name__)

@app.route('/DataBase_get_log', methods=['GET'])
def DataBase_get_log():
    try:
        conn = psycopg2.connect(dbname=config['DEFAULT']['DataBaseName'],
                                user=config['DEFAULT']['DataBaseUsername'], host=config['DEFAULT']['DataBaseHostname'], port=config['DEFAULT']['DataBasePort'], password=config['DEFAULT']['DataBasePassword'])
        cursor = conn.cursor()
    except BaseException as e:
        print("Can't connect to database: "+str(e))
        exit()
    if (request.args.get("from") != "all"):
        print(request.args.get("from"), request.args.get("to"),)
        fromDate = datetime.strptime(
            request.args.get("from"), '%Y-%m-%d-%H-%M-%S')
        toDate = datetime.strptime(request.args.get("to"), '%Y-%m-%d-%H-%M-%S')
        cursor.execute(
            "SELECT * FROM logs WHERE date >= %s and date <  %s", (fromDate, toDate,))
    else:
        cursor.execute(
            "SELECT * FROM logs")
    json = []
    ans = cursor.fetchall()
    for addrs in ans:
        json.append({"address": addrs[0], "date": addrs[1]})
    response = jsonify(json)
    response.headers.add('Access-Control-Allow-Origin', '*')
    cursor.close()
    conn.close()
    return response

@app.route('/DataBase_update', methods=['POST'])
def DataBase_update():
    try:
        conn = psycopg2.connect(dbname=config['DEFAULT']['DataBaseName'],
                                user=config['DEFAULT']['DataBaseUsername'], host=config['DEFAULT']['DataBaseHostname'], port=config['DEFAULT']['DataBasePort'], password=config['DEFAULT']['DataBasePassword'])
        cursor = conn.cursor()
    except BaseException as e:
        print("Can't connect to database: "+str(e))
        exit()

    for file in os.listdir(config['DEFAULT']['ApacheLogPath']):
        if "access.log" in file and not file.endswith(".gz"):
            try:
                f = open(config['DEFAULT']['ApacheLogPath'] +
                         ('/' if config['DEFAULT']['ApacheLogPath'][-1] != '/' else '')+file)
                for line in f.readlines():
                    entry = parser.parse(line)
                    cursor.execute("INSERT INTO logs SELECT %s, %s WHERE NOT EXISTS (SELECT address, date FROM logs WHERE address = %s AND date = %s);",
                                   (entry.remote_host, entry.request_time, entry.remote_host, entry.request_time,))
                    conn.commit()
                f.close()
            except BaseException as e:
                print(
                    f"Can't open Apache log at '{config['DEFAULT']['ApacheLogPath']}{'/' if config['DEFAULT']['ApacheLogPath'][-1] != '/' else ''}{file}': "+str(e))
                exit()
    cursor.close()
    conn.close()
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response




if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
