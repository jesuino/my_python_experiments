import collections

Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = ['A'] + [str(n) for n in range(2,11)] + list('JQK')
    suits = 'spaces diamonds clubs hearts'.split()
    def __init__(self):
        self._cards = [Card(rank, suit) for rank in self.ranks
                                       for suit in self.suits]
    def __len__(self):
        return len(self._cards)
deck = FrenchDeck()
print(deck._cards)
