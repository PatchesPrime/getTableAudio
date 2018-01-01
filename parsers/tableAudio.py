from html.parser import HTMLParser
import re
import os


# Our custom parser to build the list we will need.
class MyHTMLParser(HTMLParser):
    # URL we fetch.
    url = 'http://tabletopaudio.com/'

    # Where we put it
    localFile = '/home/patches/projects/getTableAudio/'

    # The 'ls' of the directory containing the files
    listResult = os.listdir(localFile)

    # The list we use to store our missing links.
    sasquatch = list()

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
                    if match.group(0) not in self.listResult:
                        cleanURL = self.url + cleanAttr

                        # Build list containing important information.
                        self.sasquatch.append(
                            {
                                "url": cleanURL,
                                "file": self.localFile + match.group(0)
                            }
                        )
