import csv, random, string, copy, os
random.seed(42)

industries = ["Technology","Healthcare","Fintech","EdTech","E-commerce","SaaS","Biotech","Logistics","AI/ML","Cybersecurity"]
countries = ["USA","UK","India","Germany","Canada","Australia","Singapore","France","Brazil","Israel"]
stages = ["Seed","Series A","Series B","Series C","Growth","Pre-IPO"]

rows = []
for i in range(1, 101):
    rows.append({
        "Company": f"StartupCo_{i:03d}",
        "Industry": random.choice(industries),
        "Country": random.choice(countries),
        "Founded_Year": random.randint(2008, 2022),
        "Funding_Stage": random.choice(stages),
        "Total_Funding_M": round(random.uniform(0.1, 300.0), 2),
        "Revenue_M": round(random.uniform(0.5, 500.0), 2),
        "Employee_Count": random.randint(5, 2000),
        "Customer_Count": random.randint(50, 50000),
        "ARPU": round(random.uniform(20.0, 5000.0), 2),
        "Monthly_Churn_Rate": round(random.uniform(1.0, 45.0), 2),
        "Revenue_Growth_Pct": round(random.uniform(-10.0, 120.0), 2),
        "Is_Profitable": random.choice([0, 1]),
    })

os.makedirs("tasks", exist_ok=True)

def write_csv(path, data):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        w.writeheader()
        w.writerows(data)

# EASY
easy = copy.deepcopy(rows)
for i in random.sample(range(100), 5):
    easy[i]["Revenue_M"] = ""
write_csv("tasks/task_easy.csv", easy)

# MEDIUM
medium = copy.deepcopy(rows)
for col in ["Total_Funding_M","Revenue_M","Employee_Count","ARPU","Monthly_Churn_Rate"]:
    for i in random.sample(range(100), 8):
        medium[i][col] = ""
misspells = {"Technology":["technology","Tech","Technolgy"],"Fintech":["fintech","Fin Tech","Fintceh"],"SaaS":["saas","SAAS","SaaS "],"EdTech":["edtech","Edtech "],"AI/ML":["AI","ai/ml","ai ml"]}
for i in random.sample(range(100), 12):
    orig = medium[i]["Industry"]
    if orig in misspells:
        medium[i]["Industry"] = random.choice(misspells[orig])
write_csv("tasks/task_medium.csv", medium)

# HARD
hard = copy.deepcopy(rows)
idxs = random.sample(range(100), 4)
hard[idxs[0]]["Employee_Count"] = 999999
hard[idxs[1]]["Revenue_M"] = 99999.99
hard[idxs[2]]["ARPU"] = 0.0001
hard[idxs[3]]["Monthly_Churn_Rate"] = 999.9
for r in hard:
    r["JUNK_COL"] = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
num_cols = ["Total_Funding_M","Revenue_M","Employee_Count","Customer_Count","ARPU","Monthly_Churn_Rate","Revenue_Growth_Pct","Founded_Year"]
cells = [(i, col) for i in range(100) for col in num_cols]
for i, col in random.sample(cells, int(len(cells)*0.20)):
    hard[i][col] = ""
write_csv("tasks/task_hard.csv", hard)

print("✅ All 3 CSVs created in /tasks folder")
