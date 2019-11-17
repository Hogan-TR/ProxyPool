from ProxyPool.db import myredis

g = myredis.add("test", "192.173.3.11:902", 6)
# g2 = myredis.increase("test", "192.173.3.11:902")
g3 = myredis.decrease("test", "192.173.3.11:902")
print(g, type(g))
# print(g2, type(g2))
print(g3, type(g3))
