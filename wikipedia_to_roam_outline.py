import io, sys, re

from lxml import html
import requests


html_ = requests.get(f'https://en.wikipedia.org/wiki/{sys.argv[-1]}').content.decode('utf8')

doc = html.parse(io.StringIO(html_))
root = doc.getroot()

def walk_tree(root):
  yield root
  for child in root:

    # ignore everything but the main part of the article
    if child.tag == 'table':
      continue
    if child.tag == 'h2':
      if child.text == 'Navigation menu':
        return
    if child.classes and 'hatnote' in child.get('class'):
      continue
    if child.classes and 'thumb' in child.get('class'):
      continue

    for grandchild in walk_tree(child):
      yield grandchild

headers = []
for child in walk_tree(root):

  # Stop when we hit the end of the main part of the article
  if child.tag == 'h2':
    headline = child.find('span[@class="mw-headline"]')
    if headline is not None and headline.text in (
      'External links',
      'Further reading',
      'References',
      'Notes',
      'See also',
    ):
      break

  if child.tag in ('h1', 'h2', 'h3', 'h4'):
    while headers and child.tag <= headers[-1].tag:
      headers.pop()
    headers.append(child)

  # headlines
  elif(
    child.tag == 'span' and child.classes and 'mw-headline' in child.get('class')
  ):
    print(f'{"  " * len(headers)}{child.text_content()}')

  # links
  elif(
    child.tag == 'a' and headers and child.text and len(child.text) > 3 and
    not re.match(r'\[[0-9]+\]', child.text)
  ):
    if child.text.startswith('Jump to ') or child.text == 'edit':
      continue
    if child.text.startswith('Wikipedia articles with'):
      break
    print(f'{"  " * (len(headers) + 1)}[[{child.text}]]') #, {child.attrib["href"]}')
