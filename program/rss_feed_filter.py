import configparser
import os
import datetime
import feedparser

print('Running RSS program.')

def insert_string(file_obj, str_match, str_insert):
    buffer = file_obj.readlines()
    for index, line in enumerate(buffer):
            if str_match in line:
                buffer.insert(index + 1, str_insert)
                break
    file_obj.seek(0)
    file_obj.writelines(buffer)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
config.read(BASE_DIR + '/program/config.ini')
sections = config.sections()

if not ('RSSLinks' in sections and 
        'Keywords' in sections and 
        'Authors' in sections and 
        'Files' in sections):
        raise ValueError('Config file incomplete.')

file_log = BASE_DIR + '/' + config['Files']['log']
file_output = BASE_DIR + '/' + config['Files']['output']

if not os.path.isfile(file_log):
    with open(file_log, 'wt') as f:
        f.write('RSS publication titles posted:\n')

if not os.path.isfile(file_output):
    with open(file_output, 'wt') as f:
        html_base = ['<!DOCTYPE html>\n',
                     '<html>\n',
                     '<head>\n',
                     '<h1>Filtered Publications - Hot off of RSS!</h1>\n',
                     '</head>\n',
                     '<body>\n',
                     '</body>\n',
                     '</html>']

        f.writelines(html_base)

today = datetime.date.today()
date_string = f'{today.year} / {today.month} / {today.day}'
date_insert = '<h2>' + date_string + '</h2>\n'

with open(file_output, 'r+t') as f:
    if date_insert not in f.read():
        f.seek(0)
        insert_string(f,'<body>',date_insert)


with open(file_log,'rt') as f:
    titles_logged = [line.replace('\n', '') for line in f.readlines()]

feed_list = [config['RSSLinks'][key] for key in config['RSSLinks']]
keyword_list = config['Keywords']['keyword_list'].replace('\n','').split(';')
author_list = config['Authors']['author_list'].replace('\n','').split(';')
i = 0

for feed in feed_list:
    d = feedparser.parse(feed)
        
    for entry in d.entries:
        title = entry.title.replace('\n', ' ').replace('\r', '')

        if title not in titles_logged:
            append_title = False

            if sum([keyword.casefold() in title for keyword in keyword_list]):
                append_title = True

            else:
                try:
                    if sum([author.casefold() in entry.authors for author in author_list]):
                        append_title = True
                except AttributeError:
                    pass

            if append_title:
                link = entry.link
                match = date_insert
                insert = f'<p style="font-size:x-large;">&bull;  <a href={link}>{title}</a></h3></p>\n'
                with open(file_output, 'r+t') as f:
                    insert_string(f, date_insert, insert)
                
                with open(file_log, 'a+t') as f:
                    f.write(title + '\n')

    i = i+1
    print(f'\tFinished scanning feed {i} of {len(feed_list)}.')
