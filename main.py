import pandas as pd

ds = pd.read_csv("ds_salaries.csv")

# print(ds.head())

# Remove first column, salary, and salary currency. Use only USD salaries for comparison. 

ds_clean = ds.drop(ds[['salary', 'salary_currency', 'Unnamed: 0']], axis = 1)

# print(ds_clean.head())

# Check for any NA values in the dataframe

print(ds_clean.isnull().sum())

# Combine and replace some categorical job titles to be more simple

ds_clean["job_title"] = ds_clean["job_title"].replace("ML Engineer", "Machine Learning Engineer")
ds_clean["job_title"] = ds_clean["job_title"].replace("Finance Data Analyst", "Financial Data Analyst")
ds_clean["job_title"] = ds_clean["job_title"].replace("Computer Vision Engineer", "Computer Vision Software Engineer")
ds_clean["job_title"] = ds_clean["job_title"].replace("Analytics Engineer", "Data Analytics Engineer")


### Question 1: What job titles on average make more than $100,000 annually in the United States? 

print("\nQuestion 1: What job titles on average make more than $100,000 annually in the United States?\n")

subset = ds_clean.groupby('job_title').filter(lambda x: len(x) > 1)
subset = subset[subset["company_location"] == "US"]
subset["average_salary"] = subset.groupby('job_title')["salary_in_usd"].transform('mean')
subset = subset[subset['average_salary'] > 100000]
averages = subset.groupby('job_title')['salary_in_usd'].mean().sort_values(ascending = True)

print(round(averages,2))

### Question 2: What is the salary range for data scientists at each experience level?

print("\n\nQuestion 2: What is the salary range for data scientists at each experience level?\n")
salary_range_by_level = pd.DataFrame([], columns=['min_salary_usd', 'max_salary_usd'])
salary_range_by_level['max_salary_usd'] = ds_clean.groupby('experience_level')['salary_in_usd'].max().sort_values(ascending=True)
salary_range_by_level['min_salary_usd'] = ds_clean.groupby('experience_level')['salary_in_usd'].min()
print(salary_range_by_level)

### Question 3: How does remote ratio affect entry level job salary in different locations?

print("\nQuestion 3: How does remote ratio affect entry level job salary in different locations?\n")

pd.set_option('display.max_rows', None)

filtered_df = ds_clean[ds_clean['experience_level'] == "EN"]
filtered_df = filtered_df.groupby('job_title').filter(lambda x: len(x) > 1)
remote_ratio_location = filtered_df.groupby(["remote_ratio", "company_location"])["salary_in_usd"].mean()
print(remote_ratio_location)

pd.set_option('display.max_rows', 20)

### Question 4: Which employee residence and company location combination has the highest salary?
print("\nQuestion 4: Which employee residence and company location combination has the highest salary?\n")
employee_company_location = ds_clean.groupby(['employee_residence', 'company_location']).sum()

max_employee_company_location = employee_company_location['salary_in_usd'].idxmax()
print(max_employee_company_location)

### Question 5: Which job title has the highest average remote ratio?
print("\nQuestion 5: Which job title has the highest average remote ratio?\n")
job_titles = ds_clean.groupby(['job_title']).sum()

data_engineer_roles = ds_clean[ds_clean['job_title'] == "Data Engineer"]
average_remote_ratio = data_engineer_roles['remote_ratio'].mean()

non_data_engineer_roles = ds_clean[ds_clean['job_title'] != "Data Engineer"]
ext_avg_remote_ratio = non_data_engineer_roles['remote_ratio'].mean()

highest_remote_ratio = job_titles['remote_ratio'].idxmax()
print(f"{highest_remote_ratio} has the highest average remote ratio of all job titles, with an average remote ratio of  {average_remote_ratio}% compared to the average remote ratio among all other positions, which is {round(ext_avg_remote_ratio, 2)}%")