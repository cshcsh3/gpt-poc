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

with open('top.csv', 'r') as videos:
  f = open('ratings.csv', 'w')
  headers = ['url','keyword','manual_rating','gpt_rating','partnership_id','total_referrals']
  writer = csv.writer(f)
  writer.writerow(headers)

  csv_reader = csv.reader(videos, delimiter=',')
  line_count = 0
  for video_row in csv_reader:
    if line_count > 0:
      url = video_row[0]
      keyword = video_row[1]
      manual_rating = video_row[2]
      partnership_id = video_row[3]
      total_referrals = video_row[4]

      yt_info.generate(url)
      response = query_gpt(keyword)
      writer.writerow([url, keyword, manual_rating, response, partnership_id, total_referrals])
      
    line_count += 1
    time.sleep(5)
  
  f.close()
