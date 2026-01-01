import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score, confusion_matrix
import joblib

df = pd.read_excel("intents.xlsx")
X = df["text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# increase max features so we can memorize more words
vectorizer = TfidfVectorizer(max_features=2000, ngram_range=(1,2))
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

NBmodel = MultinomialNB()
NBmodel.fit(X_train_vec, y_train)
y_pred_nb = NBmodel.predict(X_test_vec)
acc_nb = accuracy_score(y_test, y_pred_nb)
f1_nb = f1_score(y_test, y_pred_nb, average='weighted')
precision_nb = precision_score(y_test, y_pred_nb, average='weighted')
recall_nb = recall_score(y_test, y_pred_nb, average='weighted')

LRmodel = LogisticRegression(max_iter=100)
LRmodel.fit(X_train_vec, y_train)
y_pred_lr = LRmodel.predict(X_test_vec)
acc_lr = accuracy_score(y_test, y_pred_lr)
f1_lr = f1_score(y_test, y_pred_lr, average='weighted')
precision_lr = precision_score(y_test, y_pred_lr, average='weighted')
recall_lr = recall_score(y_test, y_pred_lr, average='weighted')

print("Naive Bayes Accuracy:", acc_nb)
print("Naive Bayes F1 Score:", f1_nb)
print("Naive Bayes Precision:", precision_nb)
print("Naive Bayes Recall:", recall_nb)

print("Logistic Regression Accuracy:", acc_lr)
print("Logistic Regression F1 Score:", f1_lr)
print("Logistic Regression Precision:", precision_lr)
print("Logistic Regression Recall:", recall_lr)

print("\nNaive Bayes Classification Report:\n", classification_report(y_test, y_pred_nb))
print("\nLogistic Regression Classification Report:\n", classification_report(y_test, y_pred_lr))

joblib.dump(NBmodel, "nb_intent_model_6.pkl")
joblib.dump(LRmodel, "lr_intent_model_6.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer_6.pkl")