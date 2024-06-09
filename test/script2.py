import os
from datetime import datetime, timedelta
import csv
import time
import psutil


#getting the process id
pid = os.getpid()
py = psutil.Process(pid)

#getting the cpu and memory usage
cpu_start = py.cpu_times()
mem_start = py.memory_info().rss /(1024*1024)


start_time= time.time()

#Creating the directories in case they don't exist
def check_directories():
    os.makedirs('staging', exist_ok=True)
    os.makedirs('output', exist_ok=True)

def log_processing(date_str):
    #initializing the count dictionary
    count = {}
    log_file = f'logs/listen-{date_str}.log'
    
    with open(log_file, 'r') as log:
        reader = csv.reader(log, delimiter='|')
        for row in reader:
            #ignoring the corrupted rows
            if len(row) != 3:
                print(f"Corrupted row: {row}")
                continue 
            sng_id, _, country = row #skipping the user_id since we don't need it
            #striping the white spaces
            country = country.strip()
            sng_id = sng_id.strip()
            #Removing the country with more than 2 characters and its not uppercase
            if len(country) > 2 or country != country.upper():
                print(f"Invalid country code: {country}")
                continue
            #adding the country and song id to the count dictionary
            if country not in count:
                count[country] = {}
            if sng_id not in count[country]:
                count[country][sng_id] = 0
            count[country][sng_id] += 1
            
    count_file = f'/home/lifu237/deezer-interview/staging/counts-{date_str}.csv'
    with open(count_file, 'w') as file:
        writer = csv.writer(file)
        for country, songs in count.items():
            for song, c in songs.items():
                writer.writerow([country, song, c])
                
    print(f"Count dictionary: {count}")
    print(f"Staging file written: {count_file}")

def get_the_last_seven_days(date_str):
    date = datetime.strptime(date_str, '%Y%m%d')
    return [(date - timedelta(days=i)).strftime('%Y%m%d') for i in range(7)]

def top_50(date_str):
    last_seven_days = get_the_last_seven_days(date_str)
    count = {}
    
    for date in last_seven_days:
        staging_file = f'/home/lifu237/deezer-interview/staging/counts-{date}.csv'
        if os.path.exists(staging_file):
            with open(staging_file, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    country, song, c = row
                    if country not in count:
                        count[country] = {}
                    if song not in count[country]:
                        count[country][song] = 0
                    count[country][song] += int(c)
                
    output_file = f'/home/lifu237/deezer-interview/output/country_top50_{date_str}.txt'
    with open(output_file, 'w') as file:
        for country, songs in count.items():
            # Sort the songs by count in descending order and take the top 50
            top_songs = sorted(songs.items(), key=lambda x: x[1], reverse=True)[:50]
            # Format the songs as 'sng_id:n'
            top_songs_str = ','.join(f'{sng_id}:{n}' for sng_id, n in top_songs)
            file.write(f'{country}|{top_songs_str}\n')

if __name__ == '__main__':
    check_directories()
    today = datetime.now().strftime("%Y%m%d")
    log_processing(today)
    top_50(today)


end_time = time.time()

cpu_end = py.cpu_times()
mem_end = py.memory_info().rss /(1024*1024)

cpu_usage = {
    'user': cpu_end.user - cpu_start.user,
    'system': cpu_end.system - cpu_start.system,
    'children_user': cpu_end.children_user - cpu_start.children_user,
    'children_system': cpu_end.children_system - cpu_start.children_system,
    'iowait': cpu_end.iowait - cpu_start.iowait if hasattr(cpu_end, 'iowait') else 0.0
}

print(f"Execution time: {end_time - start_time} seconds")
print(f"CPU usage: {cpu_usage}")
print(f"Memory usage: {mem_end - mem_start} MB")
