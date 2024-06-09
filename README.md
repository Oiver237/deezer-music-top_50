## Requirements
Python 3.x

## Description
This project is a Python script that processes daily log files of streams from Deezer to compute the top 50 songs most listened to in each country over the last 7 days. The results are saved as text files, one per day.

## Script Details
### log_processing(date_str)
Processes the log file for a given date:
- Reads the log file from logs/
- Ignores corrupted rows
- Counts song plays per country
- Saves the counts to a staging file in staging/

### get_the_last_seven_days(date_str)
Returns a list of the last 7 days' dates in YYYYMMDD format.

### top_50(date_str)
Generates the top 50 songs per country for the last 7 days:
- Reads counts from staging files
- Aggregates counts for each country
- Writes the top 50 songs to an output file in output/

## Installation
1. Clone the repository (https://github.com/Oiver237/deezer-music-top_50)
I can add you as collaborator

2. Create and activate a virtual environment:

3. Install the dependencies using requirements.txt file

### Testing
To test the functionality, run the test script test.py
The test script verifies the directory creation, log processing, and generation of the top 50 songs.

### Usage
1. Place the daily log files in the logs/ directory. The log files should be named listen-YYYYMMDD.log and contain rows formatted as sng_id|user_id|country.

2. Run the application:
 ```sh
    python script2.py
```

3. Check the output in the output/ directory for the file country_top50_YYYYMMDD.txt, which contains the top 50 songs per country for the last 7 days.
