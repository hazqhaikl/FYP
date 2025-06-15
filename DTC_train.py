import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.tree import plot_tree
import seaborn as sns
import joblib

# Define the name of your CSV file
csv_file_name = 'FYP.csv'

# --- 1. Load the CSV file ---
try:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_file_name)
    print(f"Successfully loaded '{csv_file_name}'.")
    print("\nInitial Data Head:")
    print(df.head())
    #print("\nData Info:")
    #df.info()
except FileNotFoundError:
    print(f"Error: The file '{csv_file_name}' was not found.")
    print("Please ensure 'FYP2.csv' is in the same directory as this script.")
    exit()

# --- GRAPH PLOT ---
print("\n--- Visualizing Voltage Patterns for Each Adulterant Type (by Concentration) ---")
if 'Adulterant_Type' in df.columns and 'Concentration' in df.columns:
    plt.figure(figsize=(12, 6))

    # --- Plot for Water Adulteration ---
    plt.subplot(1, 2, 1)
    water_df = df[df['Adulterant_Type'] == 'Water'].copy()
    sns.lineplot(data=water_df, x='Concentration', y='Voltage_mV', marker='o', color='blue')
    plt.title('Voltage Pattern - Water Adulteration')
    plt.xlabel('Water Concentration (Ratio)')
    plt.ylabel('Voltage (mV)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45, ha='right')

    # --- Plot for Fe3O4 Adulteration ---
    plt.subplot(1, 2, 2)
    fe_df = df[df['Adulterant_Type'] == 'Fe3O4'].sort_values(by='Concentration')
    sns.lineplot(data=fe_df, x='Concentration', y='Voltage_mV', marker='o', color='orange')
    plt.title('Voltage Pattern - Fe₃O₄ Adulteration')
    plt.xlabel('Fe₃O₄ Concentration (grams)')
    plt.ylabel('Voltage (mV)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(ticks=fe_df['Concentration'].unique())

    plt.tight_layout()
    plt.show()
    
else:
    print("Error: 'Adulterant_Type' or 'Concentration' column not found in the DataFrame. Skipping Voltage pattern plots.")

# --- BOX PLOT ---
print("\n--- Visualizing Voltage Distribution by Quality ---")
plt.figure(figsize=(8, 6))
quality_order = ['Good', 'Medium', 'Poor']
sns.boxplot(x='Quality', y='Voltage_mV', data=df, order=quality_order)
plt.title('Distribution of Sensor Voltage across Honey Quality Categories')
plt.xlabel('Honey Quality')
plt.ylabel('Voltage (mV)')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# --- 2. Pre-process data ---
df_processed = pd.get_dummies(df, columns=['Adulterant_Type'], drop_first=False)
label_encoder = LabelEncoder()
df_processed['Quality_Encoded'] = label_encoder.fit_transform(df_processed['Quality'])
X = df_processed[['Voltage_mV'] + [col for col in df_processed.columns if 'Adulterant_Type_' in col]]
y = df_processed['Quality_Encoded']

print("\n--- Data Pre-processing Complete ---")
#print("\nProcessed Data Head (Features used for training):")
#print(X.head())
#print("\nEncoded Quality Labels (Target Variable):")
#print(y.head())
print(f"\nUnique Quality Labels Found: {label_encoder.classes_}")
print(f"Mapping: {list(zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)))}")

# --- 3. Split data into training and testing sets ---
test_size_ratio = 0.3
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=test_size_ratio, random_state=42, stratify=y
)

print(f"\n--- Data Split Complete ---")
print(f"Total samples: {len(df)}")
print(f"Training set size: {len(X_train)} samples")
print(f"Testing set size: {len(X_test)} samples")
#print(f"Training set shape (features): {X_train.shape}, (target): {y_train.shape}")
#print(f"Testing set shape (features): {X_test.shape}, (target): {y_test.shape}")

# --- 4. Train the Decision Tree Classifier model ---
dt_model = DecisionTreeClassifier(random_state=42)
print("\n--- Training Decision Tree Classifier ---")
dt_model.fit(X_train, y_train)
print("Model training complete.")

# --- 5. Validation ---
print("\n--- Model Validation ---")
y_pred = dt_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy on Test Set: {accuracy:.2f}")

target_names_sorted = [
    label for label, _ in sorted(
        zip(label_encoder.classes_, label_encoder.transform(label_encoder.classes_)),
        key=lambda item: item[1]
    )
]
print("\nClassification Report (Test Set):")
print(classification_report(y_test, y_pred, target_names=target_names_sorted, zero_division=0))

print("\n--- Visualizing the Confusion Matrix ---")
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=label_encoder.classes_,
            yticklabels=label_encoder.classes_)
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix')
plt.tight_layout()
plt.show()

# --- 6. Save the trained model and label encoder ---
model_filename = 'decision_tree_model.pkl'
label_encoder_filename = 'label_encoder.pkl'
print("\n--- Saving Model and Label Encoder ---")
joblib.dump(dt_model, model_filename)
joblib.dump(label_encoder, label_encoder_filename)

# --- 7. Visualize the Decision Tree ---
print("\n--- Visualizing the Decision Tree Structure ---")
plt.figure(figsize=(20, 10))
plot_tree(
    dt_model,
    feature_names=X.columns,
    class_names=label_encoder.classes_,
    filled=True,
    rounded=True,
    fontsize=10
)
plt.title("Decision Tree Classifier Structure")
plt.tight_layout()
plt.show()

print(f"Trained Decision Tree Model saved as '{model_filename}'")
print(f"Label Encoder saved as '{label_encoder_filename}'")

print("\n--- Python Script Execution Complete ---")
