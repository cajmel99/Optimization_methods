import matplotlib.pyplot as plt
import pandas as pd

# Load the data
file_path = '/Users/marysia/Optimization_methods/data/results.csv'
df = pd.read_csv(file_path)


plt.figure(figsize=(12, 6))
plt.plot(df['Max'], label='Max', color='blue')
plt.plot(df['Min'], label='Min', color='red')
plt.plot(df['Avg'], label='Avg', color='green')

plt.title('Max, Min, and Avg Values Over Time')
plt.xlabel('Observation Number')
plt.ylabel('Values')
plt.legend()
plt.grid(True)

plt.show()