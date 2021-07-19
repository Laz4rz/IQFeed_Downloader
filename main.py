import sys
import socket


def read_historical_data_socket(sock, recv_buffer=4096):
    """
    Read the information from the socket, in a buffered
    fashion, receiving only 4096 bytes at a time.

    Parameters:
    sock - The socket object
    recv_buffer - Amount in bytes to receive per read
    """
    buffer = ""
    data = ""
    while True:
        data = sock.recv(recv_buffer)
        data = str(data, 'utf-8')
        buffer += data

        # Check if the end message string arrives
        if "!ENDMSG!" in buffer:
            break

    # Remove the end message string
    buffer = buffer[:-12]
    return buffer


if __name__ == "__main__":
    # Define server host, port and symbols to download
    host = "6.tcp.ngrok.io"  # Localhost
    port = 13876  # Historical data socket port
    syms = ["TLRY"]

    # Download each symbol to disk
    for sym in syms:
        print(f"Downloading symbol: {sym}...")

        # Construct the message needed by IQFeed to retrieve data
        message = f"HIT,{sym},60,20140101 075000,,,093000,160000,1\n"

        # Open a streaming socket to the IQFeed server locally
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        # Send the historical data request
        # message and buffer the data
        sock.sendall(bytes(message, 'utf-8'))
        data = read_historical_data_socket(sock)
        sock.close()

        # Remove all the endlines and line-ending
        # comma delimiter from each record
        data = "".join(data.split("\r"))
        data = data.replace(",\n","\n")[:-1]

        # Write the data stream to disk
        f = open(f"{sym}.csv", "w")
        f.write(data)
        f.close()
