import random

import wikipedia
import networkx as nx
import matplotlib.pyplot as plt



def main():
  G = nx.Graph()

  print('loading first page...')
  root_name = 'New York City'
  page = wikipedia.page(root_name)
  G.add_node(root_name)

  for step in range(4):
    print(f'step {step}')

    print('adding nodes...')
    links = page.links
    random.shuffle(links)
    links = links[:4]
    for link in links:
      G.add_node(link)
      G.add_edge(root_name, link)

    print('loading next page...')
    for _ in range(10):
      root_name = random.choice(links)
      try:
        page = wikipedia.page(root_name)
      except wikipedia.exceptions.PageError:
        continue
      else:
        break


  # plt.subplot(121)
  print('drawing graph...')
  nx.draw(G, with_labels=True, font_weight='bold')
  plt.show()

if __name__ == '__main__':
  main()
