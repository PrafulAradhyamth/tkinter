from math import gcd

def lcm(a, b):
    return a * b // gcd(a, b)


def diffgen(a,b) :
    diffs = []
    current = 0
    ab = lcm(a,b)
    while current < ab:
        nextone = min((current // a + 1) * a,
                      (current // b + 1) * b)
        diffs.append(nextone - current)
        current = nextone
    return min(diffs)


tc = int(input())

for i in range(tc) :
    total_holiday, remove_holiday = map(int, input().split())
    holidays = list(map(int, input().split()))
    
    sorted = holidays.copy()
    sorted.sort()
    
    print("holiday = ", holidays)
    print("sorted = ", sorted)
    
    remove = []
    for count in range(remove_holiday) :

        

        min_val = 2147483647
        for i in range(len(sorted)-1) :
            # get minimum difference between two consecutive holidays
            #diff = sorted[i+1] - sorted[i]
            diff = diffgen(sorted[i+1], sorted[i])
            if (diff < min_val) :
                min_val = diff
                index = i + 1
        
        print("Min value = ", min_val, " element = ", sorted[index])
        remove.append(holidays.index(sorted[index])+1)
        sorted.remove(sorted[index])
        print("sorted = ", sorted)

    remove.sort()
    print(*remove)