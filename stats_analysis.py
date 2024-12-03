import statsmodels.api as sm
from statsmodels.stats.anova import anova_lm
from statsmodels.formula.api import ols
import seaborn as sns
from scipy import stats
import matplotlib.pyplot as plt
import pandas as pd

# Get data from Question 2
data = pd.read_csv("ms_data_w_insurance.csv")

# Analyze walking speed
model1 = sm.OLS.from_formula("walking_speed ~ education_level + age", data=data).fit()
#model1 = sm.MixedLM.from_formula("walking_speed ~ education_level + age", groups = "patient_id", data=data)
#result1 = model1.fit()
print(f"Regression model for walking speed analysis: \n\n{model1.summary()}")

# Testing for significant trends
anova_result1 = anova_lm(model1, typ=2)
print(f"\n\nAnova test results: \n\n{anova_result1}")

# Coefficients and confidence intervals
print(f"\n\nCoefficients: \n\n{model1.params}")
print(f"\n\nConfidence Intervals: \n\n{model1.conf_int()}")
#t_stat1, p_val1 = stats.ttest_ind(data["insurance_type"], data["visit_cost"])
#print(f"t-test: {t_stat1}\n p-value: {p_val1}")

# Simple analysis on costs 
insurance_grouped = data.groupby("insurance_type")["visit_cost"]
mean_cost = insurance_grouped.mean()
std_cost = insurance_grouped.std()
print(f"Mean visit cost by insurance types: \n{mean_cost}\n\nStandard deviation of visit cost by insurance types: \n{std_cost}")

# Statistical Analysis
#t_stat, p_val = stats.ttest_ind(data["insurance_type"], data["visit_cost"])
model4 = ols("visit_cost ~ insurance_type", data=data).fit()
anova_result2 = anova_lm(model4)

# Boxplot for costs vs insurance types
plt.figure(figsize=(10,6))
sns.boxplot(x = "insurance_type", y = "visit_cost", data = data, order = ["Basic", "Premium", "Platinum"])
plt.title("Visit Costs by Insurance Types")
plt.xlabel("Insurance Types")
plt.ylabel("Costs")
plt.show()

# Calculate effect sizes using Cohen's d
basic = data[data["insurance_type"] == "Basic"]["visit_cost"]
premium = data[data["insurance_type"] == "Premium"]["visit_cost"]
platinum = data[data["insurance_type"] == "Platinum"]["visit_cost"]

mean_diff1 = basic.mean() - premium.mean()
mean_diff2 = basic.mean() - platinum.mean()
mean_diff3 = premium.mean() - platinum.mean()

pooled_std1 = ((basic.std()**2 + premium.std()**2) /2)**0.5
pooled_std2 = ((basic.std()**2 + platinum.std()**2) /2)**0.5
pooled_std3 = ((premium.std()**2 + platinum.std()**2) /2)**0.5

cohens_diff1 = mean_diff1 / pooled_std1
cohens_diff2 = mean_diff2 / pooled_std2
cohens_diff3 = mean_diff3 / pooled_std3

print(f"\n\nBasic v.s. Premium: {cohens_diff1} \nBasic v.s. Platinum: {cohens_diff2} \nPremium v.s. Platinum: {cohens_diff3}")

# Advanced analysis - Age and Education interaction effects on walking speed
model2 = ols("walking_speed ~ education_level * age", data=data)
result2 = model2.fit()
print(f"\n\nEducation age interaction effects on walking speed: \n{result2.summary()}")

# possible confounder other than education level and age = visit_date
model3 = ols("walking_speed ~ education_level * age + visit_date", data=data)
result3 = model3.fit()
print(f"\n\nCoefficients:\n {result2.params}")
print(f"\nP-Values:\n {result2.pvalues}")