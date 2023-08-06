import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import time

import sys

def download_file(local_filename,fileUrl,s):
    r = s.get(fileUrl, stream=True)
    try:
        if int(r.headers.get('content-length'))==os.path.getsize(local_filename):
            return 0
        print(int(r.headers.get('content-length')))
        print(local_filename)
        print(os.path.getsize(local_filename))
    except FileNotFoundError:
        pass
        #print("dowload")
    start_time = time.time()
    with open(local_filename, 'wb') as f:
        count = 1
        block_size = 512
        try:
            total_size = int(r.headers.get('content-length'))
            print('file total size :',total_size)
        except TypeError:
            print('using dummy length !!!')
            total_size = 10000000
        for chunk in r.iter_content(chunk_size=block_size):
            if chunk: # filter out keep-alive new chunks
                duration = time.time() - start_time
                progress_size = int(count * block_size)
            if duration == 0:
                duration = 0.1
            speed = int(progress_size / (1024 * duration))
            percent = int(count * block_size * 100 / total_size)
            sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" % (percent, progress_size / (1024 * 1024), speed, duration))
            f.write(chunk)
            f.flush()
            count += 1
    f.close()
