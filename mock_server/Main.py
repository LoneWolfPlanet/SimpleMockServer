import os
from tests.mock import  *

def main():

    #mock_server_port = get_free_port()
    mock_server_port = 8000
    start_mock_server(mock_server_port)
    exit = False
    while not exit:
        key = input('Press Q to quit...')
        if str(key) == 'Q' or str(key) == 'q':
            exit = True
            break

if __name__ == '__main__':
    main()
