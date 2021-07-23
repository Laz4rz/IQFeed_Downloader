import socket
from sys import argv
# import iqfeed_settings


def connect_to_socket(server_ip: str, server_port: int):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect((server_ip, server_port))
        print('Connection established!')
        return server
    except Exception as e:
        print(e)
        print('Something went wrong while establishing the connection, check host/port input')


def close_socket(server):
    try:
        server.close()
        print('Connection closed')
    except Exception as e:
        print(e)
        print('Something went wrong while closing the connection')


def clean_data(data):
    data = "".join(data.split("\r"))
    data = data.replace(",\n","\n")[:-1]
    return data


def establish_live_feed(ticker: str):
    try:
        sock.sendall(bytes(f"S,TIMESTAMPSOFF\n", 'utf-8'))
        sock.sendall(bytes(f"w{ticker}\n", 'utf-8'))
        while True:
            print(clean_data(str(sock.recv(4096), 'utf-8')))
    except Exception as e:
        print(e)
        print("Something went wrong while establishing the connection")


if __name__ == "__main__":
    try:
        ip = argv[1]
        port = int(argv[2])
        ticker = argv[3]
    except Exception as e:
#         print('Something went wrong while parsing the arguments, used default settings instead')
#         ip = iqfeed_settings.server_ip
#         port = iqfeed_settings.server_port
#         ticker = 'SPY'
        pass

    sock = connect_to_socket(ip, port)
    establish_live_feed(ticker)
    close_socket(sock)
