import rolldice

def roll_attack(num_attackers: int, bonus: int, target: int):
    rolls = [rolldice.roll_dice("d20")[0] for _ in range(num_attackers)]
    crits = rolls.count(20)
    hits = len([roll for roll in rolls if roll + bonus >= target]) - crits
    misses = num_attackers - crits - hits
    return (crits, hits, misses)


def roll_damage(hits: int, crits: int, die: str, bonus: int):
    num_rolls = hits + (crits * 2)
    num_attacks = hits + crits
    rolls = [rolldice.roll_dice(die)[0] for _ in range(num_rolls)]
    total_bonus = num_attacks * bonus
    total = sum(rolls) + total_bonus
    return total
