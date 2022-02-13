# -*- coding: utf-8 -*-
"""multilayer_perceptron.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jNkTGieZf21PZOZBQFT6ESKVOnyuEJaP
"""

! git clone https://github.com/ml4teachers/mlp.git
! git pull

import pandas as pd

movies = pd.read_json("/content/mlp/movie_df.json")

movies.head()

#Dummies für Jahrzehnte erstellen
labels = ["{0}s".format(i, i + 10) for i in range(1930, 2030, 10)]
movies["period"] = pd.cut(movies.release, range(1930, 2040, 10), right=False, labels=labels)
period_dummies = pd.get_dummies(movies["period"])

#Dummies für Bewertungen erstellen
labels = ["score:{0}".format(i, i + 10) for i in range(1, 10, 1)]
movies["rating"] = pd.cut(movies.vote_average, range(1, 11, 1), right=False, labels=labels)
rating_dummies = pd.get_dummies(movies["rating"])

#Dummies für Anzahl Bewertungen erstellen
labels = [">400", "400-1500", "1500-4000", ">4000"]
movies["votes"] = pd.cut(movies.vote_count, [0, 400, 1500, 4000, 40000], right=False, labels=labels)
vote_dummies = pd.get_dummies(movies["votes"])

#Dummies für Genres erstellen
genre_dummies = movies["genres"].str.get_dummies(sep="|")

#Neues DataFrame "movie_dummies" erstellen durch Zusammenführen der eben erstellten Dummyvariablen
movie_dummies = movies[["id"]].join(genre_dummies).join(period_dummies).join(rating_dummies).join(vote_dummies)

movie_dummies.head()

import csv

#Liste erstellen mit allen IDs der Filme, die in unserem DataFrame vorhanden sind
valid_movies = movies["id"].to_list()

good_movies = []
bad_movies = []

#Beispielratings öffnen und in gute und schlechte Filme unterteilen (Grenze = 5)
with open('/content/mlp/ratings.csv', 'r') as file:
    csv_file = csv.reader(file)
    for line in csv_file:
        if line[3] != 'Name' and float(line[8]) > 5 and int(line[0]) in valid_movies:
            good_movies.append(int(line[0]))
        elif line[3] != 'Name' and int(line[0]) in valid_movies:
            bad_movies.append(int(line[0]))

#Gesamtliste mit Film-ID's erstellen, die gleich viele gute und schlechte Filme enthält
if len(bad_movies) > len(good_movies):
  movie_list = good_movies + bad_movies[:len(good_movies)]
else:
  movie_list = good_movies[:len(bad_movies)] + bad_movies

from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

X = []
y = []

#Eingaben für Multilayer Perceptron erstellen
for movie in movie_list:
  X.append(movie_dummies[movie_dummies["id"] == movie].to_numpy()[0][1:].tolist())

#Ausgaben für Multylayer Perceptron erstellen
for i in range(0, len(X)):
    if i < (len(X)/2):
        y.append(1)
    else:
        y.append(0)

#Training- und Test Set erstellen und randomisieren
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=1)

#Multilayer Perceptron trainieren
clf = MLPClassifier(solver='lbfgs', activation='tanh', hidden_layer_sizes=(6, 2), random_state=1).fit(X_train, y_train)

#Multilayer Perceptron testen
clf.score(X_test, y_test)

#id ersetzen mit Film-ID und trainiertes MLP mit Filmen testen:
#Beispiel "Matrix Resurections" mit ID = 624860 ||
#                                               \/
test = movie_dummies[movie_dummies["id"] == 624860].to_numpy()[0][1:].tolist()
prediction = clf.predict([test])[0]
if prediction == 1:
  pred = "Like"
else:
  pred = "Dislike"
print(pred)