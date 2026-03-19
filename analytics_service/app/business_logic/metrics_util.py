

# Total Revenue
# Revenue per day
# Revenue per month
# Revenue growth rate

# Average Order Value (AOV)
# Order Distribution

# Total Orders
# Orders per day
# Orders per week
# Orders per month
# Orders growth rate


# Average Order Value
# Largest Order
# Smallest Order
# Median Order Value


def calc_total_order_count(orders: dict) -> int:
    total = len(orders['items'])
    return total

def calc_total_revenue(orders: dict) -> float:
    profit = sum(order['total'] for order in orders['items'])
    return profit



