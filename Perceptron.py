import random
import matplotlib.pyplot as plt
import numpy as np

items = 25

user_bewertungen = []
voraussagen = []
abw_voraussagen = []
gewichtete_voraussagen = []
abw_gewichtete_voraussagen = []
kritiker = {}

# Items und Bewertungen erstellen

for i in range(0, items):
    user_bewertungen.append(random.randint(1, 5))

print(user_bewertungen)

# Ähnliche Bewertungen
# print("Ähnliche Bewertungen")
for i in range(0, 10):
    kritiker[i] = {}
    for j in range(0, items):
        kritiker[i][j] = []
        kritik = int(random.normalvariate(user_bewertungen[j], 1))
        if kritik <= 1:
            kritik = 1
        elif kritik >= 5:
            kritik = 5
        kritiker[i][j] = [kritik, 1]

# Abweichende Bewertungen
# print("Abweichende Bewertungen")
for i in range(10, 20):
    kritiker[i] = {}
    for j in range(0, items):
        kritiker[i][j] = []
        kritik = int(random.normalvariate(user_bewertungen[j], 1))
        if kritik <= 1:
            kritik = 5
        elif kritik == 4:
            kritik = 2
        elif kritik == 2:
            kritik = 4
        elif kritik >= 5:
            kritk = 1
        kritiker[i][j] = [kritik, 1]

# Voraussagen ohne Anpassung der Gewichte
for i in range(0, items):
    sum_kritiken = 0
    sum_gewichte = 0
    voraussage = 0
    for j in range(0, 20):
        sum_kritiken += kritiker[j][i][0]
        sum_gewichte += kritiker[j][i][1]
        voraussage = sum_kritiken / sum_gewichte
    abweichung = round(abs(user_bewertungen[i] - voraussage), 1)
    voraussagen.append(round(voraussage, 1))
    abw_voraussagen.append(abweichung)

print(abw_voraussagen)
print(sum(abw_voraussagen))

# Anpassung der Gewichte
for i in range(0, items - 1):
    for j in range(0, 20):
        if kritiker[j][i][0] == user_bewertungen[i]:
            kritiker[j][i + 1][1] = kritiker[j][i][1] + 0.1
            if kritiker[j][i][1] >= 3:
                kritiker[j][i][1] = 3
        elif abs(kritiker[j][i][0] - user_bewertungen[i]) == 1:
            kritiker[j][i + 1][1] = kritiker[j][i][1]
        elif abs(kritiker[j][i][0] - user_bewertungen[i]) >= 2:
            kritiker[j][i + 1][1] = kritiker[j][i][1] - 0.1
            if kritiker[j][i][1] <= -1:
                kritiker[j][i][1] = -1

# Voraussagen nach Anpassung der Gewichte
for i in range(0, items):
    sum_kritiken = 0
    sum_gewichte = 0
    voraussage = 0
    for j in range(0, 20):
        sum_kritiken += kritiker[j][i][0] * kritiker[j][i][1]
        sum_gewichte += kritiker[j][i][1]
        voraussage = sum_kritiken / sum_gewichte
    abweichung = round(abs(user_bewertungen[i] - voraussage), 1)
    gewichtete_voraussagen.append(round(voraussage, 1))
    abw_gewichtete_voraussagen.append(abweichung)

print(abw_gewichtete_voraussagen)
print(sum(abw_gewichtete_voraussagen))

plot_zufall = np.array(abw_voraussagen)
plot_gew = np.array(abw_gewichtete_voraussagen)

plt.plot(plot_zufall, color='b')
plt.plot(plot_gew, color='r')
plt.show()
