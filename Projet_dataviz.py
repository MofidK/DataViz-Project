# Imports
import numpy as np
import pandas as pd
import os
import plotly.express as px

# Fonction pour transformer en dataframe les donnees json
def to_dataframe(data): 
  data_ = {key:[] for key in data['fields'][0].keys()}
  for i in range(len(data)):
    data_tmp = data['fields'][i]
    for key in data_.keys():
      try:
        data_[key].append(data_tmp[key])
      except:
        data_[key].append(' ')
  data_ = pd.DataFrame(data_)
  return data_

# Chargmenet et creation du dataframe
chemin = 'C:/Users/Mofid Krim/Desktop/DCDEV5/Dataviz/'
data = pd.read_json(chemin + 'vehicules-commercialises.json')
df = to_dataframe(data)

# Fonctions pour le traitement des donnees
def cat_hybride(label):
    return 'Non Renseingé' if label == ' ' else label

def co2(label):
  return 0 if label == ' ' else label

# Nettoyage du dataset
df['hybride'] = df['hybride'].apply(lambda x: cat_hybride(x))
df['co2_g_km'] = df['co2_g_km'].apply(lambda x: co2(x))
df['co2_g_km_approx'] = df['co2_g_km'].apply(lambda x: np.round(x)) # Pour afficher la taille en fonction du CO2 emis

# Jeux de donnees filtres par an
subset_1 = df[(df.annee == '2015')]
subset_2 = df[(df.annee == '2014')]

# Plots

fig_1 = px.histogram(df, x="annee", category_orders = dict(annee = [str(year) for year in range(2001, 2016)]), color = "hybride")
chemin_1_html = os.path.join(chemin, 'Vehicules_par_an.html')
fig_1.write_html(chemin_1_html)

fig_2 = px.scatter(subset_1, x="consommation_mixte_l_100km", y="co2_g_km", color="hybride", hover_name="modele_dossier", log_x=True, size_max=60)
chemin_2_html = os.path.join(chemin, 'Co2.html')
fig_2.write_html(chemin_2_html)

fig_3 = px.scatter(subset_1, x="carburant", y="consommation_mixte_l_100km", size="co2_g_km_approx", color="hybride", hover_name="modele_dossier")
chemin_3_html = os.path.join(chemin, 'Type_de_carburant.html')
fig_3.write_html(chemin_3_html)

fig_4 = px.scatter(subset_2, x="gamme", y="consommation_mixte_l_100km", size="co2_g_km_approx", color="hybride", hover_name="modele_dossier")
chemin_4_html = os.path.join(chemin, 'Gamme.html')
fig_4.write_html(chemin_4_html)