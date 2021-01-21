To run the project, please run 'main.py' using Python 3+
BlackBox "generator-macosx-amd64" should be in the same folder as scripts.
Stats can be viewed in web browser at localhost:8000
Last minute stats can be viewed in web browser at localhost:8000/addlastminute

Main is initialzing the stream_reader thread which is consuming the event-data from blackbox
In addition, it is starting a simple web server which exposes via http stats collected over time

Stats holds 4 dictionaries and one int - shared threw the other scripts:
- 2 default int dictionaries for counting total evets and words
- 2 default list dictionaries - holding a timestamp list for each word/event - in order to filter last minute
the last minute stats may be called rarely therefore it should filter itself every
two minutes for making the run time fast when called (and not having to filter all events and words)

- a total lines int for counting total lines and making stats computing faster
this is taking an asumption that evets and words are as number as lines output from the stream (one word and event each line)

Stream Reader is responsible for reading the json stream and fill in the stats dictionaries

Tnx
Ziv
