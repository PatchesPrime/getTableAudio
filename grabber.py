import requests
import shutil
import concurrent.futures
import sys
import importlib.util


# Function for our concurrent processes.
def downloadURL(url, local):
    req = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
    if req.status_code == 200:
        print("GET: ", url)
        with open(local, 'wb') as f:
            req.raw.decode_content = True
            shutil.copyfileobj(req.raw, f)


if len(sys.argv) != 2:
    raise IndexError('usage: python grabber.py parsers/tableAudio.py')

# Try to import the first argument passed.
# I like to live dangerously! (not really)
spec = importlib.util.spec_from_file_location(
    'blackMagic', sys.argv[1]
)

# This is where the module lives.
lib = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lib)

# Do the parsing work.
parser = lib.MyHTMLParser()
req = requests.get(parser.url, headers={'User-Agent': 'Mozilla/5.0'})

try:
    parser.feed(req.text)
except Exception as e:
    # We pass because it just happens when we run out of shit.
    # Also, the site uses malformed html. So we have to just...accept that.
    pass

# Ripped from concurrent manpage.
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {
        executor.submit(downloadURL, x["url"], x["file"]): x for x in parser.sasquatch
    }
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
