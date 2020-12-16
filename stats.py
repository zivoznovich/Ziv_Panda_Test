from collections import defaultdict


class Stats:
    def __init__(self):
        # Two int dict for the counting of events and words - total
        self.events_counter_int, self.data_words_counter_int = defaultdict(int), defaultdict(int)
        # Two list dict for counting of events and words with it's timestamp - in order to filter 60 sec
        self.events_counter_list, self.data_words_counter_list = defaultdict(list), defaultdict(list)
        
        # This variable will help to reduce computation effort
        self.total_lines = 0