
class Overflow(Exception):
    pass
# поправить чтобы при апдейте не уменьшался счетчик


class LRUCache:

    # ---------------------------------------------------------------------------------------------
    def __init__(self, capacity: int=10) -> None:
        assert type(capacity) == int, "capacity should be integer"
        self.capacity = capacity
        self.cache = dict()

    # ---------------------------------------------------------------------------------------------
    def get(self, key: str) -> str:
        return self.cache.get(key)

    # ---------------------------------------------------------------------------------------------
    def set(self, key: str, value: str) -> None:
        assert type(key) == str, "key should be a str type"
        assert type(value) == str, 'value should be a str type'
        if self.capacity <= 0:
            raise Overflow('LRUCache is full. Please, release element(s) or increase capacity')
        if key not in self.cache:
            self.capacity -= 1
        self.cache.update({key : value})

    # ---------------------------------------------------------------------------------------------
    def delete(self, key: str) -> None:
        try:
            self.cache[key]
        except KeyError:
            raise KeyError(f'Element {key} was never used before')
