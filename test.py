"""
Tests for Game.play_land, Game.play_creature and Game.tap_land in src/game.py.

Run from the repo root with either:
    python -m unittest discover -s tests -v
    pytest tests/
"""
import sys
import unittest
from pathlib import Path

# game.py does `from cards import Card`, so src/ must be importable directly.
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

from src.cards import CreatureCard, LandCard  # noqa: E402
from src.game import Game  # noqa: E402

P1, P2 = "alice", "bob"


def make_land(name="Forest"):
    return LandCard(name=name, generic_mana=0, sp_mana="", description="", effect=None)


def make_creature(name="Slime", cost=1, colour="green"):
    return CreatureCard(
        name=name, generic_mana=cost, sp_mana=colour, description="", att=1, end=1, effect=""
    )


def new_game():
    return Game(P1, P2, [], [])


def put_in_hand(game, player, card_id, card):
    card.id = card_id
    game.hand[player][card_id] = card
    return card


class IsInHandTests(unittest.TestCase):
    """play_land and play_creature both rely on is_in_hand, so check it on its own."""

    def test_card_in_hand_with_enough_mana_is_playable(self):
        game = new_game()
        put_in_hand(game, P1, "1", make_creature(cost=1))
        game.mana_pools[P1]["green"] = 2

        self.assertTrue(game.is_in_hand(P1, "1"))

    def test_card_not_in_hand_returns_false_instead_of_raising(self):
        game = new_game()
        self.assertFalse(game.is_in_hand(P1, "99"))

    def test_card_in_deck_but_not_hand_is_not_playable(self):
        game = new_game()
        creature = make_creature()
        creature.id = "1"
        game.decks[P1]["1"] = creature
        game.mana_pools[P1]["green"] = 5

        self.assertFalse(game.is_in_hand(P1, "1"))

    def test_not_enough_mana_is_not_playable(self):
        game = new_game()
        put_in_hand(game, P1, "1", make_creature(cost=3))
        game.mana_pools[P1]["green"] = 1

        self.assertFalse(game.is_in_hand(P1, "1"))

    def test_mana_from_every_colour_counts_towards_the_cost(self):
        game = new_game()
        put_in_hand(game, P1, "1", make_creature(cost=2))
        game.mana_pools[P1].update(red=1, blue=1, green=1)

        self.assertTrue(game.is_in_hand(P1, "1"))


class PlayLandTests(unittest.TestCase):
    def test_land_moves_from_hand_to_lands(self):
        game = new_game()
        land = put_in_hand(game, P1, "1", make_land())

        self.assertTrue(game.play_land(P1, "1"))
        self.assertIs(game.lands[P1]["1"], land)
        self.assertNotIn("1", game.hand[P1])

    def test_first_land_can_be_played_with_empty_mana_pool(self):
        # Every mana pool starts at 0 and lands cost 0, so if this fails
        # nobody can ever play their first land.
        game = new_game()
        put_in_hand(game, P1, "1", make_land())

        self.assertTrue(game.play_land(P1, "1"))
        self.assertIn("1", game.lands[P1])

    def test_correct_land_played_when_hand_has_several_cards(self):
        game = new_game()
        put_in_hand(game, P1, "1", make_land("Forest"))
        mountain = put_in_hand(game, P1, "2", make_land("Mountain"))
        game.mana_pools[P1]["green"] = 5

        self.assertTrue(game.play_land(P1, "2"))
        self.assertIs(game.lands[P1]["2"], mountain)
        self.assertIn("1", game.hand[P1])
        self.assertNotIn("1", game.lands[P1])

    def test_card_not_in_hand_returns_false(self):
        game = new_game()
        game.mana_pools[P1]["green"] = 5

        self.assertFalse(game.play_land(P1, "99"))
        self.assertEqual(game.lands[P1], {})

    def test_cannot_play_card_from_opponents_hand(self):
        game = new_game()
        put_in_hand(game, P2, "1", make_land())
        game.mana_pools[P1]["green"] = 5

        self.assertFalse(game.play_land(P1, "1"))
        self.assertIn("1", game.hand[P2])
        self.assertEqual(game.lands[P1], {})


class PlayCreatureTests(unittest.TestCase):
    def test_creature_moves_from_hand_to_battlefield(self):
        game = new_game()
        slime = put_in_hand(game, P1, "1", make_creature(cost=1))
        game.mana_pools[P1]["green"] = 2

        self.assertTrue(game.play_creature(P1, "1"))
        self.assertIs(game.active_creatures[P1]["1"], slime)
        self.assertNotIn("1", game.hand[P1])

    def test_correct_creature_played_when_hand_has_several_cards(self):
        game = new_game()
        put_in_hand(game, P1, "1", make_creature("Slime"))
        bigger = put_in_hand(game, P1, "2", make_creature("Bigger Slime"))
        game.mana_pools[P1]["green"] = 5

        self.assertTrue(game.play_creature(P1, "2"))
        self.assertIs(game.active_creatures[P1]["2"], bigger)
        self.assertIn("1", game.hand[P1])

    def test_not_enough_mana_returns_false_and_card_stays_in_hand(self):
        game = new_game()
        put_in_hand(game, P1, "1", make_creature(cost=3))
        game.mana_pools[P1]["green"] = 1

        self.assertFalse(game.play_creature(P1, "1"))
        self.assertIn("1", game.hand[P1])
        self.assertEqual(game.active_creatures[P1], {})

    def test_card_not_in_hand_returns_false(self):
        game = new_game()
        game.mana_pools[P1]["green"] = 5

        self.assertFalse(game.play_creature(P1, "99"))
        self.assertEqual(game.active_creatures[P1], {})

    def test_cannot_play_creature_from_opponents_hand(self):
        game = new_game()
        put_in_hand(game, P2, "1", make_creature())
        game.mana_pools[P1]["green"] = 5

        self.assertFalse(game.play_creature(P1, "1"))
        self.assertIn("1", game.hand[P2])
        self.assertEqual(game.active_creatures[P1], {})


class TapLandTests(unittest.TestCase):
    def setUp(self):
        self.game = new_game()
        self.forest = make_land()
        self.forest.id = "1"
        self.game.lands[P1]["1"] = self.forest

    def test_tapping_own_land_marks_it_tapped(self):
        self.assertTrue(self.game.tap_land(P1, "1"))
        self.assertEqual(self.forest.tapped, 1)

    def test_tapping_correct_land_when_several_are_in_play(self):
        mountain = make_land("Mountain")
        mountain.id = "2"
        self.game.lands[P1]["2"] = mountain

        self.assertTrue(self.game.tap_land(P1, "2"))
        self.assertEqual(mountain.tapped, 1)
        self.assertEqual(self.forest.tapped, 0)

    def test_tapping_missing_land_returns_false(self):
        self.assertFalse(self.game.tap_land(P1, "99"))
        self.assertEqual(self.forest.tapped, 0)

    def test_cannot_tap_opponents_land(self):
        self.assertFalse(self.game.tap_land(P2, "1"))
        self.assertEqual(self.forest.tapped, 0)

    def test_tapping_an_already_tapped_land_returns_false(self):
        # Assumption: a land can only be tapped once until it untaps.
        self.forest.tapped = 1
        self.assertFalse(self.game.tap_land(P1, "1"))


if __name__ == "__main__":
    unittest.main()