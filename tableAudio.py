from html.parser import HTMLParser, HTMLParseError
import urllib.request
import subprocess
import re

# URL we fetch.
urlTA = 'http://tabletopaudio.com/'
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
                    # Clean the string here, won't have to do it every time.
                    cleanAttr = attr[1].replace("\\", "")

                    # Rip out the names without download shit.
                    match = re.search("(\d+.+mp3)", cleanAttr)

                    # Do we already have them? No? Do shit.
                    if match.group(0) not in listResult:
                        cleanURL = urlTA + cleanAttr

                        # Fetch'em.
                        urllib.request.urlretrieve(cleanURL, localFile + match.group(0))


parser = MyHTMLParser()
tableAudio = urllib.request.urlopen(urlTA)
try:
    parser.feed(str(tableAudio.read()))
except (TypeError, HTMLParseError):
    # We pass because it just happens when we run out of shit.
    # Also, the site uses malformed html. So we have to just...accept that.
    pass
