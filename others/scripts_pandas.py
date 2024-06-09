import os
from datetime import datetime, timedelta
import time
import psutil
import pandas as pd

pid = os.getpid()
py = psutil.Process(pid) 

cpu_start = py.cpu_times()
mem_start = py.memory_info().rss / (1024 * 1024)

start_time = time.time()

def process_log(date_str):
    log_file = f'logs/listen-{date_str}.log'
    df = pd.read_csv(log_file, delimiter='|', names=['sng_id', 'user_id', 'country'], skipinitialspace=True, on_bad_lines='skip')
    df = df.drop(columns=['user_id'])
    df = df.dropna()
    df = df[df['country'].str.len() == 2]
    df['country'] = df['country'].str.upper()
    counts = df.groupby(['country', 'sng_id']).size().reset_index(name='counts')
    counts = counts.sort_values(by='counts', ascending=False)
    os.makedirs('staging', exist_ok=True)
    count_file = f'staging/counts-{date_str}.csv'
    counts.to_csv(count_file, index=False)

def get_last_seven_days(date_str):
    date = datetime.strptime(date_str, '%Y%m%d')
    return [(date - timedelta(days=i)).strftime('%Y%m%d') for i in range(7)]

def top_50(date_str):
    last_seven_days = get_last_seven_days(date_str)
    counts = pd.DataFrame()

    for date in last_seven_days:
        count_file = f'staging/counts-{date}.csv'
        if os.path.exists(count_file):
            df = pd.read_csv(count_file)
            counts = pd.concat([counts, df], ignore_index=True)

    counts = counts.groupby(['country', 'sng_id']).sum().reset_index()
    counts = counts.sort_values(['country', 'counts'], ascending=[True, False])
    top_50_counts = counts.groupby('country').head(50)

    top_50_grouped = top_50_counts.groupby('country').apply(
        lambda x: ','.join(f'{row.sng_id}:{row.counts}' for row in x.itertuples())
    ).reset_index(name='songs')

    os.makedirs('output', exist_ok=True)
    output_file = f'output/country_top50_{date_str}.txt'
    with open(output_file, 'w') as f:
        for _, row in top_50_grouped.iterrows():
            f.write(f"{row['country']}|{row['songs']}\n")

if __name__ == '__main__':
    today = datetime.now().strftime("%Y%m%d")
    process_log(today)
    top_50(today)

end_time = time.time()

cpu_end = py.cpu_times()
mem_end = py.memory_info().rss / (1024 * 1024)

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
