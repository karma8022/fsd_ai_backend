def extract_video_id(url):
    print("This is the url",url)
    # Parse URL
    url_data = urlparse.urlparse(url)
    # Extract video id
    video_id = urlparse.parse_qs(url_data.query)['v'][0]
    return video_id