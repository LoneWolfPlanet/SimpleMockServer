import psycopg2
from configparser import ConfigParser

class DBCntl():

    def __init__(self):
            self.ini_path = './Configuration/database.ini'
            self.ini_section = 'postgresql'
            self.param = self.get_credentials()

    def connect(self):
        conn = None
        try:
            #conn = psycopg2.connect("dbname=cbs user=postgres password=12345")
            conn = psycopg2.connect(** self.param )
            cur = conn.cursor()
            command = [ "CREATE TABLE IF NOT EXISTS tbClientInfo(  id SERIAL PRIMARY KEY  , " +\
                      "  username VARCHAR(255) NOT NULL , password VARCHAR(255) NOT NULL )",
                        "CREATE TABLE IF NOT EXISTS  tbCommunication(id SERIAL PRIMARY KEY, " + \
                        "communicationID VARCHAR(255) NOT NULL , data TEXT )"
                      ]
            for co in command:
                cur.execute(co)
            cur.close()
            conn.commit()
        except Exception as e:
            pass
        finally:
            if conn:
                conn.close()

    def insert(self):
        conn = psycopg2.connect(**self.param)
        cur = conn.cursor()
        insert = "INSERT INTO tbClientInfo (username, password ) VALUES ( %s ,%s)"
        cur.execute(insert, ('Antet', '12345', ))

        insert = "INSERT INTO tbCommunication(communicationID, data) VALUES(%s, %s)"
        cur.execute(insert, ('000001', 'こんにちは道路、これは緊急ホットラインですか？第11地区カムニン道路沿いの 三菱とマツダ3両が 衝突して渋 滞しているとのことです。',))
        cur.close()
        conn.commit()

    def update(self):
        conn = None
        try:
            conn = psycopg2.connect(**self.param)
            cur = conn.cursor()
            update = 'UPDATE tbClientInfo set username = %s  WHERE id = 2'
            cur.execute(update,('David', ))
            cur.close()
            conn.commit()
        except Exception as e:
            pass
        finally:
            if conn:
                conn.close()

    def search(self):
        conn = None
        try:
            conn = psycopg2.connect(**self.param)
            cur = conn.cursor()
            query = "SELECT * FROM tbClientInfo;"
            cur.execute(query)
            result = cur.fetchall()
            if result:
                print('Has values')
            cur.close()
        except Exception as e:
            pass
        finally:
            if conn:
                conn.close()

    def get_credentials(self):
        # create a parser
        parser = ConfigParser()
        # read config file
        parser.read(self.ini_path)

        # get section, default to postgresql
        db = {}
        if parser.has_section(self.ini_section):
            params = parser.items(self.ini_section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self.ini_section, self.ini_path ))

        return db