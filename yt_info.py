import yt_dlp
import re
import os
from pathlib import Path

DATA_FOLDER = 'data'

# See help(yt_dlp.YoutubeDL) for a list of available options and public functions
# TODO Are automatic subs the same as normal subs or need to handle differently?
ydl_opts = {
  'writeautomaticsub': True,
  'writedescription': True,
  'subtitleslangs': ['en'],
  'skip_download': True
}

# Generates a file with the video title, description, transcript, and stores it in the data folder
def generate(url):
  try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      ydl.download(url)
      write_to_file = []

      # Get video title and description
      for description_file in Path('.').glob('*.description'):
        title = "Title: {}".format(description_file.name.split('[')[0])
        description = "Description: {}".format(re.sub(r"\n", " ", description_file.read_text()))
        write_to_file.append(title)
        write_to_file.append(description)
        os.remove(description_file.name)
        break

      # Get video transcript
      for vtt_file in Path('.').glob('*.en.vtt'):
        vtt_text = vtt_file.read_text()
        remove_first_3_lines = vtt_text.split('\n', 3)[3]
        remove_markups = re.sub(r"\n", " ", re.sub(r"(\d+:\d+:\d+.\d+).+%", "", re.sub(r"<[^>]*>", "", remove_first_3_lines))).strip()
        captions = "Transcript: {}".format(remove_markups)
        write_to_file.append(captions)
        os.remove(vtt_file.name)
        break

      with open(DATA_FOLDER + '/info.txt', 'w') as f:
        f.write("\n".join(write_to_file))
  except:
    print('Something went wrong')
