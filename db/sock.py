import os
import time
import thread

import websocket

import predix.security.uaa

import json

from termcolor import colored


cam_dict = {}
color_dict = {1: 'blue',
2: 'aqua',
3: 'yellow',
4: 'red',
}

def on_message(ws, message):
    m = json.loads(message)

    cam = m['locationUid']

    if m['locationUid'] not in cam_dict:
        cam_dict[cam] = [m['properties']['geoCoordinates'], 0]

    if (m['eventType'] == 'PKIN'):
        cam_dict[cam][1] += 1
    elif cam_dict[cam][1] != 0:
        cam_dict[cam][1] -= 1

    for item in cam_dict:
        print(colored(item, color_dict[item[1]]))

def on_close(ws):
    print('### closed ###')

def on_open(ws):
    #print('### connected ###')
    ws.send('{"bbox":"32.715675:-117.161230,32.708498:-117.151681","eventTypes":["PKIN","PKOUT"]}')

if __name__ == '__main__':
    websocket.enableTrace(True)

    # Use Predix-Zone-ID to match events of interest
    cityiq_zone = 'SDSIM-IE-PARKING'

    cityiq = 'wss://ic-websocket-service.run.aws-usw02-pr.ice.predix.io/events'
    token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImxlZ2FjeS10b2tlbi1rZXkiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIxYmJlNDgyZTQ2MTY0ZTNhOGRhZGMxYTlkNzllNjMwNSIsInN1YiI6ImhhY2thdGhvbiIsInNjb3BlIjpbInVhYS5yZXNvdXJjZSIsImllLWN1cnJlbnQuU0RTSU0tSUUtUFVCTElDLVNBRkVUWS5JRS1QVUJMSUMtU0FGRVRZLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEFSS0lORy5JRS1QQVJLSU5HLkxJTUlURUQuREVWRUxPUCIsImllLWN1cnJlbnQuU0RTSU0tSUUtUEVERVNUUklBTi5JRS1QRURFU1RSSUFOLkxJTUlURUQuREVWRUxPUCJdLCJjbGllbnRfaWQiOiJoYWNrYXRob24iLCJjaWQiOiJoYWNrYXRob24iLCJhenAiOiJoYWNrYXRob24iLCJncmFudF90eXBlIjoiY2xpZW50X2NyZWRlbnRpYWxzIiwicmV2X3NpZyI6IjlmMWYyYzRkIiwiaWF0IjoxNTA5MjUwMzExLCJleHAiOjE1MDk4NTUxMTEsImlzcyI6Imh0dHBzOi8vODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3LnByZWRpeC11YWEucnVuLmF3cy11c3cwMi1wci5pY2UucHJlZGl4LmlvL29hdXRoL3Rva2VuIiwiemlkIjoiODkwNDA3ZDctZTYxNy00ZDcwLTk4NWYtMDE3OTJkNjkzMzg3IiwiYXVkIjpbImllLWN1cnJlbnQuU0RTSU0tSUUtVFJBRkZJQy5JRS1UUkFGRklDLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBBUktJTkcuSUUtUEFSS0lORy5MSU1JVEVEIiwiaWUtY3VycmVudC5TRFNJTS1JRS1QVUJMSUMtU0FGRVRZLklFLVBVQkxJQy1TQUZFVFkuTElNSVRFRCIsInVhYSIsImhhY2thdGhvbiIsImllLWN1cnJlbnQuU0RTSU0tSUUtRU5WSVJPTk1FTlRBTC5JRS1FTlZJUk9OTUVOVEFMLkxJTUlURUQiLCJpZS1jdXJyZW50LlNEU0lNLUlFLVBFREVTVFJJQU4uSUUtUEVERVNUUklBTi5MSU1JVEVEIl19.VhnBkYuCCzGuSfHKVAlKZ9TqmyT2vWCymqmkQ0N1mrv1mvW3lGqZ6fuozYesKooSZhSxthbK3mwyEFp5LzFuJbybaErSXn0eNI3YMJOPFyr11oiDZ6d-QTt_GSMLgCVcWZth0In8UhVXeC13_EKBu9X57VFmvpwU2SaEgQddVKx11RMpESIFPfroOG1lqEpCgbd-6J0f61j9R2kPk4iOV8C_za7f-vyKPRoOGJASzNhqtEC7tK7MFd1zEGQ_QJwyQy4Zu7svX8s-4aJJEupqXlcDX1-UFZ74X30qf85zRwQEurOBq7Sna8MIjbtH8VYzqGT_dj3SynQdFF1wp-SBuA'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Predix-Zone-Id': cityiq_zone,
        'Cache-Control': 'no-cache',
        '':''
            }
    ws = websocket.WebSocketApp(cityiq,
            header = headers,
            on_message = on_message,
            on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
