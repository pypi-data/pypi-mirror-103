from whist.card import Suit, Rank, Card


def test_suit_order():
    assert Suit.CLUBS < Suit.DIAMONDS < Suit.HEARTS < Suit.SPADES


def test_rank_order():
    assert Rank.NUM_2 < Rank.NUM_3 < Rank.NUM_4 < Rank.NUM_5 < Rank.NUM_6 < Rank.NUM_7 \
           < Rank.NUM_8 < Rank.NUM_9 < Rank.NUM_10 < Rank.J < Rank.Q < Rank.K < Rank.A


def test_card_equality():
    c1 = Card(Suit.CLUBS, Rank.NUM_2)
    c2 = Card(Suit.CLUBS, Rank.NUM_2)
    assert c1 == c2
