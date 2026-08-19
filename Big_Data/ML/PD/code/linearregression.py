import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset from the sibling Data folder
# The script is in /Big_Data/ML/PD/code, so the CSV is one level up.
df = pd.read_csv('../Data/Salary_Data.csv')

# Remove missing values if any
if df.isnull().sum().any():
    df = df.dropna()

# Create experience categories for summary and plotting
bins = [0, 5, 10, 15, 20, 25, 30]
labels = ['0-5', '6-10', '11-15', '16-20', '21-25', '26+']
df['Experience Category'] = pd.cut(df['Years of Experience'], bins=bins, labels=labels, right=False)

# Show basic category counts
print('Education Level counts:')
print(df['Education Level'].value_counts())
print('\nJob Title counts:')
print(df['Job Title'].value_counts())
print('\nExperience category counts:')
print(df['Experience Category'].value_counts(dropna=False))

# Show average salary by education level, job title, and experience category
summary = (
    df.groupby(['Education Level', 'Job Title', 'Experience Category'], as_index=False)['Salary']
    .mean()
    .sort_values(['Education Level', 'Job Title', 'Experience Category'])
)

print('\nAverage Salary by Education Level, Job Title, and Experience Category:')
print(summary.head(20).to_string(index=False))

# Prepare model inputs
X = df[['Age', 'Gender', 'Education Level', 'Job Title', 'Years of Experience']]
y = df['Salary']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Encode categorical variables and fit linear regression
preprocessor = ColumnTransformer(
    transformers=[
        ('num', 'passthrough', ['Age', 'Years of Experience']),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['Gender', 'Education Level', 'Job Title'])
    ]
)

model = Pipeline([
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print('\nLinear Regression Results:')
print(f'RMSE: {rmse:,.2f}')
print(f'R^2 Score: {r2:.4f}')

# Plot predicted vs actual salary by years of experience
plot_df = pd.DataFrame({
    'Years of Experience': X_test['Years of Experience'].reset_index(drop=True),
    'Actual Salary': y_test.reset_index(drop=True).astype(float),
    'Predicted Salary': y_pred
}).sort_values('Years of Experience')

plt.figure(figsize=(10, 6))
plt.scatter(plot_df['Years of Experience'], plot_df['Actual Salary'], alpha=0.6, label='Actual Salary')
plt.plot(plot_df['Years of Experience'], plot_df['Predicted Salary'], color='red', linewidth=2, label='Predicted Salary')
plt.title('Salary Prediction using Linear Regression')
plt.xlabel('Years of Experience')
plt.ylabel('Salary')
plt.legend()
plt.grid(True)
plt.tight_layout()
output_path = 'salary_prediction.png'
plt.savefig(output_path)
plt.close()
print(f'\nPlot saved to {output_path}')

