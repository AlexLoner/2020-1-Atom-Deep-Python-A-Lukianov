from cache import LRUCache

cache = LRUCache(100)
cache.set('Jesse', 'Pinkman')
cache.set('Walter', 'White')
print(f'Cache contains: {cache.cache}')

cache.set('Jesse', 'James')
print(f'Cache contains: {cache.cache}')

print(f'Get method: {cache.get("Jesse")}')

cache.delete('Walter')
print(f'Cache contains: {cache.cache}')

print(f'Get method: {cache.get("Walter")}')


cache = LRUCache(2)
cache.set('Jesse', 'Pinkman')
print(f'Cache contains: {cache.cache}')
cache.set('Jesse', 's;khgdf')
print(f'Cache contains: {cache.cache}')
cache.set('Walter', 'White')
print(f'Cache contains: {cache.cache}')
cache.set('23', 'unknown')
# print(f'Cache contains: {cache.cache}')
