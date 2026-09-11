def least_cost_method(costs, supply, demand):
    """
    Solve a balanced transportation problem using the Least Cost Method (LCM).

    Parameters:
        costs: 2D list of transportation costs, shape (m x n)
        supply: list of supplier capacities (length m)
        demand: list of customer demands (length n)

    Returns:
        allocation: 2D list of quantities allocated
        total_cost: total transportation cost
    """
    m = len(costs)
    n = len(costs[0]) if m > 0 else 0

    if len(supply) != m or len(demand) != n:
        raise ValueError("Supply and demand dimensions do not match the cost matrix.")

    if any(s < 0 for s in supply) or any(d < 0 for d in demand):
        raise ValueError("Supply and demand values must be non-negative.")

    if sum(supply) != sum(demand):
        raise ValueError("Total supply must equal total demand for a balanced transportation problem.")

    remaining_supply = supply[:]
    remaining_demand = demand[:]
    allocation = [[0 for _ in range(n)] for _ in range(m)]
    total_cost = 0

    while True:
        feasible = []
        for i in range(m):
            for j in range(n):
                if remaining_supply[i] > 0 and remaining_demand[j] > 0:
                    feasible.append((costs[i][j], i, j))

        if not feasible:
            break

        _, row, col = min(feasible, key=lambda x: x[0])
        qty = min(remaining_supply[row], remaining_demand[col])

        allocation[row][col] = qty
        remaining_supply[row] -= qty
        remaining_demand[col] -= qty
        total_cost += qty * costs[row][col]

    if any(s != 0 for s in remaining_supply) or any(d != 0 for d in remaining_demand):
        raise ValueError("Allocation did not satisfy all supply and demand constraints.")

    return allocation, total_cost


if __name__ == "__main__":
    # Example transportation problem
    costs = [
        [2, 3, 1],
        [5, 4, 8],
        [5, 6, 8],
    ]

    supply = [30, 40, 20]
    demand = [20, 30, 40]

    allocation, total_cost = least_cost_method(costs, supply, demand)

    print("Transportation Problem using Least Cost Method")
    print("=" * 48)
    print("Cost matrix:")
    for row in costs:
        print(row)

    print("\nSupply:", supply)
    print("Demand:", demand)
    print("\nAllocation matrix:")
    for row in allocation:
        print(row)

    print("\nTotal transportation cost =", total_cost)
