import pandas as pd
import random

# Load and structure the data
def structure_data(file_path):
    # Read processed csv file
    data = pd.read_csv(file_path)
    # Convert visit_date to datetime
    data["visit_date"] = pd.to_datetime(data["visit_date"])
    # Sort by patient_id and visit_date
    data.sort_values(["patient_id", "visit_date"], inplace = True)
    return data

# Add insurance information
def insurance_info(data, insurance_file, base_cost):
    # read insurance types from insurance.lst
    with open(insurance_file, "r") as insurance_file:
        insurance_types = [line.strip() for line in insurance_file.readlines()]
    
    # randomly assign insurance type using random function, but keeping constant across same patient ID
    data["insurance_type"] = data["patient_id"].apply(lambda patient_id: random.Random(hash(patient_id)).choice(insurance_types))

    # Generate random visit costs based on insurance type with variation between -10 % and 10 %
    data["visit_cost"] = round(data["insurance_type"].apply(lambda x: base_cost[x] * (1 + random.uniform(-0.1, 0.1))), 2)

    return data

# Calculate summary statistics
def summary_stats(data):
    mean_speed = data["walking_speed"].groupby(data["education_level"]).mean()
    print(f"Mean walking speed by education level: \n", mean_speed)
    mean_costs = round(data["visit_cost"].groupby(data["insurance_type"]).mean(), 2)
    print(f"Mean costs by insurance type: \n", mean_costs)
    age_effect = data[["age", "walking_speed"]].corr().iloc[0,1]
    print(f"Correlation between Age and Walking speed: ", age_effect)

# Main codes
file_path = "ms_data.csv"
insurance_file = "insurance.lst"
base_cost = {"Basic" : 100, "Premium": 150, "Platinum": 200}

data = structure_data(file_path)
data = insurance_info(data, insurance_file, base_cost)
summary_stats(data)

# Create new data file containing insurance information
data.to_csv("ms_data_w_insurance.csv", index=False)