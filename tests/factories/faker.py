import random
import string


class Faker:
    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)

    def random_int(self, min_value: int = 0, max_value: int = 100) -> int:
        return self.random.randint(min_value, max_value)

    def random_string(self, string_length: int = 10) -> str:
        return "".join(self.random.choices(string.ascii_letters, k=string_length))


faker = Faker(42)
