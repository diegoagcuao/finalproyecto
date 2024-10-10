import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# Cargar el dataset
df = pd.read_csv('website_classification.csv')

# Preprocesar el dataset
df['text'] = df['cleaned_website_text'].fillna('')  # Usamos la columna 'cleaned_website_text'
X = df['text']  # Características (texto)
y = df['Category']  # Etiquetas (categorías)

# Convertir el texto en vectores numéricos usando TF-IDF
vectorizer = TfidfVectorizer(max_features=5000)
X_tfidf = vectorizer.fit_transform(X)

# Dividir el dataset en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)

# Entrenar el modelo de Logistic Regression
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Hacer predicciones en el conjunto de prueba
y_pred = model.predict(X_test)

# Calcular la precisión del modelo
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy del modelo: {accuracy * 100:.2f}%")

# Guardar el modelo y el vectorizador para usarlos en Flask
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
