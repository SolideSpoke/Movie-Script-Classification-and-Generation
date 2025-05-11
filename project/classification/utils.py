import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from collections import Counter
import seaborn as sns


test_size = 0.2
random_state = 42
top_k = 15

def train_test(model,df_filtered_one_genre_to_train,equilibrate=False,desc=None,plots=None):

    encoder = LabelEncoder()
    if not equilibrate:
        X_train,X_test , y_train,y_test = train_test_split(df_filtered_one_genre_to_train['Script'],df_filtered_one_genre_to_train['filtered_genre'],test_size=test_size,random_state=random_state)
    else:
        minn = df_filtered_one_genre_to_train['filtered_genre'].value_counts().min()
        list_equilibrate = []
        for genre in df_filtered_one_genre_to_train['filtered_genre'].unique():
            list_equilibrate.append(df_filtered_one_genre_to_train.loc[df_filtered_one_genre_to_train['filtered_genre'] == genre].sample(minn))
        df_equilbrate = pd.concat(list_equilibrate)
        X_train,X_test , y_train,y_test = train_test_split(df_equilbrate['Script'],df_equilbrate['filtered_genre'],test_size=test_size,random_state=random_state)
    y_train_encoded = encoder.fit_transform(y_train)
    y_test_encoded = encoder.transform(y_test)

    model.fit(X_train, y_train_encoded)
    y_pred = model.predict(X_test)
    string_equilibrate = "balanced" if equilibrate else "unbalanced"
    y_pred_label = encoder.inverse_transform(y_pred)
    print(f"Model: {desc}")
    print(f"Features dimension: {len(X_train), len(model[0].vocabulary_)}")
    print(f"Classification Report {string_equilibrate}:\n", classification_report(y_test, y_pred_label))
    
    if plots:
        vectorizer_name = list(model.named_steps.keys())[0]
        model_name = list(model.named_steps.keys())[1]
        n = len(plots)
        if "top_words" in plots:
            vectorizer = model.named_steps[vectorizer_name]
            model_instance = model.named_steps[model_name]
            print(model_instance)
            feature_names = np.array(vectorizer.get_feature_names_out())
            if hasattr(model_instance, "feature_log_prob_"): 
                class_probs = model_instance.feature_log_prob_
            elif hasattr(model_instance, "coef_"):  
                class_probs = model_instance.coef_
            for i, class_label in enumerate(model.named_steps[model_name].classes_):
                top_tokens = feature_names[np.argsort(class_probs[i])[-top_k:]]
                print(f"Top {top_k} mots pour la classe '{encoder.inverse_transform([class_label])[0]}': {top_tokens}")
            n -= 1
    
        _,axes = plt.subplots(1,n,figsize=(12,5))
        if not isinstance(axes, np.ndarray):
            axes = [axes]
        i=0
        if "matrix" in plots:
            cm = confusion_matrix(y_test_encoded, y_pred, labels=model.classes_)
            disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=encoder.classes_)
            disp.plot(ax=axes[i]) 
            axes[i].set_title("Matrice de confusion")
            i+=1
        if "avg_words" in plots:
            print(f"Try avg_words")
            vectorizer = model.named_steps[vectorizer_name]  # Obtenir le vectorizer
            model_instance = model.named_steps[model_name]  # Obtenir l'instance du modèle

            # Récupérer les noms des features (mots)
            feature_names = np.array(vectorizer.get_feature_names_out())

            # Si le modèle est Naive Bayes (ou tout modèle ayant l'attribut 'feature_count_')
            if hasattr(model_instance, "feature_count_"):
                print(f"This is Naives Bayes")
                word_counts_per_class = model_instance.feature_count_.sum(axis=1)  # Comptage des mots par classe
                class_counts = np.bincount(y_train_encoded)  # Comptage des occurrences des classes

                # Calcul de la moyenne des mots par classe
                average_word_count_per_class = word_counts_per_class / class_counts

            # Si le modèle est un modèle linéaire comme LogisticRegression
            elif hasattr(model_instance, "coef_"):
                # Calcul de la fréquence des mots dans les données d'entraînement pour chaque classe
                print(f"This is LogisticRegression")
                class_counts = np.bincount(y_train_encoded)
                word_frequencies_per_class = np.zeros((model_instance.coef_.shape[0], len(feature_names)))

                    # Calculer la fréquence des mots pour chaque classe en fonction des prédictions
                for j, class_label in enumerate(model_instance.classes_):  # ← utilise j ici
                    top_tokens = feature_names[np.argsort(class_probs[j])[-top_k:]]
                    print(f"Top {top_k} mots pour la classe '{encoder.inverse_transform([class_label])[0]}': {top_tokens}")


                    # Calcul de la moyenne des mots par classe
                    average_word_count_per_class = word_frequencies_per_class.sum(axis=1) / class_counts

            else:
                print(f"Error not attribute")
                raise AttributeError(f"Le modèle {model_name} n'a pas d'attribut pour compter les mots.")

            df_word = pd.DataFrame({
                "Classe": encoder.classes_,
                "Nombre total de mots": average_word_count_per_class
            })

            # Affichage avec seaborn
            sns.barplot(x="Classe", y="Nombre total de mots", data=df_word, ax=axes[i])
            axes[i].set_title("Nombre total de mots par classe")
            i += 1

        plt.tight_layout()
        plt.show()



