from abc import ABC, abstractmethod


# --------------------------------------
# 🍕 Abstract Pizza Interface
# --------------------------------------
class Pizza(ABC):
    @abstractmethod
    def prepare(self):
        pass


# 🍕 Concrete Pizza Classes
class Margherita(Pizza):
    def prepare(self):
        print("Margherita: Cheese only!")


class Paneer(Pizza):
    def prepare(self):
        print("Paneer Pizza: Spicy paneer chunks!")


class Chicken(Pizza):
    def prepare(self):
        print("Chicken Pizza: Grilled chicken!")


class Farmhouse(Pizza):
    def prepare(self):
        print("Farmhouse Pizza: Loaded with veggies!")


# --------------------------------------
# 🏭 PizzaFactory with Category Registry
# --------------------------------------
class PizzaFactory:
    registry = {}
    categories = {}

    @classmethod
    def register(cls, name: str, constructor, category: str):
        cls.registry[name] = constructor
        cls.categories.setdefault(category, set()).add(name)

    @classmethod
    def get_pizza(cls, name: str) -> Pizza:
        if name in cls.registry:
            return cls.registry[name]()
        raise ValueError(f"Unknown pizza type: {name}")

    @classmethod
    def get_category(cls, category: str):
        return cls.categories.get(category, set())


# Register Pizzas
PizzaFactory.register("margherita", Margherita, "veg")
PizzaFactory.register("paneer", Paneer, "veg")
PizzaFactory.register("farmhouse", Farmhouse, "veg")
PizzaFactory.register("chicken", Chicken, "nonveg")


# --------------------------------------
# 👨‍🍳 Chef Abstract Class
# --------------------------------------
class Chef(ABC):
    @abstractmethod
    def prepare_pizza(self, pizza_type: str) -> Pizza:
        pass


# 🥗 VegChef Implementation
class VegChef(Chef):
    def prepare_pizza(self, pizza_type):
        if pizza_type in PizzaFactory.get_category("veg"):
            return PizzaFactory.get_pizza(pizza_type)
        raise ValueError(f"VegChef can't prepare {pizza_type}")


# 🍖 NonVegChef Implementation
class NonVegChef(Chef):
    def prepare_pizza(self, pizza_type):
        if pizza_type in PizzaFactory.get_category("nonveg"):
            return PizzaFactory.get_pizza(pizza_type)
        raise ValueError(f"NonVegChef can't prepare {pizza_type}")


# --------------------------------------
# 👨‍🍳 HeadChef as Kitchen Interface (DIP)
# --------------------------------------
class Kitchen(ABC):
    @abstractmethod
    def place_order(self, pizza_type: str) -> Pizza:
        pass


class HeadChef(Kitchen):
    def __init__(self, chef_registry: dict):
        self.chef_registry = chef_registry

    def place_order(self, pizza_type: str) -> Pizza:
        for chef in self.chef_registry.values():
            try:
                return chef.prepare_pizza(pizza_type)
            except ValueError:
                continue
        raise ValueError(f"No chef available to prepare '{pizza_type}'")


# --------------------------------------
# 🧾 Order Object — Tracks Order ID
# --------------------------------------
class Order:
    def __init__(self, order_id: int, pizza: Pizza):
        self.order_id = order_id
        self.pizza = pizza

    def prepare(self):
        print(f"👨‍🍳 Chef: Preparing Order #{self.order_id}")
        self.pizza.prepare()

    def deliver(self):
        print(f"🧑‍🍽️ Waiter: Delivering Order #{self.order_id}")
        self.pizza.prepare()


# --------------------------------------
# 🧑‍💼 Receptionist — Manages Order Intake
# --------------------------------------
class Receptionist:
    def __init__(self, kitchen: Kitchen):
        self.kitchen = kitchen

    def take_order(self, pizza_type: str, order_id: int) -> Order:
        print(
            f"\n🧾 Receptionist: Received Order #{order_id} for '{pizza_type}' pizza."
        )
        pizza = self.kitchen.place_order(pizza_type)
        return Order(order_id, pizza)


# --------------------------------------
# 🧑‍🍽️ Waiter — Handles Delivery
# --------------------------------------
class Waiter:
    def deliver(self, order: Order):
        order.deliver()


"""
# --------------------------------------
# 🚀 Dynamic Simulation
# --------------------------------------
if __name__ == "__main__":
    chef_registry = {"veg": VegChef(), "nonveg": NonVegChef()}

    kitchen = HeadChef(chef_registry)
    receptionist = Receptionist(kitchen)
    waiter = Waiter()

    print("🍕 Welcome to the Python Pizza Shop!")
    print("Available pizzas:", ", ".join(PizzaFactory.registry.keys()))

    order_counter = 1

    while True:
        print("Available pizzas:", ", ".join(PizzaFactory.registry.keys()))
        choice = (
            input(f"\nOrder #{order_counter} - Enter pizza type (or 'exit' to quit): ")
            .lower()
            .strip()
        )
        if choice == "exit":
            print("\n👋 All orders complete. Thank you!")
            break
        try:
            order = receptionist.take_order(choice, order_counter)
            order.prepare()
            waiter.deliver(order)
        except ValueError as e:
            print(f"❌ Error with Order #{order_counter}: {e}")
        finally:
            order_counter += 1
"""

# --------------------------------------
# 🚀 Dynamic Simulation
# --------------------------------------
if __name__ == "__main__":
    chef_registry = {"veg": VegChef(), "nonveg": NonVegChef()}

    kitchen = HeadChef(chef_registry)
    receptionist = Receptionist(kitchen)
    waiter = Waiter()

    print("🍕 Welcome to the Python Pizza Shop!")
    print("Available pizzas:", ", ".join(PizzaFactory.registry.keys()))

    order_counter = 1

    while True:
        print("Available pizzas:", ", ".join(PizzaFactory.registry.keys()))
        choice = (
            input(f"\nOrder #{order_counter} - Enter pizza type (or 'exit' to quit): ")
            .lower()
            .strip()
        )
        if choice == "exit":
            print("\n👋 All orders complete. Thank you!")
            break
        try:
            order = receptionist.take_order(choice, order_counter)
            order.prepare()
            waiter.deliver(order)
        except ValueError as e:
            print(f"❌ Error with Order #{order_counter}: {e}")
        finally:
            order_counter += 1
