def adder(n):
    def adder_generator(old_f):
        def adder(*args, **kwds):
            return n + old_f(*args, **kwds)
        return adder;
    return adder_generator
    

@adder(2)
def double(x):
    return x * 2

a = double(5)
print(a)

