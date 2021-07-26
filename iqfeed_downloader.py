import socket
from sys import argv
# import iqfeed_settings


def connect_to_socket(host: str, port: int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print("Connection established!")
        return sock
    except Exception as e:
        print(e)
        print("Something went wrong while establishing the connection, check host/port input")


def close_socket(sock):
    try:
        sock.close()
        print("Connection closed")
    except Exception as e:
        print(e)
        print("Something went wrong while closing the connection")


def send_message_to_socket(sock, message: str):
    try:
        sock.sendall(bytes(message, "utf-8"))
        print("Message sent...")
    except Exception as e:
        print(e)
        print("Something went wrong while sending the message")


def receive_historical_data_socket(sock, recv_buffer=4096):
    """
    Read the information from the socket, in a buffered
    fashion, receiving only 4096 bytes at a time.
    Parameters:
    sock - The socket object
    recv_buffer - Amount in bytes to receive per read
    """
    buffer = ""
    data = ""
    try:
        while True:
            data = sock.recv(recv_buffer)
            data = str(data, "utf-8")
            buffer += data

            # Check if the end message string arrives
            if "!ENDMSG!" in buffer:
                break

        # Remove the end message string
        buffer = buffer[:-12]

        print("Data received...")
        return buffer
    except Exception as e:
        print(e)
        print("Something went wrong while receiving data")


def data_to_csv(data):
    try:
        f = open(f"{sym}_{start_date}_{end_date}_{interval}.csv", "w")
        f.write(data)
        f.close()
    except Exception as e:
        print(e)
        print("Something went wrong while dumping data")


def clean_data(data):
    data = "".join(data.split("\r"))
    data = data.replace(",\n", "\n")[:-1]
    return data


if __name__ == "__main__":
    try:
        host = argv[1]
        port = int(argv[2])
        start_date = argv[3]
        end_date = argv[4]
        interval = argv[5]
        tickers = argv[6:]
    except Exception as e:
        print(e)
        print("Something went wrong while parsing the arguments, used default settings instead")
#         host = iqfeed_settings.historical_server_ip
#         port = iqfeed_settings.historical_server_port
#         start_date = "20210715"
#         end_date = "20210719"
#         interval = "1"
#         tickers = ["TLRY"]
    
    sock = connect_to_socket(host, port)

    # Download each symbol to disk
    for sym in tickers:
        print(f"Downloading symbol: {sym}...")

        # Construct the message needed by IQFeed to retrieve data
        message = f"HIT,{sym},{interval},{start_date},{end_date},,093000,160000,1\n"

        # Encode and send the message
        send_message_to_socket(sock, message)

        # Receive the historical data
        data = receive_historical_data_socket(sock)

        # Prepare the data for CSV dump
        data = clean_data(data)

        # Write the data stream to disk
        data_to_csv(data)

    close_socket(sock)
