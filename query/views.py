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

# Function to extract video id from url
def extract_video_id(url):
    # Parse URL
    url_data = urlparse.urlparse(url)
    # Extract video id
    video_id = urlparse.parse_qs(url_data.query)['v'][0]
    return video_id

def say_hello(request):
    return HttpResponse("Hello")

def yt(request):
    # Get YouTube URL from request parameters
    url = request.GET.get('url', '')
    # Extract video id
    video_id = extract_video_id(url)

    embedding2 = GooglePalmEmbeddings(google_api_key="AIzaSyBysL_SjXQkJ8lI1WPTz4VwyH6fxHijGUE")
    vdb_chunks_HF = FAISS.load_local(f"./query/vdb_chunks_HF/", embedding2,index_name=f"index{video_id}")
    query = request.GET.get('query', '')
    ans = vdb_chunks_HF.as_retriever().get_relevant_documents(query)
    answers = [doc.page_content for doc in ans[:3]] if ans else []

    # Return answers and summary as a JSON response
    return JsonResponse({'answers': answers})

def process_youtube_video(request):
    print(request)
    # Get YouTube URL from request parameters
    url = request.GET.get('url', '')

    # Extract video id
    video_id = extract_video_id(url)

    # Fetch the captions
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_generated_transcript(['en'])
        captions = transcript.fetch()

        # Open a text file in write mode
        with open(f'./query/vdb_chunks_HF/{video_id}_captions.txt', 'w') as f:
            for caption in captions:
                # Write the caption to the text file
                f.write(caption['text'] + '\n')
    except:
        return JsonResponse({'error': "An error occurred while fetching the captions."})

    # Load text file
    with open(f'./query/vdb_chunks_HF/{video_id}_captions.txt', 'r') as file:
        text = file.read()

    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=0, length_function=len)
    chunks = text_splitter.split_text(text)

    # Create documents from chunks
    docs = text_splitter.create_documents(chunks)

    # Convert chunks to embeddings and save as FAISS file
    embedding = GooglePalmEmbeddings(google_api_key="AIzaSyBysL_SjXQkJ8lI1WPTz4VwyH6fxHijGUE")
    vdb_chunks_HF = FAISS.from_documents(docs, embedding=embedding)
    vdb_chunks_HF.save_local(f'./query/vdb_chunks_HF/', index_name=f"index{video_id}")

    return JsonResponse({'status': 'success'})
