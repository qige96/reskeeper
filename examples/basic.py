from reskeeper import ResourceKeeper
import sys


resources = [
    "127.0.0.1",
    "127.0.0.2",
]

# New resource keeper and load 2 resources
rk = ResourceKeeper()
rk.load(resources)


# Get resources and print them
res1 = rk.get()
res2 = rk.get()
res3 = rk.get()

print(res1.to_dict())
print([res2.res_id, res2.data])
try:
    print(res3.to_dict())
except AttributeError:
    print("res3 is None")
    print(res3)


# Release a resource and get it again
rk.release(res2)
print(res2)
res3 = rk.get()
print(res3.to_dict())


print("Add a resource")
rk.add("127.0.0.3")
res4 = rk.get()
print({"res_id":res4.res_id, "data": res4.data})




