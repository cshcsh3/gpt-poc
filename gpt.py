import csv
import yt_info
import time
import re
from dotenv import load_dotenv
from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader

load_dotenv()

def query_gpt(topic):
  documents = SimpleDirectoryReader(yt_info.DATA_FOLDER).load_data()
  index = GPTSimpleVectorIndex(documents)
  query = index.query("Given the following video information, on a scale of 1-10, how confident are you that the video talks about {}?".format(topic))
  return re.sub(r"\n", "", query.response)

with open('videos.csv', 'r') as videos:
  f = open('ratings.txt', 'w')
  csv_reader = csv.reader(videos, delimiter=',')
  line_count = 0
  for video_row in csv_reader:
    if line_count > 0:      
      url = video_row[0]
      topic = video_row[1]

      yt_info.generate(url)
      response = query_gpt(topic)
      f.write(f'{url} - Topic: {topic}, Manual rating: {video_row[4]}, GPT rating: {response}\n')

    line_count += 1
    time.sleep(5)
  
  f.close()
