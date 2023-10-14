def solution(number):
    def sum_of_multiples(n):
        p = (number - 1) // n
        return n * p * (p + 1) // 2

    return sum_of_multiples(3) + sum_of_multiples(5) - sum_of_multiples(15)
