import pandas as pd # pyright: ignore[reportMissingModuleSource]
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

# Load the dataset
file_path = "student_pass_fail_dataset.csv"
df = pd.read_csv(file_path)

print("Dataset preview:")
print(df.head())

# Encode categorical values
# Convert Gender to numeric format for the model
# Result is encoded to 0/1 so the classifier can learn it
# Use a binary target: Pass = 1, Fail = 0

df = pd.get_dummies(df, columns=["Gender"], drop_first=True)
result_encoder = LabelEncoder()
df["Result"] = result_encoder.fit_transform(df["Result"])

X = df.drop(columns=["Result"])
y = df["Result"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"\nModel accuracy: {accuracy:.2f}")
print("Sample predictions:")
print(predictions[:10])
print("Actual labels:")
print(y_test.to_numpy()[:10])