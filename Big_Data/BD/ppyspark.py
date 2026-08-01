# 1. Import and initialize the Spark Session
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

spark = spark = SparkSession.builder \
    .appName("MySparkApp") \
    .getOrCreate()  

print(f"Spark Version: {spark.version}")

# Step 2: Load Big Data Efficiently
file_path = "/home/third/.cache/kagglehub/datasets/vinothkannaece/sales-dataset/versions/1/sales_data.csv"

#Load the data and automatically infer the schema
df = spark.read.csv(file_path, header=True, inferSchema=True)

# Inspect the dataset layout without printing all rows
print("\n--- 1. Data Schema Overview ---")
df.printSchema()

# --- 2. Calculate Total Metrics across entire company ---
total_metrics = df.select(
        F.sum("Sales_Amount").alias("Total_Company_Revenue"),
        F.sum("Quantity_Sold").alias("Total_Units_Sold")
)
print("\n--- 2. Global Company Performance ---")
total_metrics.show()

# --- 3. Performance Breakdown by Region ---
region_summary = df.groupBy("Region").agg(
        F.sum("Sales_Amount").alias("Total_Sales"),
        F.avg("Sales_Amount").alias("Average_Order_Value"),
        F.sum("Quantity_Sold").alias("Total_Items_Sold")
).orderBy(F.col("Total_Sales").desc())

print("\n--- 3. Performance Summary by Region ---")
region_summary.show()

# --- 4. Performance Breakdown by Sales Representative ---
rep_summary = df.groupBy("Sales_Rep").agg(
        F.sum("Sales_Amount").alias("Total_Revenue_Generated"),
        F.count("Product_ID").alias("Total_Transactions"),
        F.avg("Quantity_Sold").alias("Avg_Items_Per_Sale")
).orderBy(F.col("Total_Revenue_Generated").desc())

print("\n--- 4. Top Sales Representatives Ranking ---")
rep_summary.show(20, truncate=False)


try:
    df = spark.read.csv(file_path, header=True, inferSchema=True)
    
    # --- 1. Standardize text strings into proper Date format ---
    # Based on your data preview, dates look like '2023-02-03' (yyyy-MM-dd)
    df_with_date = df.withColumn("Cleaned_Date", F.to_date(F.col("Sale_Date"), "yyyy-MM-dd"))
    
    # --- 2. Extract structural time dimensions ---
    df_time_features = df_with_date \
        .withColumn("Year", F.year("Cleaned_Date")) \
        .withColumn("Month_Num", F.month("Cleaned_Date")) \
        .withColumn("Day_of_Week", F.date_format("Cleaned_Date", "E")) # Returns Mon, Tue, etc.

    # --- 3. Monthly Sales Velocity ---
    monthly_trends = df_time_features.groupBy("Year", "Month_Num").agg(
        F.sum("Sales_Amount").alias("Monthly_Revenue"),
        F.count("Product_ID").alias("Order_Volume")
    ).orderBy("Year", "Month_Num")

    print("\n--- 1. Monthly Revenue Performance Trends ---")
    monthly_trends.show(12)

    # --- 4. Most Productive Days of the Week ---
    weekday_trends = df_time_features.groupBy("Day_of_Week").agg(
        F.sum("Sales_Amount").alias("Day_Revenue"),
        F.avg("Sales_Amount").alias("Average_Order_Size")
    ).orderBy(F.col("Day_Revenue").desc())

    print("\n--- 2. Sales Distribution by Weekday ---")
    weekday_trends.show()

except Exception as e:
    print(f"Error compiling time trends: {e}")
