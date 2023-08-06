from timedfunc import timedfunc

@timedfunc
def my_function(x):
	print("doing stuff that takes some time...")
	import time
	time.sleep((x + 1) * 0.100) # simulate a computation

for i in range(3):
	my_function(i)

