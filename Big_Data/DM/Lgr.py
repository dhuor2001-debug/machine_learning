import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
import matplotlib.pyplot as plt


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

    # Logistic Regression
    log_model = LogisticRegression(max_iter=1000)
    log_model.fit(X_train, y_train)

    log_pred = log_model.predict(X_test)
    log_acc = accuracy_score(y_test, log_pred)
    print(f"Logistic Regression accuracy: {log_acc:.2f}\n")
    print("Logistic Regression classification report:")
    print(classification_report(y_test, log_pred))

    cm = confusion_matrix(y_test, log_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=result_encoder.classes_)
    disp.plot()
    plt.title("Logistic Regression Confusion Matrix")
    plt.show()

    # Decision Tree
    dt_model = DecisionTreeClassifier(random_state=42)
    dt_model.fit(X_train, y_train)

    dt_pred = dt_model.predict(X_test)
    dt_acc = accuracy_score(y_test, dt_pred)
    print(f"Decision Tree accuracy: {dt_acc:.2f}\n")
    print("Decision Tree classification report:")
    print(classification_report(y_test, dt_pred))

    cm2 = confusion_matrix(y_test, dt_pred)
    disp2 = ConfusionMatrixDisplay(confusion_matrix=cm2, display_labels=result_encoder.classes_)
    disp2.plot()
    plt.title("Decision Tree Confusion Matrix")
    plt.show()

    # Return both models; logistic regression remains the default for interactive prediction
    return log_model, dt_model, result_encoder, X.columns


def predict_student_result(log_model, dt_model, result_encoder, feature_columns):
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
    # Let user choose which model to use for prediction
    print("\nChoose model for prediction:")
    print("1) Logistic Regression")
    print("2) Decision Tree")
    print("3) Both")
    choice = input("Select 1/2/3 (default 1): ").strip() or "1"
    while choice not in ["1", "2", "3"]:
        print("Invalid choice. Enter 1, 2, or 3.")
        choice = input("Select 1/2/3 (default 1): ").strip() or "1"

    if choice in ["1", "3"]:
        prediction = log_model.predict(input_df)[0]
        label = result_encoder.inverse_transform([prediction])[0]
        print(f"\nLogistic Regression predicted result: {label}")

    if choice in ["2", "3"]:
        prediction_dt = dt_model.predict(input_df)[0]
        label_dt = result_encoder.inverse_transform([prediction_dt])[0]
        print(f"Decision Tree predicted result: {label_dt}")


log_model, dt_model, result_encoder, feature_columns = train_model()
print("Enter student details to predict pass/fail:")
predict_student_result(log_model, dt_model, result_encoder, feature_columns)