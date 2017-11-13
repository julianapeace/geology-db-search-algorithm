import scholarly

def hello():
    search_query = scholarly.search_author('Steven A Cholewiak')
    author = next(search_query).fill()
    print(author)

    # Print the titles of the author's publications
    print([pub.bib['title'] for pub in author.publications])

    # Take a closer look at the first publication
    pub = author.publications[0].fill()
    print(pub)

    # Which papers cited that publication?
    print([citation.bib['title'] for citation in pub.get_citedby()])

search_query = scholarly.search_keyword('geology')
print(next(search_query))
