def func(i):
    print(i)
    if i > 50:
        return i
    i = i+10
    func(i+10)
    
a = 10
print(func(a))
print(a)