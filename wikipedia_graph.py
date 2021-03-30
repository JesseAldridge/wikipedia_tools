import random, sys

import wikipedia
import networkx as nx
import matplotlib.pyplot as plt



def main(is_test):
  G = nx.Graph()

  print('loading first page...')
  root_name = 'Chemistry'
  page = wikipedia.page(root_name)
  G.add_node(root_name)

  steps = 2 if is_test else 6
  all_node_names = []
  for step in range(steps):
    print(f'step {step}')
    all_node_names.append(root_name)

    print('adding nodes...')
    links = page.links
    random.shuffle(links)
    links = links[:4]

    for i, _ in enumerate(links):
      truncated_link = links[i][:25] + ('...' if len(links[i]) > 25 else '')
      links[i] = word_wrap(truncated_link, n=5)

    for link in links:
      G.add_node(link)
      G.add_edge(root_name, link)
      all_node_names.append(link)

    print('loading next page...')
    for _ in range(10):
      root_name = random.choice(all_node_names)
      try:
        page = wikipedia.page(root_name)
      except:
        continue
      else:
        break

  print('drawing graph...')

  ax1 = plt.subplot(111)
  ax1.margins(0.3)

  pos = nx.spring_layout(
    G,
    k=0.1,
  )


  nx.draw(
    G,
    ax=ax1,
    with_labels=True,
    font_size=6,
    node_color='#eee',
    # node_color='white',
    node_size=700,
    node_shape='s', # square
    pos=pos,
  )

  plt.show()

def word_wrap(s, n=80):
  lines = []
  line = ''
  for ch in s:
    line += ch
    if len(line) > n and ch == ' ':
      lines.append(line)
      line = ''
  lines.append(line)
  return '\n'.join(lines)

if __name__ == '__main__':
  main(is_test='test' in sys.argv)
