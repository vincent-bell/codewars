def validate(digits: int):
    # Get digit count
    digit_count = len(str(digits))

    # Store digits in array
    digit_array = [int(digit) for digit in str(digits)]

    # Luhn algorithm
    for i in range(digit_count-2, -1, -2):
        digit_array[i] *= 2
        if digit_array[i] > 9:
            digit_array[i] -= 9

    if sum(digit_array) % 10 == 0:
        return True
    return False
