import socket


def connect_to_socket(host: str, port: int) -> socket.socket:
    """
    Establishes connection to the IQFeed socket - socket is made by the IQFeed app after you properly log in
    :param host: IQFeed socket address
    :param port: IQFeed socket port
    :return: Returns socket object
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print("Connection established!")
    return sock


def close_socket(sock: socket.socket) -> None:
    """
    Closes the socket connection
    :param sock: The socket object
    """
    sock.close()
    print("Connection closed")


def send_message_to_socket(sock: socket.socket, message: str) -> None:
    """
    Sends a message - request - to a socket
    :param sock: The socket object
    :param message: Request in string format
    """
    sock.sendall(bytes(message, "utf-8"))
    print("Message sent...")


def receive_data(sock: socket.socket, recv_buffer=4096) -> str:
    """
    Read the information from the socket, in a buffered
    fashion, receiving only 4096 bytes at a time.
    :param sock: The socket object
    :param recv_buffer: Amount in bytes to receive per read
    """
    buffer = ""
    data = ""
    while True:
        data = sock.recv(recv_buffer)
        data = str(data, "utf-8")
        buffer += data

        if "!ENDMSG!" in buffer:
            break

    buffer = buffer[:-12]

    print("Data received...")
    return buffer


def data_to_csv(data: str, sym: str, start_date: str, end_date: str, interval: str) -> None:
    """
    Writes the data in a file with custom file name
    :param data: String to save in a file
    :param sym: Ticker name that the data belongs to
    :param start_date: Starting date of contained data
    :param end_date: Ending date of contained data
    :param interval: Interval in seconds of contained data
    """
    f = open(f"{sym}_{start_date}_{end_date}_{interval}.csv", "w")
    f.write(data)
    f.close()


def clean_data(data: str) -> str:
    """
    Does basic string operations to make the data more readable
    :param data: Data string
    :return: Cleared data
    """
    data = "".join(data.split("\r"))
    data = data.replace(",\n", "\n")[:-1]
    return data


def establish_live_feed(sock: socket.socket, ticker_name: str) -> None:
    """
    Establishes live feed with stock data of desired ticker, runs constantly as a print with current data
    :param sock: The socket object
    :param ticker_name: Ticker name you want to see live data for
    """
    sock.sendall(bytes(f"S,TIMESTAMPSOFF\n", "utf-8"))
    sock.sendall(bytes(f"w{ticker_name}\n", "utf-8"))
    while True:
        print(clean_data(str(sock.recv(4096), "utf-8")))

