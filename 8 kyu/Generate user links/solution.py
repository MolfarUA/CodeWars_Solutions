57037ed25a7263ac35000c80


import urllib

def generate_link(user):
    return 'http://www.codewars.com/users/' + urllib.quote(user)
_______________________________________
from urllib.parse import quote


def generate_link(user: str) -> str:
    return f"http://www.codewars.com/users/{quote(user)}"
_______________________________________
import urllib.parse
def generate_link(user):
    return 'http://www.codewars.com/users/' + urllib.parse.quote(user)
_______________________________________
import urllib
def generate_link(user):
  return 'http://www.codewars.com/users/{}'.format(urllib.pathname2url(user))
_______________________________________
import urllib.parse

def generate_link(user):
    encoded_url = urllib.parse.quote(user)
    return f"http://www.codewars.com/users/{encoded_url}"
_______________________________________
generate_link = lambda _: 'http://www.codewars.com/users/'+__import__('urllib.parse').parse.quote(_)
