from youtube_transcript_api import YouTubeTranscriptApi
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain.vectorstores import FAISS
from django.http import JsonResponse
import urllib.parse as urlparse
from django.shortcuts import render
from django.http import HttpResponse
from langchain.embeddings import HuggingFaceEmbeddings
import requests
from django.http import JsonResponse
from langchain.embeddings import GooglePalmEmbeddings
from transformers import pipeline
from django.http import JsonResponse
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import GooglePalmEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFacePipeline
from langchain.chains.question_answering import load_qa_chain
import json
from langchain.llms.huggingface_hub import HuggingFaceHub
from django.views.decorators.csrf import csrf_exempt
url="https://www.youtube.com/watch?v=7vE95eBX6M0"
def extract_video_id(url):
    print("This is the url",url)
    # Parse URL
    url_data = urlparse.urlparse(url)
    # Extract video id
    video_id = urlparse.parse_qs(url_data.query)['v'][0]
    return video_id
video_id=extract_video_id(url)
# transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
# transcript = transcript_list.find_generated_transcript(['en'])
# captions = transcript.fetch()

# # Open a text file in write mode
# with open(f'./query/vdb_chunks_HF/{video_id}_captions.txt', 'w') as f:
#     for caption in captions:
#         # Write the caption to the text file
#         f.write(caption['text'] + '\n')

# print(captions)
# with open(f'./query/vdb_chunks_HF/{video_id}_captions.txt', 'r') as file:
#         text = file.read()

# text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=0, length_function=len)
# chunks = text_splitter.split_text(text)

#     # Create documents from chunks
# docs = text_splitter.create_documents(chunks)

# # Convert chunks to embeddings and save as FAISS file
embedding = GooglePalmEmbeddings(google_api_key="AIzaSyBysL_SjXQkJ8lI1WPTz4VwyH6fxHijGUE")
# vdb_chunks_HF = FAISS.from_documents(docs, embedding=embedding)
# vdb_chunks_HF.save_local(f'./query/vdb_chunks_HF/', index_name=f"index{video_id}")

query = input("Enter your query: ")

db = FAISS.load_local("./query/vdb_chunks_HF/", embedding, index_name=f"index{video_id}")
llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.1, "max_length": 65536, "min_length": 32768}, huggingfacehub_api_token="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")
chain = load_qa_chain(llm, chain_type="stuff")
docs = db.similarity_search(query)
response = chain.run(input_documents=docs, question=query)

print(response)
