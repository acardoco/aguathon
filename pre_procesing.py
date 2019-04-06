import datetime
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.ar_model import AR
from statsmodels.tsa.vector_ar.var_model import VAR

lista_de_municipios = ['ALAGON_NR', 'GRISEN_NR', 'NOVILLAS_NR', 'TAUSTE_NR', 'TUDELA_NR', 'ZGZ_NR']
path = 'datos/datos.csv'
# ----------------------------------------------------------------------------------------------------------------------
def transform_dataframe(path):
    df = pd.read_csv(path, delimiter=';')
    df['RIESGO'] = np.where(df['RIESGO'] == True, 1, 0)
    df.replace([np.inf, -np.inf], np.nan)
    df.fillna(0, inplace=True)

    df['time'] = pd.to_datetime(df['time'])
    #df['time'] = df.sort_values(by='time')
    #df.set_index('time', inplace=True)

    print(df.dtypes)

    return df
# ----------------------------------------------------------------------------------------------------------------------
# -----------------------------------------------Vector Auto Regression (VAR)-------------------------------------------
def testing_var():
    df = transform_dataframe(path)

    #creating the train and validation set

    train = df.iloc[:int(0.8*(len(df)))]
    valid = df.iloc[int(0.8*(len(df))):]

    model = VAR(endog=train)
    model_fit = model.fit()

    # make prediction on validation
    prediction = model_fit.forecast(model_fit.y, steps=len(valid))

    cols = df.columns.values
    #converting predictions to dataframe
    pred = pd.DataFrame(index=range(0,len(prediction)),columns=cols)
    for j in range(0,10):
        for i in range(0, len(prediction)):
           pred.iloc[i][j] = prediction[i][j]

    #check rmse
    for i in cols:
        p=pred[i]
        v=valid[i]
        print('rmse value for', i, 'is : ', np.sqrt(mean_squared_error(p, v)))

    #make final predictions
    model = VAR(endog=df)

    model_fit = model.fit()
    yhat = model_fit.forecast(model_fit.y, steps=1)
    print(yhat)

# ----------------------------------------------------------------------------------------------------------------------
def plot_df(df):
#df.plot(x='time', y=lista_de_municipios[:2])
    # plot each column
    df = df.loc[df['time'].dt.year == 2018]
    print(df['time'])
    df.plot(subplots=True, x='time', y=lista_de_municipios)

    plt.show()
# ----------------------------------------------------------------------------------------------------------------------
