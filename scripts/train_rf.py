import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# Load parsed BLAST results
df = pd.read_csv("results/blast_hits_parsed.csv")

# Features and labels
X = df[["pident","length","bitscore"]]
y = df["staxids"].astype(str)

# Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train RF model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Test
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(clf, "models/rf_model.pkl")
print("Model saved to models/rf_model.pkl")
