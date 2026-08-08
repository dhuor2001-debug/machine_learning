import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def train_model():
    file_path = "student_pass_fail_dataset.csv"
    df = pd.read_csv(file_path)

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

    print(f"Model accuracy: {accuracy:.2f}\n")
    return model, result_encoder, X.columns


def predict_student_result(model, result_encoder, feature_columns):
    gender = input("Enter gender (Male/Female): ").strip().title()
    while gender not in ["Male", "Female"]:
        print("Invalid gender. Please enter Male or Female.")
        gender = input("Enter gender (Male/Female): ").strip().title()

    try:
        age = float(input("Enter age: "))
        marks = float(input("Enter marks: "))
        attendance = float(input("Enter attendance percentage: "))
    except ValueError:
        print("Please enter numeric values for age, marks, and attendance.")
        return

    feature_values = {
        "Age": age,
        "Marks": marks,
        "Attendance": attendance,
        "Gender_Male": 1 if gender == "Male" else 0,
    }

    input_df = pd.DataFrame([feature_values], columns=feature_columns)
    prediction = model.predict(input_df)[0]
    label = result_encoder.inverse_transform([prediction])[0]

    print(f"\nPredicted result: {label}")


model, result_encoder, feature_columns = train_model()
print("Enter student details to predict pass/fail:")
predict_student_result(model, result_encoder, feature_columns)