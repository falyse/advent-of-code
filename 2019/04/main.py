range_min = 134792
range_max = 675810

def match(value):
    if len(str(value)) != 6:
        return False
    if not has_double(value):
        return False
    if not increasing(value):
        return False
    return True

def has_double(value):
    last = None
    for x in str(value):
        if last != None and x == last:
            if not (x + x + x) in str(value):
                return True
        last = x
    return False

def increasing(value):
    last = None
    for x in str(value):
        if last != None and int(x) < int(last):
            return False
        last = x
    return True

# print(match(111111))
# print(match(223450))
# print(match(123789))
print(match(112233))
print(match(123444))
print(match(111122))


cnt = 0
for i in range(range_min, range_max):
   if match(i):
       cnt += 1

print(cnt)