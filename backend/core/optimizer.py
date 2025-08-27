import bisect
from typing import List, Dict

#=====optimize aproch with the nlogn complexity=================#
def greedy_pack_trucks(df):
    # Step 1: Convert DataFrame to list of load records
    loads = df[["truck_id", "capacity", "assigned_load", "company"]].to_dict("records")

    # Step 2: Sort loads by assigned load descending
    loads_sorted = sorted(loads, key=lambda x: x["assigned_load"], reverse=True)

    # Step 3: Initialize bins (existing trucks)
    # We'll keep two parallel lists:
    # - bins_info: list of dicts with bin details
    # - bins_remaining_sorted: sorted list of (remaining capacity, bin index in bins_info)
    bins_info = []
    bins_remaining_sorted = []  # List of tuples: (remaining_capacity, bin_index)

    for idx, row in enumerate(loads):
        bin_data = {
            "truck_id": row["truck_id"],
            "capacity": row["capacity"],
            "remaining": row["capacity"],
            "allocated": 0.0,
            "company": row["company"]
        }
        bins_info.append(bin_data)
        # Insert initial remaining capacity with bin index in sorted order
        bisect.insort(bins_remaining_sorted, (bin_data["remaining"], idx))

    assignments = []

    # Step 4: Assign loads using best-fit decreasing with binary search
    for load in loads_sorted:
        assigned_load = load["assigned_load"]

        # Use binary search to find the first bin with remaining >= assigned_load
        # bins_remaining_sorted is sorted by remaining capacity ascending
        idx = bisect.bisect_left(bins_remaining_sorted, (assigned_load, -1))

        if idx == len(bins_remaining_sorted):
            # No bin found, create overflow bin
            new_bin_index = len(bins_info)
            new_bin_id = f"overflow_bin_{new_bin_index + 1}"
            new_bin = {
                "truck_id": new_bin_id,
                "capacity": assigned_load,
                "remaining": 0.0,
                "allocated": assigned_load,
                "company": "Unassigned"
            }
            bins_info.append(new_bin)
            # Insert new bin with zero remaining space
            bisect.insort(bins_remaining_sorted, (new_bin["remaining"], new_bin_index))

            assignments.append({
                "original_truck": load["truck_id"],
                "assigned_load": assigned_load,
                "placed_in": new_bin_id,
                "company": "Unassigned"
            })
        else:
            # Bin found
            remaining_capacity, bin_index = bins_remaining_sorted[idx]
            bin = bins_info[bin_index]

            # Remove old entry from sorted list
            del bins_remaining_sorted[idx]

            # Update bin
            bin["remaining"] -= assigned_load
            bin["allocated"] += assigned_load

            # Insert updated remaining capacity back to sorted list
            bisect.insort(bins_remaining_sorted, (bin["remaining"], bin_index))

            assignments.append({
                "original_truck": load["truck_id"],
                "assigned_load": assigned_load,
                "placed_in": bin["truck_id"],
                "company": bin["company"]
            })

    # Step 5: Compute stats
    total_capacity = sum(b["capacity"] for b in bins_info)
    total_load = sum(b["allocated"] for b in bins_info)
    used_trucks = sum(1 for b in bins_info if b["allocated"] > 0)
    unused_capacity = sum(b["remaining"] for b in bins_info)
    utilization_percent = round((total_load / total_capacity) * 100, 2) if total_capacity > 0 else 0.0

    return {
        "total_capacity": float(total_capacity),
        "total_load": float(total_load),
        "used_trucks": used_trucks,
        "unused_capacity": float(round(unused_capacity, 2)),
        "utilization_percent": utilization_percent,
        "assignments": assignments,
        "bins": bins_info
    }

#=================best fir algo n^2 approch =========================

# def greedy_pack_trucks(df):
#     # Step 1: Convert DataFrame to list of load records
#     loads = df[["truck_id", "capacity", "assigned_load", "company"]].to_dict("records")

#     # Step 2: Sort loads by assigned load descending
#     loads_sorted = sorted(loads, key=lambda x: x["assigned_load"], reverse=True)

#     # Step 3: Initialize bins (existing trucks)
#     bins = [{
#         "truck_id": row["truck_id"],
#         "capacity": row["capacity"],
#         "remaining": row["capacity"],
#         "allocated": 0.0,
#         "company": row["company"]
#     } for row in loads]

#     # Step 4: Assign loads using best-fit decreasing
#     assignments = []
#     for load in loads_sorted:
#         best_bin_index = None
#         min_space_left = None

#         for i, bin in enumerate(bins):
#             if load["assigned_load"] <= bin["remaining"]:
#                 space_left = bin["remaining"] - load["assigned_load"]
#                 if (min_space_left is None) or (space_left < min_space_left):
#                     min_space_left = space_left
#                     best_bin_index = i

#         if best_bin_index is not None:
#             # Place load in the best bin found
#             bin = bins[best_bin_index]
#             bin["remaining"] -= load["assigned_load"]
#             bin["allocated"] += load["assigned_load"]
#             assignments.append({
#                 "original_truck": load["truck_id"],
#                 "assigned_load": load["assigned_load"],
#                 "placed_in": bin["truck_id"],
#                 "company": bin["company"]
#             })
#         else:
#             # Create new overflow bin
#             new_id = f"overflow_bin_{len(bins) + 1}"
#             bins.append({
#                 "truck_id": new_id,
#                 "capacity": load["assigned_load"],
#                 "remaining": 0.0,
#                 "allocated": load["assigned_load"],
#                 "company": "Unassigned"
#             })
#             assignments.append({
#                 "original_truck": load["truck_id"],
#                 "assigned_load": load["assigned_load"],
#                 "placed_in": new_id,
#                 "company": "Unassigned"
#             })

#     # Step 5: Compute stats
#     total_capacity = sum(b["capacity"] for b in bins)
#     total_load = sum(b["allocated"] for b in bins)
#     used_trucks = sum(1 for b in bins if b["allocated"] > 0)
#     unused_capacity = sum(b["remaining"] for b in bins)
#     utilization_percent = round((total_load / total_capacity) * 100, 2) if total_capacity > 0 else 0.0

#     return {
#         "total_capacity": float(total_capacity),
#         "total_load": float(total_load),
#         "used_trucks": used_trucks,
#         "unused_capacity": float(round(unused_capacity, 2)),
#         "utilization_percent": utilization_percent,
#         "assignments": assignments,
#         "bins": bins
#     }



# ============First fit algo===========================#
# def greedy_pack_trucks(df):
#     # Step 1: Convert DataFrame to list of load records
#     loads = df[["truck_id", "capacity", "assigned_load", "company"]].to_dict("records")

#     # Step 2: Sort loads by assigned load (descending)
#     loads_sorted = sorted(loads, key=lambda x: x["assigned_load"], reverse=True)

#     # Step 3: Initialize empty bins from existing trucks
#     bins = [{
#         "truck_id": row["truck_id"],
#         "capacity": row["capacity"],
#         "remaining": row["capacity"],
#         "allocated": 0.0,
#         "company": row["company"]
#     } for row in loads]

#     # Step 4: Assign loads using greedy first-fit
#     assignments = []
#     for load in loads_sorted:
#         placed = False
#         for bin in bins:
#             if load["assigned_load"] <= bin["remaining"]:
#                 bin["remaining"] -= load["assigned_load"]
#                 bin["allocated"] += load["assigned_load"]
#                 assignments.append({
#                     "original_truck": load["truck_id"],
#                     "assigned_load": load["assigned_load"],
#                     "placed_in": bin["truck_id"],
#                     "company": bin["company"]
#                 })
#                 placed = True
#                 break

#         if not placed:
#             # Create new bin (if needed — i.e., overflow)
#             new_id = f"overflow_bin_{len(bins) + 1}"
#             bins.append({
#                 "truck_id": new_id,
#                 "capacity": load["assigned_load"],
#                 "remaining": 0.0,
#                 "allocated": load["assigned_load"],
#                 "company": "Unassigned"
#             })
#             assignments.append({
#                 "original_truck": load["truck_id"],
#                 "assigned_load": load["assigned_load"],
#                 "placed_in": new_id,
#                 "company": "Unassigned"
#             })

#     # Step 5: Compute stats
#     total_capacity = sum(b["capacity"] for b in bins)
#     total_load = sum(b["allocated"] for b in bins)
#     used_trucks = sum(1 for b in bins if b["allocated"] > 0)
#     unused_capacity = sum(b["remaining"] for b in bins)
#     utilization_percent = round((total_load / total_capacity) * 100, 2) if total_capacity > 0 else 0.0

#     return {
#         "total_capacity": float(total_capacity),
#         "total_load": float(total_load),
#         "used_trucks": used_trucks,
#         "unused_capacity": float(round(unused_capacity, 2)),
#         "utilization_percent": utilization_percent,
#         "assignments": assignments,
#         "bins": bins
#     }
