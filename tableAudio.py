from html.parser import HTMLParser, HTMLParseError
import urllib.request
import subprocess
import re
import concurrent.futures


# URL we fetch.
urlTA = 'http://tabletopaudio.com/'
localFile = '/databank/Audio/Music/Ambience/'

# We need dis.
endList = []

# The 'ls' of the directory containing the files
listResult = subprocess.check_output("ls {}".format(localFile),
                                     universal_newlines = True,
                                     stderr = subprocess.STDOUT,
                                     shell = True)

# Our custom parser to build the list we will need.
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                # Find the MP3s
                if '.mp3' in attr[1]:
                    # Clean the string here, won't have to do it every time.
                    cleanAttr = attr[1].replace("\\", "")

                    # Rip out the names without download shit.
                    match = re.search("(\d+.+mp3)", cleanAttr)

                    # Do we already have them? No? Do shit.
                    if match.group(0) not in listResult:
                        cleanURL = urlTA + cleanAttr

                        # Build list containing important information.
                        endList.append({"url": cleanURL, "file": localFile + match.group(0)})

# Function for our concurrent processes.
def downloadURL(url, local):
    print("GET: ", url)
    urllib.request.urlretrieve(url, local)

# Do the parsing work.
parser = MyHTMLParser()
tableAudio = urllib.request.urlopen(urlTA)
try:
    parser.feed(str(tableAudio.read()))
except (TypeError, HTMLParseError):
    # We pass because it just happens when we run out of shit.
    # Also, the site uses malformed html. So we have to just...accept that.
    pass

# Ripped from concurrent manpage.
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(downloadURL, x["url"], x["file"]): x for x in endList}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
