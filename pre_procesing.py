import datetime
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

lista_de_municipios = ['ALAGON_NR', 'GRISEN_NR', 'NOVILLAS_NR', 'TAUSTE_NR', 'TUDELA_NR', 'ZGZ_NR']

# ----------------------------------------------------------------------------------------------------------------------
df = pd.read_csv('datos/datos.csv', delimiter=';')
df['time'] = pd.to_datetime(df['time'])
df['time'] = df.sort_values(by='time')
df.fillna(0)

# ----------------------------------------------------------------------------------------------------------------------
#df.plot(x='time', y=lista_de_municipios[:2])
# plot each column

values = df.values
plt.figure()
i = 1
groups = np.arange(1,7)
for group in groups:
    plt.subplot(len(groups), 1, i)
    plt.plot(values[:, group])
    plt.title(df.columns[group], y=0.5, loc='right')
    i += 1
plt.show()