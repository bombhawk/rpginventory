"""Automated tests for the RPG inventory system.

The tests are grouped by purpose:
- Unit tests: individual methods and rules
- Integration tests: inventory and health behavior working together
- System tests: a complete player workflow
"""

import pytest

from main import Item, Player


#Unit tests
def test_collect_item_adds_item_to_inventory():
    player = Player()
    potion = Item("Health Potion", "potion")

    assert player.collect_item(potion) is True
    assert player.inventory == [potion]


def test_inventory_rejects_item_when_full():
    player = Player(inventory_capacity=1)
    assert player.collect_item(Item("Health Potion", "potion")) is True

    assert player.collect_item(Item("Iron Sword", "weapon")) is False
    assert len(player.inventory) == 1


def test_potion_restores_25_health():
    player = Player(health=50)
    player.collect_item(Item("Health Potion", "potion"))

    assert player.use_health_potion() is True
    assert player.health == 75


def test_potion_does_not_exceed_maximum_health():
    player = Player(health=90)
    player.collect_item(Item("Health Potion", "potion"))

    player.use_health_potion()

    assert player.health == 100


def test_using_potion_consumes_exactly_one_potion():
    player = Player(health=50)
    player.collect_item(Item("Health Potion", "potion"))
    player.collect_item(Item("Health Potion", "potion"))

    player.use_health_potion()

    assert player.count_item("Health Potion") == 1


def test_cannot_use_potion_when_none_are_available():
    player = Player(health=50)

    assert player.use_health_potion() is False
    assert player.health == 50


def test_damage_cannot_reduce_health_below_zero():
    player = Player(health=20)

    player.take_damage(50)

    assert player.health == 0


def test_negative_damage_is_rejected():
    player = Player(health=50)

    with pytest.raises(ValueError):
        player.take_damage(-5)


def test_invalid_initial_health_is_rejected():
    with pytest.raises(ValueError):
        Player(health=101)


#Integration tests
def test_collect_and_use_potion_updates_health_and_inventory():
    player = Player(health=50)
    potion = Item("Health Potion", "potion")

    collected = player.collect_item(potion)
    used = player.use_health_potion()

    assert collected is True
    assert used is True
    assert player.health == 75
    assert player.count_item("Health Potion") == 0


def test_full_inventory_does_not_allow_potion_use_without_potion():
    player = Player(inventory_capacity=1)
    player.collect_item(Item("Iron Sword", "weapon"))

    assert player.use_health_potion() is False
    assert player.count_item("Iron Sword") == 1


#System tests
def test_complete_workflow_collect_use_and_check_final_state():
    """A full workflow: start injured, collect potion, use it, verify state."""
    player = Player(health=60, inventory_capacity=2)

    assert player.health == 60
    assert player.collect_item(Item("Health Potion", "potion")) is True
    assert player.count_item("Health Potion") == 1

    assert player.use_health_potion() is True
    assert player.health == 85
    assert player.count_item("Health Potion") == 0


def test_complete_workflow_with_near_maximum_health():
    """The complete workflow should cap health at max and consume the potion."""
    player = Player(health=90)
    player.collect_item(Item("Health Potion", "potion"))

    assert player.use_health_potion() is True
    assert player.health == player.max_health
    assert player.count_item("Health Potion") == 0
