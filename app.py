from dotenv import load_dotenv
from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader

load_dotenv()

topic = "hair"
documents = SimpleDirectoryReader('data').load_data()
index = GPTSimpleVectorIndex(documents)

response = index.query("Given this video transcript, on a scale of 1-10, how confident are you that the video talks about {}?".format(topic))
print(response)