from instagram.client import InstagramAPI
from credentials import ACCESS_TOKEN
import time
import sys


class Error(Exception):
    def __init__(self, error_message):
        self.error_message = error_message
    def __str__(self):
        return self.error_message

def get_max_id(next_url):
    if next_url == None:
        return None
    import re
    pattern = re.compile("max_id=([a-zA-Z_0-9]*)")
    return re.findall(pattern, next_url)[0]

if len(sys.argv) <= 1:
    raise Error("No user specified")
username = sys.argv[1]
api = InstagramAPI(access_token=ACCESS_TOKEN)
search_result = api.user_search(username)
if search_result <= 0:
    raise Error("User not found!")
user = search_result[0]

max_id = ""
while max_id != None:
    max_id = None
    media, next = api.user_recent_media(user_id=user.id, count=70, max_id=max_id)
    for m in media:
        api.like_media(m.id)
        print "You liked %s" % m.link
        time.sleep(60)
    max_id = get_max_id(next)

print "Done. Go check at http://instagram.com/%s" % (username)
