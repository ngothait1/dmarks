import multiprocessing
import requests
import json

def parseDownload(json_object):
    if json_object:
        return len(json.dumps(json_object))
    return 0

def downloader(url, queue):
    downloaded_json = requests.get(url).json()
    url_char_num = parseDownload(downloaded_json)
    queue.put((url, url_char_num))

def main():
    queue = multiprocessing.Queue()
    total_chars = 0
    tracker_dict = {}
    urls = [
        'https://jsonplaceholder.typicode.com/posts',
        'https://jsonplaceholder.typicode.com/comments',
        'https://jsonplaceholder.typicode.com/albums',
        'https://jsonplaceholder.typicode.com/photos',
        'https://jsonplaceholder.typicode.com/todos',
        'https://jsonplaceholder.typicode.com/users'
    ]
    processes = [] 
    for url in urls:
        process = multiprocessing.Process(target = downloader, args = (url, queue))
        process.start()
        processes.append(process)
    for _ in processes:
        url, char_count = queue.get()
        tracker_dict[url] = char_count
        total_chars += char_count
    for process in processes:
        process.join()
    return tracker_dict, total_chars

if __name__ == "__main__":
    threads_dict, total_chars = main()
    for url, char_count in threads_dict.items():
        print(f"Downloaded {char_count} chars from: {url}")
    print(f"The total amount of characters downloaded is: {total_chars}")

