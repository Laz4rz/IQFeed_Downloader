# IQFeed Downloader

Python scripts created to use with DTN IQFeed Market Data application. Connect to IQFeed socket, download historical data or start a live flow of prices for desired ticker.


## How to use?

1. Clone the repository or download both files.
2. Log into any IQFeed application and have it running in the background - make sure you've bought the data plan that contains desired ticker. 
3. Run the script.


## Running the script

There are two ways of running the script and here are the examples:
- historical data access
'''
python iqfeed_downloader historical 127.0.0.1 9100 20210201 20210220 1 TLRY GME
'''
- live data access
'''
python iqfeed_downloader live 127.0.0.1 5009 AMC
'''


