
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from stats import Stats
from stream_reader import Stream_Reader

'''
Main is initialzing the stream_reader which is consuming the event-data output of a stream generator (json encoded).
In addition, it is starting a simple web server which exposes via http stats collected over time.
There is an option to read stats in the last 60 seconds by adding url path "/addlastminute"
'''

def main():
    print("Main: started.")
    
    stream_reader = Stream_Reader(stats)

    # opening a backround thread for consuming the stream generator
    terminate_thread = False
    input_thread = threading.Thread(target=stream_reader.start, args=(lambda : terminate_thread, ))
    input_thread.start()

    start_server()

    # this code line will be executed only if the server was closed
    # in this case I will terminate the stream read thread
    terminate_thread = True
    input_thread.join()


# start_server method is initializing the server which listens on http://localhost:8000
def start_server():
    PORT = 8000
    server = HTTPServer(('', PORT), Http_Handler)
    
    print(f'Server is running on port {PORT}')
    try:
    	server.serve_forever()
    	
    except KeyboardInterrupt:
    	print ("KeyboardInterrupt, server down")
    	server.server_close()

# Http_Handler is a simple handler to listen GET requests and fetch the relevant statistics from Stats object
class Http_Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("do_GET: GET request has been called")
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

        # Creating a string of stats
        event_out = self.stat_creator(stats.events_counter_int)
        data_words_out = self.stat_creator(stats.data_words_counter_int)
        total_output = f'<br>TOTAL EVENTS:<br>{event_out}<br>TOTAL DATA WORDS:<br>{data_words_out}'
        
        self.wfile.write(total_output.encode())
        print(f"do_GET: Returned HTTP response with the statistics: {total_output}")
        
        # Adding the statistics for the last minute
        if self.path == "/addlastminute":
            print(f"do_GET: Path addlastminute has been requested: {datetime.now().time()}")
            
            now_stamp = datetime.timestamp(datetime.now())
            minute_event = self.last_minute_filter(now_stamp, stats.events_counter_list)
            minute_data_word = self.last_minute_filter(now_stamp, stats.data_words_counter_list)
            minute_output = f'<br>LAST MINUTE EVENTS:<br>{minute_event}<br>LAST MINUTE DATA WORDS:<br>{minute_data_word}'
            
            self.wfile.write(minute_output.encode())
            print(f"do_GET: Returned HTTP response with the last minute statistics: {minute_output}")

    # stat_creator function counts total events/words in the dictionary and calculates percentage    
    def stat_creator(self, int_dict):
        string_list = []
        total = stats.total_lines
        print(f"stat_creator: Starting to compute statistics. Total lines so far: {total}")

        for key in int_dict:
            percentage = (100*int_dict[key]//total)
            string_list.append(f'{key}: {percentage}% ({int_dict[key]})')
        return string_list

    # last_minute_filter filters all timestamps of the dictionary values that are older than 60 sec
    def last_minute_filter(self, now_stamp, list_dict):
        print(f"last_minute_filter: Starting to compute statistics for the last minute: {datetime.now().time()}")
        string_list = []
        total = 0
        for key in list_dict:
            # 60 seconds time filter
            list_dict[key] = list(filter(lambda curr_stamp: now_stamp-curr_stamp <= 60, list_dict[key]))
            
            # Count total events/words
            total += len(list_dict[key])

        # This loops and calculates percentage
        for key in list_dict:
            amount_number = len(list_dict[key])
            percentage = 100 * amount_number // total
            string_list.append(f'{key}: {percentage}% ({amount_number})')
        return string_list

if __name__ == '__main__':
    # Stats class will be used to store all the relevant statistics
    stats = Stats()

    main()