from dataclasses import dataclass, field


@dataclass
class Item:
    name: str
    item_type: str


@dataclass
class Player:
    max_health: int = 100
    health: int = 100
    inventory_capacity: int = 5
    inventory: list[Item] = field(default_factory=list)

    def __post_init__(self):
        if self.max_health <= 0:
            raise ValueError("Maximum health must be greater than zero.")
        if not 0 <= self.health <= self.max_health:
            raise ValueError("Health must be between zero and maximum health.")
        if self.inventory_capacity < 0:
            raise ValueError("Inventory capacity cannot be negative.")
        if len(self.inventory) > self.inventory_capacity:
            raise ValueError("Initial inventory exceeds capacity.")

    def collect_item(self, item: Item) -> bool:
        """Add an item if there is room. Return whether it was collected."""
        if len(self.inventory) >= self.inventory_capacity:
            return False
        self.inventory.append(item)
        return True

    def use_health_potion(self) -> bool:
        """Use one health potion. Return False if none are available."""
        potion_index = next(
            (i for i, item in enumerate(self.inventory)
             if item.item_type == "potion" and item.name == "Health Potion"),
            None,
        )
        if potion_index is None:
            return False

        #A potion is consumed even if the player's health is already full.
        self.inventory.pop(potion_index)
        self.health = min(self.max_health, self.health + 25)
        return True

    def take_damage(self, amount: int) -> None:
        """Reduce health without allowing negative damage or negative health."""
        if amount < 0:
            raise ValueError("Damage cannot be negative.")
        self.health = max(0, self.health - amount)

    def count_item(self, name: str) -> int:
        return sum(1 for item in self.inventory if item.name == name)


def run_demo() -> None:
    player = Player(health=100)
    potion = Item(name="Health Potion", item_type="potion")

    print("-=+ RPG Inventory Demo +=-")
    print(f"Starting health: {player.health}/{player.max_health}")
    print(f"Collect potion: {player.collect_item(potion), player.collect_item(potion)}")
    print(f"Inventory potions: {player.count_item('Health Potion')}")
    print(f"Use potion: {player.use_health_potion()}")
    print(f"Final health: {player.health}/{player.max_health}")
    print(f"Inventory potions remaining: {player.count_item('Health Potion')}")


if __name__ == "__main__":
    run_demo()
