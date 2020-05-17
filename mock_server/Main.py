import os
from SSE.SSETx import *
from tests.mock import  *
from controller.DBControl import *
from time import sleep
from threading import Thread

def startThread(method):
     send_event_thread = Thread(target = method)
     send_event_thread.setName('Real-Time Thread')
     send_event_thread.start()

def main():

    #mock_server_port = get_free_port()
    mock_server_port = 8000
    start_mock_server(mock_server_port)
    exit = False
    send = SendEvent()
    startThread(send.start)
    while not exit:
        key = input('Press Q to quit...')
        if str(key) == 'Q' or str(key) == 'q':
            send.stopSend()
            sleep(1)
            exit = True
            break

if __name__ == '__main__':
    main()
