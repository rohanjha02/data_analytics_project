import pandas as pd

# Load the dataset (replace 'your_dataset.csv' with your actual file)
df = pd.read_csv('model.csv')

# Assuming 'Year' is the column containing the years, 'Population' is the population column, and 'CO2' is the CO2 column
# Sorting by 'Year' in case it's not sorted
df = df.sort_values(by='year')

# Calculate average growth rate for population
average_population_growth_rate = ((df['population'].iloc[-1] / df['population'].iloc[0]) ** (1 / len(df['year']))) - 1

# Function to predict future population
def predict_population(current_population, growth_rate, years_into_future):
    return current_population * (1 + growth_rate) ** years_into_future

# Example usage for predicting future population
current_population = df['population'].iloc[-1]  # Use the latest population from your dataset
years_into_future = int(input("Enter the number of years into the future for population prediction: "))

predicted_population = predict_population(current_population, average_population_growth_rate, years_into_future)
print(f"Predicted population {years_into_future} years into the future: {predicted_population:.2f}")

# Assuming 'CO2' is the column containing CO2 values
# Calculate average growth rate for CO2 based on population growth rate
average_co2_growth_rate = ((df['co2'].iloc[-1] / df['co2'].iloc[0]) ** (1 / len(df['year']))) - 1

# Function to predict future CO2 levels based on population growth
def predict_co2(current_co2, growth_rate, years_into_future):
    return current_co2 * (1 + growth_rate) ** years_into_future

# Example usage for predicting future CO2 levels
current_co2 = df['co2'].iloc[-1]  # Use the latest CO2 value from your dataset
predicted_co2 = predict_co2(current_co2, average_co2_growth_rate, years_into_future)
print(f"Predicted CO2 level {years_into_future} years into the future: {predicted_co2:.2f}")
