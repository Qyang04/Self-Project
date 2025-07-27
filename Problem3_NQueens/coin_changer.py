import math

# Initialize set of coins & target amount
coins = [1, 3, 4, 5]
amount = 7

def coin_change(coins, amount):
    # Create array (x) of size amount+1
    x = [0] + [math.inf] * (amount + 1)

    # Replace each index from x[1] through x[amount] with least no. of coins needed
    for a in range(1, amount + 1):
        # try each coin starting with the smallest value
        for c in coins:
            if c <= a:
                # if we use coin c, we add 1 to x[a-c]
                candidate = x[a - c] + 1
                # replace x[a] with smaller value
                if candidate < x[a]:
                    x[a] = candidate

    # If x[amount] is still > amount, no solution exists
    return x[amount] if x[amount] <= amount else -1


print(coin_change(coins, amount))
