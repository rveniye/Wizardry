"""
Randomised game tests for Game.tap, Game.play_creature and Game.play_land.

Run from the repo root:
    python random_game_test.py            # random seed each run (printed on failure)
    SEED=1234 python random_game_test.py  # replay one exact game

(Named random_game_test.py rather than test_*.py because your .gitignore
ignores test_*.py.)
"""
import copy
import os
import random
import unittest
from collections import Counter

import src.card_index as card_index
from src.cards import CreatureCard, LandCard
from src.game import Game

P1, P2 = "alice", "bob"

ALL_CREATURES = [n for n, v in vars(card_index).items() if isinstance(v, CreatureCard)]
ALL_LANDS = [n for n, v in vars(card_index).items() if isinstance(v, LandCard)]

ZONES = ("decks", "hand", "lands", "active_creatures", "graveyard")


# ===========================================================================
# 1. Building a random game
# ===========================================================================

def real_card(name):
    """A fresh copy of a card_index card, so tests never share a card object."""
    return copy.deepcopy(getattr(card_index, name))


class MockGame:
    """Chainable builder around a real Game (see the earlier mock_game.py)."""

    def __init__(self, p1=P1, p2=P2):
        self.game = Game(p1, p2, [], [])
        self._next_id = 1

    def _place(self, zone, player, cards):
        for card in cards:
            card.id = str(self._next_id)
            zone[player][card.id] = card
            self._next_id += 1
        return self

    def hand(self, player, *cards):      return self._place(self.game.hand, player, cards)
    def deck(self, player, *cards):      return self._place(self.game.decks, player, cards)
    def lands(self, player, *cards):     return self._place(self.game.lands, player, cards)
    def creatures(self, player, *cards): return self._place(self.game.active_creatures, player, cards)
    def graveyard(self, player, *cards): return self._place(self.game.graveyard, player, cards)

    def mana(self, player, **colours):
        self.game.mana_pools[player].update(colours)
        return self

    def build(self):
        return self.game


def random_game(seed, creatures_each=12, lands_each=12):
    """
    Deals each player `creatures_each` random creatures and `lands_each` random
    lands (at least 10 of each), spread across every zone:

        hand: 3 creatures + 3 lands     lands in play: 4
        battlefield: 3 creatures        graveyard: 2 creatures
        deck: everything left over

    Same seed -> same game, so a failure can always be replayed.
    """
    assert creatures_each >= 10 and lands_each >= 10
    rng = random.Random(seed)
    mock = MockGame()

    for player in (P1, P2):
        creatures = [real_card(n) for n in rng.choices(ALL_CREATURES, k=creatures_each)]
        lands = [real_card(n) for n in rng.choices(ALL_LANDS, k=lands_each)]

        mock.hand(player, *creatures[:3], *lands[:3])
        mock.creatures(player, *creatures[3:6])
        mock.graveyard(player, *creatures[6:8])
        mock.lands(player, *lands[3:7])
        mock.deck(player, *creatures[8:], *lands[7:])
        mock.mana(player, red=rng.randint(0, 3), blue=rng.randint(0, 3), green=rng.randint(0, 3))

    return mock.build()


# ===========================================================================
# 3. Insight helpers: look inside a game
# ===========================================================================

def cards_in(game, zone, player):
    """{card_id: card} for one zone, e.g. cards_in(game, "hand", P1)."""
    return getattr(game, zone)[player]


def where_is(game, card_id):
    """Which (player, zone) a card id is in, or None if it's nowhere."""
    for zone in ZONES:
        for player in (game.p1_name, game.p2_name):
            if card_id in cards_in(game, zone, player):
                return player, zone
    return None


def total_mana(game, player):
    return sum(game.mana_pools[player].values())


def describe_card(card):
    """One line per card: id, name, cost, stats, tapped."""
    cost = f"{card.generic_mana}+{card.sp_mana}" if card.sp_mana else str(card.generic_mana)
    stats = f" {card.attack}/{card.defence}" if isinstance(card, CreatureCard) else ""
    tapped = " (tapped)" if card.tapped else ""
    return f"#{card.id:<3} {card.name:<20} cost {cost:<8}{stats}{tapped}"


def describe_zone(game, zone, player):
    cards = cards_in(game, zone, player)
    lines = [f"  {zone} ({len(cards)}):"]
    lines += [f"    {describe_card(c)}" for c in cards.values()] or ["    (empty)"]
    return "\n".join(lines)


def board(game, player=None, zones=ZONES):
    """
    A printable picture of the whole game (or one player). Pass it as the
    `msg` of an assertion and you'll see the board whenever a test fails.
    """
    out = []
    for p in ([player] if player else [game.p1_name, game.p2_name]):
        pool = game.mana_pools[p]
        out.append(f"== {p}  mana: {pool} (total {total_mana(game, p)})")
        out += [describe_zone(game, z, p) for z in zones]
    return "\n".join(out)


def snapshot(game):
    """
    A plain-data copy of where everything is right now: zones, tapped
    state and mana. Take one before an action and one after, then diff().
    """
    snap = {}
    for p in (game.p1_name, game.p2_name):
        snap[p] = {"mana": dict(game.mana_pools[p])}
        for zone in ZONES:
            snap[p][zone] = {cid: c.tapped for cid, c in cards_in(game, zone, p).items()}
    return snap


def diff(before, after):
    """
    Everything that changed between two snapshots, as readable lines:
      'alice: card #3 moved hand -> lands'
      'alice: card #7 tapped'
      'alice: mana green 2 -> 1'
    An empty list means nothing changed.
    """
    changes = []
    for p in before:
        for colour, amount in before[p]["mana"].items():
            if after[p]["mana"][colour] != amount:
                changes.append(f"{p}: mana {colour} {amount} -> {after[p]['mana'][colour]}")

        located_before = {cid: z for z in ZONES for cid in before[p][z]}
        located_after = {cid: z for z in ZONES for cid in after[p][z]}
        for cid in sorted(set(located_before) | set(located_after), key=int):
            z1, z2 = located_before.get(cid), located_after.get(cid)
            if z1 != z2:
                changes.append(f"{p}: card #{cid} moved {z1 or 'nowhere'} -> {z2 or 'nowhere'}")
            elif before[p][z1][cid] != after[p][z2][cid]:
                state = "tapped" if after[p][z2][cid] else "untapped"
                changes.append(f"{p}: card #{cid} {state}")
    return changes


def zone_counts(game, zone, player):
    """How many of each card by name, e.g. Counter({'Skeleton': 2})."""
    return Counter(c.name for c in cards_in(game, zone, player).values())


def pick(game, zone, player, card_type=None, rng=random):
    """A random card id from a zone, optionally only 'Land' or 'Creature'."""
    ids = [cid for cid, c in cards_in(game, zone, player).items()
           if card_type is None or c.type == card_type]
    return rng.choice(ids) if ids else None


def payment_for(card):
    """
    The cheapest payment under your current rule (generic_mana + 1, with one of
    the card's own colour), e.g. {'green': 3} for a 2+green creature.
    """
    return {card.sp_mana or "green": card.generic_mana + 1}


# ===========================================================================
# 2. The tests
# ===========================================================================

class RandomGameTest(unittest.TestCase):
    """Every test builds its own random game and shows the seed + board if it fails."""

    def setUp(self):
        self.seed = int(os.environ.get("SEED", random.randrange(10**6)))
        self.rng = random.Random(self.seed)
        self.game = random_game(self.seed)
        self.before = snapshot(self.game)

    def info(self):
        """Attach this to assertions: seed to replay, what changed, and the board."""
        changes = diff(self.before, snapshot(self.game)) or ["(nothing changed)"]
        return (f"\n\nReplay with: SEED={self.seed} python random_game_test.py"
                f"\n\nWhat changed:\n  " + "\n  ".join(changes) +
                f"\n\n{board(self.game)}")

    def assertOnlyChanges(self, expected):
        """Fails if the action changed anything other than `expected`."""
        self.assertEqual(diff(self.before, snapshot(self.game)), expected, self.info())


class SetupTests(RandomGameTest):
    def test_each_player_has_at_least_10_creatures_and_10_lands(self):
        for p in (P1, P2):
            everything = [c for z in ZONES for c in cards_in(self.game, z, p).values()]
            self.assertGreaterEqual(sum(c.type == "Creature" for c in everything), 10, self.info())
            self.assertGreaterEqual(sum(c.type == "Land" for c in everything), 10, self.info())

    def test_every_card_id_is_unique_across_the_whole_game(self):
        ids = [cid for z in ZONES for p in (P1, P2) for cid in cards_in(self.game, z, p)]
        self.assertEqual(len(ids), len(set(ids)), self.info())


class PlayLandTests(RandomGameTest):
    def test_land_moves_from_hand_to_lands_and_nothing_else_changes(self):
        land_id = pick(self.game, "hand", P1, "Land", self.rng)

        self.assertTrue(self.game.play_land(P1, land_id), self.info())
        self.assertOnlyChanges([f"{P1}: card #{land_id} moved hand -> lands"])

    def test_land_in_deck_cannot_be_played(self):
        land_id = pick(self.game, "decks", P1, "Land", self.rng)

        self.assertFalse(self.game.play_land(P1, land_id), self.info())
        self.assertOnlyChanges([])

    def test_cannot_play_opponents_land(self):
        land_id = pick(self.game, "hand", P2, "Land", self.rng)

        self.assertFalse(self.game.play_land(P1, land_id), self.info())
        self.assertOnlyChanges([])

    def test_all_three_lands_in_hand_can_be_played(self):
        # Assumption: no one-land-per-turn rule yet. Change this if you add one.
        for land_id in [cid for cid, c in cards_in(self.game, "hand", P1).items() if c.type == "Land"]:
            self.assertTrue(self.game.play_land(P1, land_id), self.info())
        self.assertEqual(zone_counts(self.game, "hand", P1).total(), 3, self.info())


class PlayCreatureTests(RandomGameTest):
    def setUp(self):
        super().setUp()
        self.game.mana_pools[P1].update(red=10, blue=10, green=10)  # enough for anything
        self.before = snapshot(self.game)

    def test_creature_moves_from_hand_to_battlefield(self):
        cid = pick(self.game, "hand", P1, "Creature", self.rng)
        card = cards_in(self.game, "hand", P1)[cid]

        self.assertTrue(self.game.play_creature(P1, cid, payment_for(card)), self.info())
        self.assertEqual(where_is(self.game, cid), (P1, "active_creatures"), self.info())

    def test_creature_on_battlefield_cannot_be_played_again(self):
        cid = pick(self.game, "active_creatures", P1, "Creature", self.rng)
        card = cards_in(self.game, "active_creatures", P1)[cid]

        self.assertFalse(self.game.play_creature(P1, cid, payment_for(card)), self.info())
        self.assertOnlyChanges([])

    def test_creature_in_graveyard_cannot_be_played(self):
        cid = pick(self.game, "graveyard", P1, "Creature", self.rng)
        card = cards_in(self.game, "graveyard", P1)[cid]

        self.assertFalse(self.game.play_creature(P1, cid, payment_for(card)), self.info())
        self.assertOnlyChanges([])

    def test_not_enough_mana_leaves_everything_alone(self):
        self.game.mana_pools[P1].update(red=0, blue=0, green=0)
        self.before = snapshot(self.game)
        cid = pick(self.game, "hand", P1, "Creature", self.rng)

        self.assertFalse(self.game.play_creature(P1, cid, {}), self.info())
        self.assertOnlyChanges([])


@unittest.skipUnless(hasattr(Game, "tap"), "Game.tap(player, creature_id) isn't written yet")
class TapCreatureTests(RandomGameTest):
    def test_tapping_own_creature_on_battlefield(self):
        cid = pick(self.game, "active_creatures", P1, "Creature", self.rng)

        self.assertTrue(self.game.tap(P1, cid), self.info())
        self.assertOnlyChanges([f"{P1}: card #{cid} tapped"])

    def test_cannot_tap_a_creature_twice(self):
        cid = pick(self.game, "active_creatures", P1, "Creature", self.rng)
        self.game.tap(P1, cid)

        self.assertFalse(self.game.tap(P1, cid), self.info())

    def test_cannot_tap_creature_in_hand(self):
        cid = pick(self.game, "hand", P1, "Creature", self.rng)

        self.assertFalse(self.game.tap(P1, cid), self.info())
        self.assertOnlyChanges([])

    def test_cannot_tap_opponents_creature(self):
        cid = pick(self.game, "active_creatures", P2, "Creature", self.rng)

        self.assertFalse(self.game.tap(P1, cid), self.info())
        self.assertOnlyChanges([])

    def test_tapping_one_creature_leaves_the_others_untapped(self):
        ids = list(cards_in(self.game, "active_creatures", P1))
        self.game.tap(P1, ids[0])

        for other in ids[1:]:
            self.assertEqual(cards_in(self.game, "active_creatures", P1)[other].tapped, 0, self.info())


if __name__ == "__main__":
    unittest.main(verbosity=2)
