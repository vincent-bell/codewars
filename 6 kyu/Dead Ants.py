def dead_ant_count(ants):
    ants = ants.replace('ant', '')
    parts = {}
    for char in ants:
        if char in ['a', 'n', 't']:
            parts[char] = 1 if not char in parts else parts[char] + 1
    return max(parts.values())
