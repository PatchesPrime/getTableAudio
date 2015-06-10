from html.parser import HTMLParser, HTMLParseError
import urllib.request
import subprocess
import re

# URL we fetch.
urlTA = 'http://tabletopaudio.com'
localFile = '/databank/Audio/Music/Ambience/'

# The 'ls' of the directory containing the files
listResult = subprocess.check_output("ls {}".format(localFile),
                                     universal_newlines = True,
                                     stderr = subprocess.STDOUT,
                                     shell = True)


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr in attrs:
                # Find the MP3s
                if '.mp3' in attr[1]:
                    # Rip out the names without download shit.
                    match = re.search("(\d+.+mp3)", attr[1])
                    # Do we already have them? No? Do shit.
                    if match.group(0).replace("\\", "") not in listResult:
                        # Trust me.
                        cleanURL = urlTA + "/" + attr[1].replace("\\", "")
                        # Fetch'em.
                        print("WGET ", cleanURL)
                        urllib.request.urlretrieve(cleanURL, localFile + match.group(0).replace("\\", ""))


parser = MyHTMLParser()
tableAudio = urllib.request.urlopen(urlTA)
try:
    parser.feed(str(tableAudio.read()))
except (TypeError, HTMLParseError):
    # We pass because it just happens when we run out of shit.
    # Also, the site uses malformed html. So we have to just...accept that.
    pass

