def abundant(h):
    for i in range(h, 11, -1):
        divisors = [j for j in range(1, i//2 + 1) if i % j == 0]
        sum_of_divisors = sum(divisors)
        if sum_of_divisors > i: return [[i], [sum_of_divisors - i]] 
