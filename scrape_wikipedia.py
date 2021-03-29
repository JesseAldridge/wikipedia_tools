import io

from lxml import html
import requests


html_ = requests.get('https://en.wikipedia.org/wiki/Chemistry').content.decode('utf8')

doc = html.parse(io.StringIO(html_))
root = doc.getroot()

def walk_tree(root):
  yield root
  for child in root:
    for grandchild in walk_tree(child):
      yield grandchild

headers = []
for child in walk_tree(root):
  if child.tag in ('h2', 'h3', 'h4'):
    while headers and child.tag <= headers[-1].tag:
      headers.pop()
    headers.append(child)
  elif child.tag == 'span' and child.classes and child.classes.pop() == 'mw-headline':
    print(f'{"  " * len(headers)}{child.text}')
  elif child.tag == 'a' and headers and child.text and len(child.text) > 5:
    print(f'{"  " * (len(headers) + 1)}{child.text}') #, {child.attrib["href"]}')
