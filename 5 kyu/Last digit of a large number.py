def last_digit(n1, n2):
    if n2 == 0: return 1
    return ((n1 % 10) ** 4) % 10 if (n2 % 4) == 0 else ((n1 % 10) ** (n2 % 4)) % 10
