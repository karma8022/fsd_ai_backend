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


# Function to extract video id from url
def extract_video_id(url):
    print("This is the url",url)
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
    answers = [doc.page_content for doc in ans]

    # Add CORS headers to the response
    response = JsonResponse({'answers': answers})
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response


# def llm_answering(request):
#     url = request.GET.get('url', '')
#     video_id = extract_video_id(url)
#     embedding2 = GooglePalmEmbeddings(google_api_key="AIzaSyBysL_SjXQkJ8lI1WPTz4VwyH6fxHijGUE")
#     print(f"index{video_id}")
#     db=FAISS.load_local(f"./query/vdb_chunks_HF/", embedding2,index_name=f"index{video_id}")
#     llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.1, "max_length":1024,"min_length": 512},huggingfacehub_api_token="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")
#     chain = load_qa_chain(llm, chain_type="stuff")
#     query = request.GET.get('query', '')
#     print(query)
#     docs = db.similarity_search(query)
#     response = chain.run(input_documents=docs, question=query)
#     return response

# def llm_answering(request):
#     # Assuming you're using Django for web development
#     url = request.GET.get('url', '')
#     print(url)
#     query = request.GET.get('query', '')
#     # Validate if both 'url' and 'query' parameters are present
#     if not url or not query:
#         return HttpResponse("Both 'url' and 'query' parameters are required.")
#     video_id = extract_video_id(url)
#     embedding2 = GooglePalmEmbeddings(google_api_key="AIzaSyBysL_SjXQkJ8lI1WPTz4VwyH6fxHijGUE")
#     # Adjust the path to your FAISS index directory
#     db = FAISS.load_local("./query/vdb_chunks_HF/", embedding2, index_name=f"index{video_id}")
#     llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.1, "max_length": 65536, "min_length": 32768}, huggingfacehub_api_token="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")
#     chain = load_qa_chain(llm, chain_type="stuff")
#     print(f"Query: {query}")
#     docs = db.similarity_search(query)
#     response = chain.run(input_documents=docs, question=query)
#     return JsonResponse({'response': response})

def llm_answering(request):
    # Assuming you're using Django for web development
    url = request.GET.get('url', '')
    query = request.GET.get('query', '')
    # Validate if both 'url' and 'query' parameters are present
    if not url or not query:
        return HttpResponse("Both 'url' and 'query' parameters are required.")
    video_id = extract_video_id(url)
    embedding2 = GooglePalmEmbeddings(google_api_key="AIzaSyBysL_SjXQkJ8lI1WPTz4VwyH6fxHijGUE")
    # Adjust the path to your FAISS index directory
    db = FAISS.load_local("./query/vdb_chunks_HF/", embedding2, index_name=f"index{video_id}")
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature": 0.1, "max_length": 65536, "min_length": 32768}, huggingfacehub_api_token="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")
    chain = load_qa_chain(llm, chain_type="stuff")
    docs = db.similarity_search(query)
    response = chain.run(input_documents=docs, question=query)

    # Add CORS headers to the response
    response = JsonResponse({'response': response})
    response['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    return response


def process_youtube_video(request):
    print(request)
    # Get YouTube URL from request parameters
    url = request.GET.get('query', '')
    print("This is the url",request.GET.get('query', ''))
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

# http://127.0.0.1:8000/query/yt/?query=omega&url=https://www.youtube.com/watch?v=7kcWV6zlcRU&list=PLUl4u3cNGP62esZEwffjMAsEMW_YArxYC&index=5&ab_channel=MITOpenCourseWare
# http://127.0.0.1:8000/query/ytvid/?url=https://www.youtube.com/watch?v=IcmzF1GT1Qw
# http://127.0.0.1:8000/query/llm/?query=what+is+omega&url=https://www.youtube.com/watch?v=7kcWV6zlcRU&list=PLUl4u3cNGP62esZEwffjMAsEMW_YArxYC&index=5&ab_channel=MITOpenCourseWare
# http://127.0.0.1:8000/query/llm/?query=what+does+he+say+about+beethoven+?&url=https://www.youtube.com/watch?v=IcmzF1GT1Qw&ab_channel=Vienna
# https://www.youtube.com/watch?v=Tuw8hxrFBH8

# https://www.youtube.com/watch?v=ep6k3Ofcf2s