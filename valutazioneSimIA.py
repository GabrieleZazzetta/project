#Zazzetta Gabriele, mat 347093

from simscheduler import Process, FCFS, SJF, Priority, RoundRobin, read_processes_from_file

import tensorflow as tf
from sklearn.model_selection import train_test_split
import numpy as np
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

#Definizione del modello TensorFlow
def create_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(64, activation='relu', input_shape=input_shape),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

#Funz. per preparare i dati di input per il modello
def preprocess_data(results):
    process_features = [process[1:] for process in results]  #Nome del processo ignorato
    return np.array(process_features)

def train_model(model, X_train, y_train):
    X_train = np.array(X_train)
    y_train = np.array(y_train)  #Convertiamo y_train in un array NumPy
    model.fit(X_train, y_train, epochs=10, batch_size=32)
    
def evaluate_model(model, X_test, y_test):
    #Converti y_test in un array NumPy
    y_test = np.array(y_test)
    
    #Converti X_test in un array NumPy
    X_test = np.array(X_test)
    
    #Valutazione del modello
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Test accuracy: {accuracy}")

#Funz. per valutare i risultati dell'algoritmo SJF utilizzando un modello di machine learning
def check_results_SJF(results):
    input_data = preprocess_data(results)
    labels = [1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1]  #Etichette corrispondenti all'output dell'algoritmo SJF
    
    #Altre Etichette
    for i in range(39):
        results.append((f"P{i+13}", np.random.randint(1, 10), np.random.randint(1, 5)))  #Processi brevi
        labels.append(0)  #Etichette per i nuovi processi brevi
    for i in range(39):
        results.append((f"P{i+52}", np.random.randint(10, 30), np.random.randint(1, 5)))  #Processi lunghi
        labels.append(1)  #Etichette per i nuovi processi lunghi
    
    #Suddivide i dati in set di addestramento e test
    X_train, X_test, y_train, y_test = train_test_split(input_data, labels, test_size=0.2, random_state=42)
    model = create_model(input_shape=(input_data.shape[1],)) #creo modello
    train_model(model, X_train, y_train) #addestro modello
    evaluate_model(model, X_test, y_test) #valuto accuracy del modello sui dati di test


process_data = [
    ("P1", 10, 2),   #Processo breve con priorità bassa
    ("P2", 29, 3),   #Processo lungo con priorità media
    ("P3", 3, 4),    #Processo breve con priorità alta
    ("P4", 7, 5),    #Processo breve con priorità massima
    ("P5", 12, 1),   #Processo medio con priorità bassa
    ("P6", 1, 5),    #Processo molto breve con priorità massima
    ("P7", 30, 2),   #Processo molto lungo con priorità bassa
    ("P8", 15, 3),   #Processo medio con priorità media
    ("P9", 5, 4),    #Processo breve con priorità alta
    ("P10", 20, 1),  #Processo medio con priorità massima
    ("P11", 2, 3),   #Processo molto breve con priorità media
    ("P12", 25, 4),  #Processo molto lungo con priorità alta
    ("P13", np.random.randint(1, 10), np.random.randint(1, 5)),
    ("P14", np.random.randint(10, 30), np.random.randint(1, 5)),
]

#Aggiungo 38 nuovi processi brevi(etichetta 0)
for i in range(38):
    process_data.append((f"P{i+15}", np.random.randint(1, 10), np.random.randint(1, 5)))

#Aggiungo 38 nuovi processi lunghi(etichetta 1)
for i in range(38):
    process_data.append((f"P{i+54}", np.random.randint(10, 30), np.random.randint(1, 5)))

check_results_SJF(process_data)  #valutazione dell'efficacia dell'SJF in combinazione con il modello creato con TensorFlow