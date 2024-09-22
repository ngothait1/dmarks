import threading
import requests
import json

total_chars = 0
total_chars_lock = threading.Lock()

def parseDownload(json_object):
    if json_object:
        return len(json.dumps(json_object))
    return 0
                
def downloader(url, thread_id, tracker):
    global total_chars 
    downloaded_json = requests.get(url).json()
    url_char_num = parseDownload(downloaded_json)
    if thread_id not in tracker:
        tracker[thread_id] = {'url': url, 'chars_num': url_char_num}
    with total_chars_lock:
        total_chars += url_char_num
    
def main():
    tracker_dict = {}
    global total_chars 
    urls = [
        'https://jsonplaceholder.typicode.com/posts',  
        'https://jsonplaceholder.typicode.com/comments',    
        'https://jsonplaceholder.typicode.com/albums',     
        'https://jsonplaceholder.typicode.com/photos',      
        'https://jsonplaceholder.typicode.com/todos',     
        'https://jsonplaceholder.typicode.com/users'
        ]
    threads = [] 
    for thread_id, url in enumerate(urls):
        thread = threading.Thread(target = downloader, args = (url, thread_id, tracker_dict))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return tracker_dict

if __name__ == "__main__":
    threads_dict = main()  
    for thread_id, url_chars in threads_dict.items():
        print(f"Thread {thread_id} downloaded {url_chars.get("chars_num")} chars from: {url_chars.get("url")}")
    print(f"The total amount of characaters downloaded is: {total_chars }")

