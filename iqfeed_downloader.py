from typing import List

import typer

from iqfeed_utils import (
    connect_to_socket, send_message_to_socket, receive_data, clean_data, data_to_csv,
    close_socket, establish_live_feed
    )

app = typer.Typer()


@app.command()
def historical(
    host: str,
    port: int,
    start_date: str,
    end_date: str,
    interval: str,
    tickers: List[str],
):
    """
    Historical lets you download historical data for a desired set of tickers between start/end date with custom candles
    interval and then save it in a file with name made of set parameters, each ticker gets it's own file
    :param host: IQFeed socket address
    :param port: IQFeed socket port
    :param start_date: Start date of data to download in YYYYMMDD format
    :param end_date: End date of data to download in YYYYMMDD format
    :param interval: Interval of data to download in seconds
    :param tickers: List of tickers to download the data for
    """
    sock = connect_to_socket(host=host, port=port)
    sock.sendall(bytes("S,SET PROTOCOL 6.1\n", "utf-8"))

    for sym in tickers:
        print(f"Downloading symbol: {sym}...")

        message = (
            f"HTT,{sym},{interval},{start_date} 093000,{end_date} 160000\n"
            if interval == "TICK"
            else f"HIT,{sym},{interval},{start_date} 093000,{end_date} 160000\n"
        )

        send_message_to_socket(sock=sock, message=message)
        data = receive_data(sock=sock)
        data = clean_data(data=data)
        data_to_csv(data=data, sym=sym, start_date=start_date, end_date=end_date, interval=interval)

    close_socket(sock)


@app.command()
def live(host: str, port: int, ticker: str):
    """
    Live lets you establish a live flow of desired ticker's prices
    :param host: IQFeed socket address
    :param port: IQFeed socket port
    :param ticker: Ticker name that you wish to follow
    :return: Streams a price flow
    """
    sock = connect_to_socket(host=host, port=port)
    establish_live_feed(sock=sock, ticker_name=ticker)


if __name__ == "__main__":
    app()
