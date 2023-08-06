# # -*- coding: utf-8 -*-
# """
# Created on 2021/4/25 10:20 上午
# ---------
# @summary:
# ---------
# @author: Boris
# @email: boris_liu@foxmail.com
# """
#
from feapder.db.redisdb import RedisDB
import time

db = RedisDB.from_url("redis://localhost:6379")
# db = RedisDB()

db.clear("test")
a = db.strset("test", {"test":2})
print(a)





db.clear("test")

for i in range(20):
    # result = db.zadd("test", list(range(10)), list(range(10)))
    result = db.zadd("test", list(range(5)), list(range(5)))
    # result = db.zadd("test", 1)
    print(result)
    time.sleep(3)


#
# # db.zremrangebyscore("test", 1, 3)
#
# db.zrem("test", [4, 0])
#
# print(db.zget("test", 10))

