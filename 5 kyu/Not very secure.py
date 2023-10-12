def alphanumeric(password):
    if not password:
        return False

    alphanumeric_characters = "abcdefghijklmnopqrstuvwxyz0123456789"
    for character in password.lower():
        if character not in alphanumeric_characters:
            return False

    return True
