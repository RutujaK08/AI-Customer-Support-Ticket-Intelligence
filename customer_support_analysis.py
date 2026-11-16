# ============================================================
# CUSTOMER SUPPORT TICKET ANALYSIS
# Data Quality Assessment and Data Cleaning - Steps 1 to 5
# ============================================================

import re
import warnings
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")

# ------------------------------------------------------------
# 1. LOAD DATASET
# ------------------------------------------------------------

# This script should be saved inside the "notebooks" folder.
project_folder = Path(__file__).resolve().parent.parent
dataset_path = project_folder / "Dataset" / "raw" / "customer_support_tickets.csv"

df = pd.read_csv(dataset_path)

print("\nDataset successfully loaded!")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# ------------------------------------------------------------
# 2. INITIAL DATA EXPLORATION
# ------------------------------------------------------------

print("\nFirst 5 records:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset information:")
df.info()

print("\nStatistical summary:")
print(df.describe(include="all"))

# ------------------------------------------------------------
# 3. MISSING VALUES ANALYSIS
# ------------------------------------------------------------

missing_report = pd.DataFrame({
    "Missing_Count": df.isnull().sum(),
    "Missing_Percentage": (df.isnull().sum() / len(df)) * 100
}).sort_values(by="Missing_Percentage", ascending=False)

print("\nMissing values report:")
print(missing_report)

# ------------------------------------------------------------
# 4. DUPLICATE RECORDS ANALYSIS
# ------------------------------------------------------------

duplicate_rows = df.duplicated().sum()
duplicate_ticket_ids = df["Ticket ID"].duplicated().sum()

print("\nDuplicate rows:", duplicate_rows)
print("Duplicate Ticket IDs:", duplicate_ticket_ids)

# ------------------------------------------------------------
# 5. MISSING VALUES BY TICKET STATUS
# ------------------------------------------------------------

print("\nMissing Resolution by Ticket Status:")
print(
    df.groupby("Ticket Status")["Resolution"]
    .apply(lambda values: values.isnull().sum())
)

print("\nMissing First Response Time by Ticket Status:")
print(
    df.groupby("Ticket Status")["First Response Time"]
    .apply(lambda values: values.isnull().sum())
)

print("\nMissing Customer Satisfaction Rating by Ticket Status:")
print(
    df.groupby("Ticket Status")["Customer Satisfaction Rating"]
    .apply(lambda values: values.isnull().sum())
)

# ------------------------------------------------------------
# 6. DATA TYPE ANALYSIS AND CONVERSION
# ------------------------------------------------------------

print("\nOriginal data types:")
print(df.dtypes)

# Convert date/time columns
date_columns = [
    "Date of Purchase",
    "First Response Time",
    "Time to Resolution"
]

for col in date_columns:
    df[col] = pd.to_datetime(df[col], errors="coerce")

# Ticket ID is an identifier, not a numeric measure
df["Ticket ID"] = df["Ticket ID"].astype("string")

# Keep missing ratings as missing; use nullable integer type
df["Customer Satisfaction Rating"] = pd.to_numeric(
    df["Customer Satisfaction Rating"],
    errors="coerce"
).astype("Int64")

# Ensure Customer Age is numeric
df["Customer Age"] = pd.to_numeric(
    df["Customer Age"],
    errors="coerce"
).astype("Int64")

datatype_report = pd.DataFrame({
    "Column_Name": df.columns,
    "Data_Type": df.dtypes.astype(str).values
})

print("\nUpdated data type report:")
print(datatype_report.to_string(index=False))

# ------------------------------------------------------------
# 7. CATEGORICAL VALUE ANALYSIS
# ------------------------------------------------------------

categorical_columns = [
    "Ticket Type",
    "Ticket Status",
    "Ticket Priority",
    "Ticket Channel",
    "Customer Gender"
]

print("\nCategorical value analysis:")
for col in categorical_columns:
    print(f"\n{col}:")
    print(df[col].value_counts(dropna=False))

print("\nUnique categorical values after trimming spaces:")
for col in categorical_columns:
    print(f"\n{col}:")
    print(df[col].astype("string").str.strip().unique())

# ------------------------------------------------------------
# 8. CUSTOMER AGE VALIDATION
# ------------------------------------------------------------

print("\nCustomer Age Analysis:")
print("Minimum age:", df["Customer Age"].min())
print("Maximum age:", df["Customer Age"].max())

invalid_ages = df[
    (df["Customer Age"] < 18) |
    (df["Customer Age"] > 100)
]

print("Number of unusual age records:", len(invalid_ages))
print(invalid_ages[["Ticket ID", "Customer Age"]].head(10))

# ------------------------------------------------------------
# 9. CUSTOMER SATISFACTION RATING VALIDATION
# ------------------------------------------------------------

print("\nCustomer Satisfaction Rating Analysis:")
print("Unique ratings:")
print(sorted(df["Customer Satisfaction Rating"].dropna().unique()))

invalid_ratings = df[
    (df["Customer Satisfaction Rating"] < 1) |
    (df["Customer Satisfaction Rating"] > 5)
]

print("Minimum rating:", df["Customer Satisfaction Rating"].min())
print("Maximum rating:", df["Customer Satisfaction Rating"].max())
print("Number of invalid ratings:", len(invalid_ratings))

# ------------------------------------------------------------
# 10. PRODUCT PLACEHOLDER ANALYSIS (BEFORE CLEANING)
# ------------------------------------------------------------

# Match the standalone placeholder only. Do not match related tokens
# such as product_purchased_id or product_purchased_name.
placeholder_pattern = (
    r"(?i)[{<]\s*product_purchased(?![A-Za-z0-9_.])\s*[}>]*"
)

placeholder_records = df[
    df["Ticket Description"].str.contains(
        placeholder_pattern,
        na=False,
        regex=True
    )
]

print("\nDescriptions containing product placeholder:",
      len(placeholder_records))
print("\nPlaceholder examples:")
print(
    placeholder_records[
        ["Product Purchased", "Ticket Description"]
    ].head(10).to_string(index=False)
)

# ------------------------------------------------------------
# 11. REPEATED TICKET DESCRIPTION ANALYSIS
# ------------------------------------------------------------

duplicate_descriptions = df["Ticket Description"].duplicated().sum()
print("\nRepeated ticket descriptions:", duplicate_descriptions)

print("\nExamples of repeated descriptions:")
print(
    df[df["Ticket Description"].duplicated(keep=False)][
        ["Ticket ID", "Product Purchased", "Ticket Description"]
    ].head(10).to_string(index=False)
)

# ------------------------------------------------------------
# 12. MISSING VALUES SUMMARY BY TICKET STATUS
# ------------------------------------------------------------

missing_by_status = df.groupby("Ticket Status").agg(
    Total_Tickets=("Ticket ID", "count"),
    Missing_Resolution=("Resolution", lambda x: x.isna().sum()),
    Missing_First_Response=("First Response Time", lambda x: x.isna().sum()),
    Missing_Satisfaction_Rating=(
        "Customer Satisfaction Rating",
        lambda x: x.isna().sum()
    )
)

print("\nMissing values by ticket status:")
print(missing_by_status)

# ------------------------------------------------------------
# 13. DATE RANGE ANALYSIS
# ------------------------------------------------------------

date_columns_for_range = [
    "Date of Purchase",
    "First Response Time",
    "Time to Resolution"
]

print("\nDate range analysis:")
for col in date_columns_for_range:
    print(f"\n{col}")
    print("Earliest:", df[col].min())
    print("Latest:", df[col].max())

# ------------------------------------------------------------
# 14. RESPONSE AND RESOLUTION DATE VALIDATION
# ------------------------------------------------------------

# Ticket Date is derived from Date of Purchase for comparison.
df["Ticket Date"] = df["Date of Purchase"]

print("\nResponse and resolution date validation:")
print(
    "First response before ticket date:",
    (df["First Response Time"] < df["Ticket Date"]).sum()
)
print(
    "First response after ticket date:",
    (df["First Response Time"] > df["Ticket Date"]).sum()
)
print(
    "Resolution before ticket date:",
    (df["Time to Resolution"] < df["Ticket Date"]).sum()
)
print(
    "Resolution after ticket date:",
    (df["Time to Resolution"] > df["Ticket Date"]).sum()
)

# ============================================================
# PART 2: DATA CLEANING
# ============================================================

print("\n" + "=" * 55)
print("DATA CLEANING STARTED")
print("=" * 55)

# ------------------------------------------------------------
# CREATE WORKING COPY
# ------------------------------------------------------------

# Keep original df unchanged. Apply cleaning only to clean_df.
clean_df = df.copy()

print("Original dataset shape:", df.shape)
print("Working dataset shape:", clean_df.shape)

# ------------------------------------------------------------
# REMOVE LEADING AND TRAILING SPACES FROM TEXT COLUMNS
# ------------------------------------------------------------

text_columns = clean_df.select_dtypes(
    include=["object", "string"]
).columns

for col in text_columns:
    clean_df[col] = clean_df[col].str.strip()

print("\nLeading and trailing spaces removed from text columns.")

# ============================================================
# STEP 1: STANDARDIZE CATEGORICAL COLUMNS
# ============================================================

categorical_columns = [
    "Ticket Type",
    "Ticket Status",
    "Ticket Priority",
    "Ticket Channel",
    "Customer Gender"
]

for col in categorical_columns:
    clean_df[col] = (
        clean_df[col]
        .astype("string")
        .str.strip()
        .str.lower()
    )

print("\nStep 1 completed: Categorical values standardized.")

# ============================================================
# STEP 2: MISSING VALUES ANALYSIS
# ============================================================

missing_count = clean_df.isnull().sum()
missing_percentage = (missing_count / len(clean_df)) * 100

cleaning_missing_report = pd.DataFrame({
    "Column_Name": clean_df.columns,
    "Missing_Count": missing_count.values,
    "Missing_Percentage": missing_percentage.values
}).sort_values(by="Missing_Percentage", ascending=False)

print("\nStep 2: Missing values report:")
print(cleaning_missing_report.to_string(index=False))

print("\nTotal missing values:", clean_df.isnull().sum().sum())

# Visualize missing values
plt.figure(figsize=(12, 6))
sns.heatmap(
    clean_df.isnull(),
    cbar=False,
    yticklabels=False,
    cmap="viridis"
)
plt.title("Missing Values Heatmap")
plt.xlabel("Columns")
plt.ylabel("Records")
plt.tight_layout()
plt.show()

# ============================================================
# STEP 3: MISSING VALUES ANALYSIS BY TICKET STATUS
# ============================================================

missing_by_status_clean = clean_df.groupby("Ticket Status").agg(
    Total_Tickets=("Ticket ID", "count"),
    Missing_Resolution=("Resolution", lambda x: x.isnull().sum()),
    Missing_First_Response=(
        "First Response Time",
        lambda x: x.isnull().sum()
    ),
    Missing_Satisfaction_Rating=(
        "Customer Satisfaction Rating",
        lambda x: x.isnull().sum()
    )
)

print("\nStep 3: Missing values by ticket status:")
print(missing_by_status_clean)

missing_percentage_by_status = (
    missing_by_status_clean[
        [
            "Missing_Resolution",
            "Missing_First_Response",
            "Missing_Satisfaction_Rating"
        ]
    ].div(missing_by_status_clean["Total_Tickets"], axis=0) * 100
)

print("\nMissing percentage by ticket status:")
print(missing_percentage_by_status.round(2))

# ============================================================
# STEP 4: VALIDATE MISSING VALUES AGAINST TICKET STATUS
# ============================================================

open_tickets = clean_df[clean_df["Ticket Status"] == "open"]
pending_tickets = clean_df[
    clean_df["Ticket Status"] == "pending customer response"
]
closed_tickets = clean_df[clean_df["Ticket Status"] == "closed"]

print("\nStep 4: Missing value validation")

print("\nOpen tickets:", len(open_tickets))
print(
    "Open tickets without resolution:",
    open_tickets["Resolution"].isnull().sum()
)
print(
    "Open tickets without first response:",
    open_tickets["First Response Time"].isnull().sum()
)

print("\nPending tickets:", len(pending_tickets))
print(
    "Pending tickets without resolution:",
    pending_tickets["Resolution"].isnull().sum()
)
print(
    "Pending tickets without first response:",
    pending_tickets["First Response Time"].isnull().sum()
)

print("\nClosed tickets:", len(closed_tickets))
print(
    "Closed tickets with missing resolution:",
    closed_tickets["Resolution"].isnull().sum()
)
print(
    "Closed tickets with missing first response:",
    closed_tickets["First Response Time"].isnull().sum()
)

print("\nStep 4 completed: Missing values validated against ticket status.")

# ============================================================
# STEP 5: PRODUCT PLACEHOLDER CLEANING
# ============================================================

print("\nStep 5: Product placeholder cleaning started.")

pattern = (
    r"(?i)[{<]\s*product_purchased(?![A-Za-z0-9_.])\s*[}>]*"
)

# Count matching placeholders before cleaning
before_count = clean_df["Ticket Description"].str.contains(
    pattern,
    na=False,
    regex=True
).sum()

print("Placeholders before cleaning:", before_count)


def replace_product_placeholder(row):
    description = row["Ticket Description"]
    product = row["Product Purchased"]

    if pd.isna(description) or pd.isna(product):
        return description

    return re.sub(
        pattern,
        lambda match: str(product),
        description
    )

# Replace placeholders in the working copy only
clean_df["Ticket Description"] = clean_df.apply(
    replace_product_placeholder,
    axis=1
)

# Count matching placeholders after cleaning
after_count = clean_df["Ticket Description"].str.contains(
    pattern,
    na=False,
    regex=True
).sum()

print("Placeholders after cleaning:", after_count)

remaining = clean_df[
    clean_df["Ticket Description"].str.contains(
        pattern,
        na=False,
        regex=True
    )
]

print("Remaining placeholder records:", len(remaining))

if not remaining.empty:
    print("\nInspect these remaining records before making further changes:")
    print(
        remaining[
            ["Ticket ID", "Product Purchased", "Ticket Description"]
        ].to_string(index=False)
    )

print("\nStep 5 completed: Product placeholder cleaning checked.")

# ------------------------------------------------------------
# SUMMARY THROUGH STEP 5
# ------------------------------------------------------------

print("\n" + "=" * 55)
print("SUMMARY: COMPLETED THROUGH STEP 5")
print("=" * 55)

print("Original dataset shape:", df.shape)
print("Working dataset shape:", clean_df.shape)
print("Duplicate rows in original dataset:", df.duplicated().sum())
print("Duplicate Ticket IDs:", df["Ticket ID"].duplicated().sum())
print("Product placeholders before cleaning:", before_count)
print("Product placeholders after cleaning:", after_count)
print("Missing values in working dataset:", clean_df.isnull().sum().sum())

print("\nCleaned dataset preview:")
print(clean_df.head())

print("\nAnalysis and cleaning through Step 5 completed.")

# ============================================================
# STEP 6: DATE AND TIME VALIDATION
# ============================================================

print("\n" + "=" * 50)
print("STEP 6: DATE AND TIME VALIDATION")
print("=" * 50)

date_columns = [
    "Date of Purchase",
    "First Response Time",
    "Time to Resolution"
]

for col in date_columns:
    print("\nColumn:", col)
    print("Missing Values:", clean_df[col].isnull().sum())
    print("Earliest Date:", clean_df[col].min())
    print("Latest Date:", clean_df[col].max())
    print("Data Type:", clean_df[col].dtype)

print("\nSTEP 6 COMPLETED!")

# ============================================================
# STEP 7: CUSTOMER AGE VALIDATION
# ============================================================

print("\n" + "=" * 50)
print("STEP 7: CUSTOMER AGE VALIDATION")
print("=" * 50)

clean_df["Customer Age"] = pd.to_numeric(
    clean_df["Customer Age"],
    errors="coerce"
)

print("Minimum Customer Age:", clean_df["Customer Age"].min())
print("Maximum Customer Age:", clean_df["Customer Age"].max())
print("Missing Customer Ages:", clean_df["Customer Age"].isnull().sum())

invalid_ages = clean_df[
    (clean_df["Customer Age"] < 18) |
    (clean_df["Customer Age"] > 100)
]

print("Number of Unusual Age Records:", len(invalid_ages))

print("\nUnusual Age Records:")
print(
    invalid_ages[
        ["Ticket ID", "Customer Age"]
    ].to_string(index=False)
)

print("\nSTEP 7 COMPLETED!")

# ============================================================
# STEP 8: CUSTOMER SATISFACTION RATING VALIDATION
# ============================================================

print("\n" + "=" * 50)
print("STEP 8: CUSTOMER SATISFACTION RATING VALIDATION")
print("=" * 50)

# Convert ratings into numeric format
clean_df["Customer Satisfaction Rating"] = pd.to_numeric(
    clean_df["Customer Satisfaction Rating"],
    errors="coerce"
)

# Check missing ratings
missing_ratings = clean_df[
    "Customer Satisfaction Rating"
].isnull().sum()

print("\nMissing Satisfaction Ratings:", missing_ratings)

# Check minimum and maximum ratings
print(
    "Minimum Rating:",
    clean_df["Customer Satisfaction Rating"].min()
)

print(
    "Maximum Rating:",
    clean_df["Customer Satisfaction Rating"].max()
)

# Identify ratings outside the valid 1–5 range
invalid_ratings = clean_df[
    (clean_df["Customer Satisfaction Rating"] < 1) |
    (clean_df["Customer Satisfaction Rating"] > 5)
]

print("\nNumber of Invalid Ratings:", len(invalid_ratings))

# Display invalid records
print("\nInvalid Rating Records:")

print(
    invalid_ratings[
        ["Ticket ID", "Customer Satisfaction Rating"]
    ].to_string(index=False)
)

print("\nSTEP 8 COMPLETED!")

# ============================================================
# STEP 9: CATEGORICAL DATA VALIDATION
# ============================================================

print("\n" + "=" * 50)
print("STEP 9: CATEGORICAL DATA VALIDATION")
print("=" * 50)

categorical_columns = [
    "Ticket Type",
    "Ticket Status",
    "Ticket Priority",
    "Ticket Channel",
    "Customer Gender"
]

# Expected categories based on the dataset's observed values
expected_categories = {
    "Ticket Type": [
        "technical issue",
        "billing inquiry",
        "product inquiry",
        "cancellation request",
        "refund request"
    ],
    "Ticket Status": [
        "open",
        "closed",
        "pending customer response"
    ],
    "Ticket Priority": [
        "low",
        "medium",
        "high",
        "critical"
    ],
    "Ticket Channel": [
        "email",
        "phone",
        "chat",
        "social media"
    ],
    "Customer Gender": [
        "male",
        "female",
        "other"
    ]
}

for col in categorical_columns:

    print("\nColumn:", col)

    # Check missing values
    print("Missing Values:", clean_df[col].isnull().sum())

    # Get unique values
    actual_values = set(
        clean_df[col].dropna().astype("string").str.strip().str.lower().unique()
    )

    print("Unique Values:", sorted(actual_values))

    # Identify unexpected categories
    unexpected_values = actual_values - set(expected_categories[col])

    print("Unexpected Categories:", sorted(unexpected_values))

print("\nSTEP 9 COMPLETED!")

# ============================================================
# STEP 10: TEXT DATA CLEANING
# ============================================================

print("\n" + "=" * 50)
print("STEP 10: TEXT DATA CLEANING")
print("=" * 50)

text_columns = [
    "Ticket Description",
    "Resolution"
]

for col in text_columns:

    # Count empty values before cleaning
    before_empty = clean_df[col].isnull().sum()

    # Clean text without changing missing values
    clean_df[col] = (
        clean_df[col]
        .astype("string")
        .str.replace(r"[\r\n\t]+", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )

    # Count empty values after cleaning
    after_empty = clean_df[col].isnull().sum()

    print("\nColumn:", col)
    print("Missing values before cleaning:", before_empty)
    print("Missing values after cleaning:", after_empty)

print("\nCleaned text preview:")
print(
    clean_df[
        ["Ticket Description", "Resolution"]
    ].head(5).to_string(index=False)
)

print("\nSTEP 10 COMPLETED!")

# ============================================================
# STEP 11: FINAL MISSING VALUES ANALYSIS
# ============================================================

print("\n" + "=" * 50)
print("STEP 11: FINAL MISSING VALUES ANALYSIS")
print("=" * 50)

# Calculate missing values
final_missing_count = clean_df.isnull().sum()

final_missing_percentage = (
    final_missing_count / len(clean_df)
) * 100

# Create final missing values report
final_missing_report = pd.DataFrame({
    "Column_Name": clean_df.columns,
    "Missing_Count": final_missing_count.values,
    "Missing_Percentage": final_missing_percentage.values
})

final_missing_report = final_missing_report.sort_values(
    by="Missing_Count",
    ascending=False
)

print("\nFinal Missing Values Report:")
print(final_missing_report.to_string(index=False))

# Calculate total missing values
total_missing = clean_df.isnull().sum().sum()

print("\nTotal Missing Values:", total_missing)
print("Total Rows:", clean_df.shape[0])
print("Total Columns:", clean_df.shape[1])

print("\nSTEP 11 COMPLETED!")

# ============================================================
# STEP 12: FINAL DUPLICATE CHECK
# ============================================================

print("\n" + "=" * 50)
print("STEP 12: FINAL DUPLICATE CHECK")
print("=" * 50)

# Check complete duplicate rows
final_duplicate_rows = clean_df.duplicated().sum()

# Check duplicate Ticket IDs
final_duplicate_ticket_ids = clean_df["Ticket ID"].duplicated().sum()

print("\nFinal Duplicate Rows:", final_duplicate_rows)
print("Final Duplicate Ticket IDs:", final_duplicate_ticket_ids)

# Display duplicate records if found
if final_duplicate_rows > 0:
    print("\nDuplicate Row Records:")
    print(
        clean_df[
            clean_df.duplicated(keep=False)
        ].to_string(index=False)
    )
else:
    print("\nNo duplicate rows found.")

if final_duplicate_ticket_ids > 0:
    print("\nDuplicate Ticket ID Records:")
    print(
        clean_df[
            clean_df["Ticket ID"].duplicated(keep=False)
        ][["Ticket ID", "Ticket Description"]].to_string(index=False)
    )
else:
    print("\nNo duplicate Ticket IDs found.")

print("\nSTEP 12 COMPLETED!")

# ============================================================
# STEP 13: FINAL DATA QUALITY REPORT
# ============================================================

print("\n" + "=" * 50)
print("STEP 13: FINAL DATA QUALITY REPORT")
print("=" * 50)

print("\nDATASET OVERVIEW")
print("Total Records:", clean_df.shape[0])
print("Total Columns:", clean_df.shape[1])

print("\nDATA QUALITY SUMMARY")
print("Missing Values:", clean_df.isnull().sum().sum())
print("Duplicate Rows:", clean_df.duplicated().sum())
print("Duplicate Ticket IDs:", clean_df["Ticket ID"].duplicated().sum())

print("\nCOLUMN DATA TYPES")
print(clean_df.dtypes)

print("\nMISSING VALUES BY COLUMN")
print(clean_df.isnull().sum())

print("\nFINAL DATA QUALITY REPORT COMPLETED!")

# ============================================================
# STEP 14: EXPORT CLEANED DATASET
# ============================================================

print("\n" + "=" * 50)
print("STEP 14: EXPORT CLEANED DATASET")
print("=" * 50)

# Create processed folder
processed_folder = project_folder / "Dataset" / "processed"
processed_folder.mkdir(parents=True, exist_ok=True)

# Export cleaned dataset
output_path = processed_folder / "customer_support_tickets_cleaned.csv"

clean_df.to_csv(output_path, index=False)

print("\nCleaned dataset exported successfully!")
print("File Location:", output_path)
print("Exported Rows:", clean_df.shape[0])
print("Exported Columns:", clean_df.shape[1])

print("\nPART 2: DATA CLEANING COMPLETED!")

# STEP 15: TICKET STATUS DISTRIBUTION

print("\nSTEP 16: TICKET STATUS DISTRIBUTION")

status_count = clean_df["Ticket Status"].value_counts()

print("\nTicket Status Count:")
print(status_count)

plt.figure(figsize=(7, 5))
status_count.plot(kind="bar", rot=0)
plt.title("Ticket Status Distribution")
plt.xlabel("Ticket Status")
plt.ylabel("Number of Tickets")
plt.tight_layout()
plt.show()

print("\nSTEP 16 COMPLETED!")

# STEP 16: TICKET PRIORITY ANALYSIS

priority_count = clean_df["Ticket Priority"].value_counts()

print("\nTicket Priority Distribution:")
print(priority_count)

priority_count.plot(kind="bar", title="Ticket Priority Distribution",
                    xlabel="Priority", ylabel="Ticket Count",
                    rot=0, figsize=(7, 5))
plt.tight_layout()
plt.show()

# STEP 18: TICKET TYPE ANALYSIS

type_count = clean_df["Ticket Type"].value_counts()

print("\nTicket Type Distribution:")
print(type_count)

type_count.plot(kind="bar", title="Ticket Type Distribution",
                xlabel="Ticket Type", ylabel="Ticket Count",
                rot=45, figsize=(9, 5))
plt.tight_layout()
plt.show()

# STEP 17: CUSTOMER GENDER AND AGE ANALYSIS

print("\nCustomer Gender Distribution:")
print(clean_df["Customer Gender"].value_counts())

print("\nCustomer Age Statistics:")
print(clean_df["Customer Age"].describe())

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

clean_df["Customer Gender"].value_counts().plot(
    kind="bar", ax=axes[0], title="Customer Gender Distribution", rot=0
)

clean_df["Customer Age"].dropna().plot(
    kind="hist", bins=15, ax=axes[1], title="Customer Age Distribution"
)

plt.tight_layout()
plt.show()


# STEP 18: PRODUCT-WISE TICKET ANALYSIS

product_count = clean_df["Product Purchased"].value_counts()

print("\nTop 10 Products by Ticket Volume:")
print(product_count.head(10))

product_count.head(10).plot(
    kind="bar", figsize=(10, 5),
    title="Top 10 Products by Ticket Volume",
    xlabel="Product", ylabel="Ticket Count", rot=45
)
plt.tight_layout()
plt.show()

# STEP 19: TICKET CHANNEL ANALYSIS

channel_count = clean_df["Ticket Channel"].value_counts()

print("\nTicket Channel Distribution:")
print(channel_count)

channel_count.plot(
    kind="pie", autopct="%1.1f%%",
    figsize=(7, 7), title="Ticket Channel Distribution"
)
plt.ylabel("")
plt.show()

# STEP 20: CUSTOMER SATISFACTION ANALYSIS

rating_count = clean_df["Customer Satisfaction Rating"].value_counts().sort_index()

print("\nCustomer Satisfaction Rating Distribution:")
print(rating_count)

print("\nAverage Satisfaction Rating:",
      clean_df["Customer Satisfaction Rating"].mean())

rating_count.plot(
    kind="bar", figsize=(7, 5), rot=0,
    title="Customer Satisfaction Rating Distribution",
    xlabel="Rating (1–5)", ylabel="Number of Customers"
)
plt.tight_layout()
plt.show()

# STEP 21: RESPONSE AND RESOLUTION TIME ANALYSIS

time_columns = ["First Response Time", "Time to Resolution"]

print("\nResponse and Resolution Time Analysis")

for col in time_columns:
    print(f"\n{col}")
    print("Available Records:", clean_df[col].notna().sum())
    print("Missing Records:", clean_df[col].isna().sum())
    print("Earliest Timestamp:", clean_df[col].min())
    print("Latest Timestamp:", clean_df[col].max())

# Visualize timestamp availability
clean_df[time_columns].notna().sum().plot(
    kind="bar", rot=0, figsize=(7, 5),
    title="Available Response and Resolution Records",
    ylabel="Number of Records"
)
plt.tight_layout()
plt.show()

print("\nSTEP 23 COMPLETED!")

# STEP 22: KEY BUSINESS INSIGHTS

print("\nKEY BUSINESS INSIGHTS")

print("Total Tickets:", len(clean_df))
print("Most Common Ticket Status:",
      clean_df["Ticket Status"].mode()[0])
print("Most Common Priority:",
      clean_df["Ticket Priority"].mode()[0])
print("Most Common Ticket Type:",
      clean_df["Ticket Type"].mode()[0])
print("Most Common Channel:",
      clean_df["Ticket Channel"].mode()[0])
print("Top Product:",
      clean_df["Product Purchased"].mode()[0])
print("Average Customer Age:",
      round(clean_df["Customer Age"].mean(), 2))
print("Average Satisfaction Rating:",
      round(clean_df["Customer Satisfaction Rating"].mean(), 2))

print("\nPART 3: EDA COMPLETED!")

import pandas as pd

file_path = r"C:\Users\dell\Desktop\AI_Customer_Support_Intelligence\Dataset\processed\customer_support_tickets_cleaned.csv"

check_df = pd.read_csv(file_path)

print("CSV Rows:", len(check_df))
print("CSV Columns:", len(check_df.columns))
print("Missing rows:", check_df.isnull().all(axis=1).sum())

