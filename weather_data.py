import requests  
import time  
import datetime
import pytz
import os

data_hoursofday = []
time_criteria = None
keys = ['YYMMDDHHMI', 'STN', 'WD1', 'WS1', 'WDS', 'WSS', 'WD10', 'WS10', 'TA', 'RE', 'RN-15m', 'RN-60m', 'RN-12H', 'RN-DAY', 'HM', 'PA', 'PS', 'TD']
cache_directory = 'Cache'
data_cache = {}


def load_cached_files():
    if not os.path.exists(cache_directory):
        os.makedirs(cache_directory)
    for file in os.listdir(cache_directory):
        if file.startswith('data') and file.endswith('.txt'):
            data_cache[file] = open(cache_directory + '/' + file, 'r').read()


def download_file(file_url, filename):
    path = cache_directory + '/' + filename
    print('Downloading: %s' % filename)
    with open(path, 'wb') as f: # Open file to be saved in binary write mode
        response = requests.get(file_url) # Send GET request to file URL
        f.write(response.content) # Write contents of response to file
    data_cache[filename] = open(path, 'r').read()


def get_file(time_str):
    filename = 'data%s.txt' % time_str
    if filename not in data_cache:
        url = 'https://apihub.kma.go.kr/api/typ01/cgi-bin/url/nph-aws2_min?stn=0&tm2=%s&disp=1&help=1&authKey=Ud0jPfajTAWdIz32o5wFcg' % time_str
        download_file(url, filename)
    else:
        print('Using cached file: %s' % filename)
    return data_cache[filename]


def process_file(file_content):
    data = dict()
    lines = file_content.split('\n')
    for line in lines:
        if line.startswith('#'):
            continue
        info = line.split(',')
        if info[-1] == '=':
            for i in range(2, 18):
                info[i] = float(info[i])
                info[i] = float('NaN') if info[i] <= -50.0 else info[i]
            data[info[1]] = dict(zip(keys, info))
    return data


def initialize():
    global time_criteria
    # Call file download function
    load_cached_files()

    # current time to KST
    time_criteria = datetime.datetime.now(pytz.timezone('Asia/Seoul'))
    time_criteria -= datetime.timedelta(minutes=1)
    time_criteria = time_criteria.replace(minute=0, second=0, microsecond=0)

    for hour_delta in range(0, 24):
        target_time = time_criteria - datetime.timedelta(hours=hour_delta)
        target_time_str = target_time.strftime('%Y%m%d%H%M')
        content = get_file(target_time_str)
        data = process_file(content)
        data_hoursofday.insert(0, data)