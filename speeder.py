#Author: Daniel Morales
#Version: 1.0
#Description: Automates speedtest usiong librespeed and insert results into a DB backend

#Import section
import argparse
import subprocess
import pyfiglet
import logging
import json
import signal
import os
from socket import gethostname
import time
import mariadb
from mariadb import Error

#Handling user press ctrl-c
def user_abort(sig, frame):
    print("\n\n[+] User aborted execution")
    exit(0)

signal.signal(signal.SIGINT,user_abort)

#Main class
class Speeder:
    def __init__(self):
        self.args = self.parse_arguments()
        self.run()

    #Argument parser
    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Speeder - Automatic Speedtest daemon")
        parser.add_argument('-t','--targets', help="Path to the custom speedtest server list",required=True)
        parser.add_argument('-d','--database', help="Path to database config file",required=True)
        parser.add_argument('-f','--freq', type=int, help="Speed test frequency, specified in seconds. Default run test every 300 seconds.", default=300)
        args = parser.parse_args()
        return args
    
    #Database connection
    def get_db_connection(self):
        try:
            #Read db config file
            with open(os.path.join(self.args.database), 'r', encoding='UTF-8') as file:
                params =json.load(file)
            db_host = params[0]['DB_HOST']
            db_user = params[0]['DB_USER']
            db_password = params[0]['DB_PASSWORD']
            db_name = params[0]['DB_NAME']
            connection = mariadb.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name
            )
            if connection is not None:
                print("\t[+] Database connection successful")
                return connection
        except Error as e:
            print("\n[*] ERROR: can not connect to database",e)
            return None
        except FileNotFoundError:
            logging.error("\n[*] ERROR: File not found")
            exit(1)
        except json.JSONDecodeError:
            logging.error("\n[*] ERROR: Can not decode JSON file")
            exit(1)
        
     #Database query   
    def execute_query(self, query, params):
        connection = self.get_db_connection()
        if connection is None:
            exit(1)
        try:
            cursor = connection.cursor()
            cursor.execute(query, params)
            connection.commit()
            print("\t[+] Query executed successfully")
        except Error as e:
            print(f"[*] ERROR: {e}")
        finally:
            if connection is not None:
                cursor.close()
                connection.close()
                print("\t[+] Connection closed")


    #Main method
    def run(self):
        try:
            os.system("clear")
            print(pyfiglet.figlet_format('SPEEDER','slant'),"v0.1\n")
            print("[+] Daemon is running...")
            while True:
                print("\n\t[+] Launching speedtest...")
                result = subprocess.run(['librespeed-cli', '--local-json', self.args.targets, '--telemetry-level', 'disabled', '--json'], capture_output=True, text=True)
                json_result = json.loads(result.stdout)
                query = "INSERT INTO measures (timestamp, client, server, ping, jitter, upload, download) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                params = (json_result[0]['timestamp'], gethostname(), json_result[0]['server']['name'],int(json_result[0]['ping']), int(json_result[0]['jitter']), float(json_result[0]['upload']), float(json_result[0]['download']))
                self.execute_query(query, params)
                time.sleep(self.args.freq)
        except Exception as e:
            print(f'[*] ERROR: {e}')
            exit(1)

    
if __name__ == "__main__":
    Speeder()
