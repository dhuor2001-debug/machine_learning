import pandas as pd
from sklearn.preprocessing import labelEncoder
from sklearn.model_selection import logisticRegression

# Load a local CSV file into a DataFrame
df = pd.read_csv("student_pass_Fail_dataset.csv")

# Preview the first 5 rows
print(df.head())

#Encode Result Colum 
#encoder = labelEncoder()
#df["Result"] = encoder.fit