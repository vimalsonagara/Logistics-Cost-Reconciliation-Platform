def calculate_company_costs(df, total_cost: float):
    total_load = df["assigned_load"].sum()
    if total_load == 0:
        return {}
    company_loads = df.groupby("company")["assigned_load"].sum()
    result = {}
    for company, load in company_loads.items():
        result[company] = round(total_cost * (load / total_load), 2)
    diff = round(total_cost - sum(result.values()), 2)
    if abs(diff) >= 0.01:
        largest = max(result, key=result.get)
        result[largest] = round(result[largest] + diff, 2)
    return result
