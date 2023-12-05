# Convert chunks to embeddings and save as FAISS file
# embedding = GooglePalmEmbeddings(google_api_key="AIzaSyBysL_SjXQkJ8lI1WPTz4VwyH6fxHijGUE")
# vdb_chunks_HF = FAISS.from_documents(docs, embedding=embedding)
# vdb_chunks_HF.save_local(f'./query/vdb_chunks_HF/', index_name=f"index{video_id}")
# print("done")