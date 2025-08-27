# Logistics Cost Reconciliation Platform

## 📌 Problem Statement
The goal of this project is to build a **Logistics Cost Reconciliation Platform** that:
1. Accepts truck and load data (via Excel upload or API).
2. Calculates how much each transport company owes, based on their share of total load.
3. Optimizes fleet utilization so that trucks are used as efficiently as possible (minimizing unused capacity).

The key challenges include:
- **Cost allocation**: Dividing the total transport cost fairly across companies based on load distribution.
- **Fleet optimization**: Ensuring trucks are filled close to their capacity, reducing wasted space.

---

## 🚀 My Approach
The solution was divided into two main parts:

### 1. Company Cost Calculation
- Each company’s cost share is calculated proportional to the total load carried by its trucks.
- Small rounding errors are corrected by adjusting the company with the largest share, ensuring the total matches the exact cost.

### 2. Load Optimization
- Implemented a **greedy best-fit decreasing algorithm**:
  - Treat each truck as a “bin” with a fixed capacity.
  - Sort loads in descending order.
  - Assign each load to the best-fit truck using binary search (`bisect`).
  - If no truck fits, create an overflow bin.
- This achieves **O(n log n)** complexity, efficient for large datasets.
- Statistics like utilization %, unused capacity, and truck usage are also reported.

---

## ⚙️ Setup Instructions

### Prerequisites
- Python 3.11.5  
- Virtual environment (recommended)  
- FastAPI & dependencies (listed in `requirements.txt`)  
- HTML+JavaScript (for basic frontend usage, though minimal setup needed)

### Steps to Run the Project
1. **Clone the repository**  
   ```bash
   git clone https://github.com/vimalsonagara/Logistics-Cost-Reconciliation-Platform.git
   cd Logistics-Cost-Reconciliation-Platform
   ```

2. **Create and activate a virtual environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate    # Linux / Mac
   venv\Scripts\activate       # Windows
   ```

3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the backend server**  
   ```bash
   uvicorn backend.main:app --reload
   ```
   - FastAPI backend will start on: `http://127.0.0.1:8000`
   - The basic HTML + JS frontend will also communicate with this backend.

5. **Access the application**  
   - Visit `http://127.0.0.1:8000` to access the frontend.  
   - API docs are available at `http://127.0.0.1:8000/docs`.

---

## 🧩 Explanation of Complex Logic

### Cost Calculation
```python
def calculate_company_costs(df, total_cost: float):
    total_load = df["assigned_load"].sum()
    ...
```
- Divides cost proportionally across companies.
- Adjusts rounding discrepancies to ensure totals match.

### Load Optimization
```python
def greedy_pack_trucks(df):
    # Greedy best-fit decreasing bin packing with binary search
    ...
```
- Sort loads descending.
- Use `bisect` to quickly find best-fit truck for each load.
- Overflow bins created for loads that cannot fit in any truck.

This approach is computationally efficient and balances **speed vs. accuracy**, as exact bin-packing is NP-hard.

---

## ⚠️ Areas Requiring Special Consideration
- **Ambiguity in problem statement**: It was initially unclear whether cost reconciliation or optimization was the main goal, so both aspects were addressed.  
- **Floating-point precision**: Adjustments were required to ensure cost shares add up exactly.  
- **Greedy trade-offs**: The greedy algorithm may not always give the absolute optimal packing, but it is scalable and efficient for large datasets.

---

## 📂 Tech Stack
- **Backend**: Python, FastAPI  
- **Frontend**: HTML + JavaScript (basic UI)  
- **Data Handling**: Pandas (for load/cost calculations)  
- **Server**: Uvicorn (ASGI server for FastAPI)  

---
## Loom video link ##
-- https://www.loom.com/share/c45caf3353fc43b5a78a79482df9e8ab
