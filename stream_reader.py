
import json
import subprocess
from datetime import datetime

# Stream_Reader is responsible on reading the json stream and fill in the stats object
class Stream_Reader():
    def __init__(self, stats):
        self.stats = stats
        
    def start(self, terminate_thread):
        #this is the stream consuming function
        print("start: Stream thread has started")
        
        process = subprocess.Popen("./generator-macosx-amd64", stdout=subprocess.PIPE)
        event_type = 'event_type'
        data = 'data'
        timestamp = 'timestamp'
        
        secondsToKeep = 120
        timeLastCleaned = datetime.timestamp(datetime.now())
        
        while not terminate_thread():
            line = process.stdout.readline()

            # Handling corrupted lines by catching UnicodeDecodeError and json.JSONDecodeError (and ignoring)
            try:
                json_line = json.loads(line)
                
                # Two default int dictionaries counts the total events and words by name/key 
                self.stats.events_counter_int[json_line[event_type]] += 1
                self.stats.data_words_counter_int[json_line[data]] += 1
                
                # Two default list dictionaries consumes timestamps to a list by name/key
                # This is for lastet filtering stats by timestamp
                self.stats.events_counter_list[json_line[event_type]].append(json_line[timestamp])
                self.stats.data_words_counter_list[json_line[data]].append(json_line[timestamp])
        
                # This variable will help to reduce computation effort
                self.stats.total_lines += 1

                # Clean the last minute data: By cleaning all data older than 2 minutes, we guarantee that 
                # this data won't consume redunant memory in case the server will run for a while, without addlastminute 
                # will be called
                # I'm cleaning anything older than 2 last minutes, and not 1, to avoid cleaning cruical information if the Get request will
                # arrive in the same time
                timeNow = datetime.timestamp(datetime.now())
                if timeLastCleaned + secondsToKeep < timeNow:
                    timeLastCleaned = timeNow
                    for key in self.stats.events_counter_list:
                        self.stats.events_counter_list[key] = list(filter(lambda curr_stamp: timeNow-curr_stamp <= secondsToKeep, self.stats.events_counter_list[key]))
                    for key in self.stats.data_words_counter_list:
                        self.stats.data_words_counter_list[key] = list(filter(lambda curr_stamp: timeNow-curr_stamp <= secondsToKeep, self.stats.data_words_counter_list[key]))
            
            except (UnicodeDecodeError, json.JSONDecodeError) :
                pass

        print("Stream thread terminated")



