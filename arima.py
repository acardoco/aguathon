from sklearn.metrics import mean_squared_error
from statsmodels.tsa.arima_model import ARIMA
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series
import utils

def arima():
    # contrived dataset
    from pre_procesing import transform_dataframe
    path = 'datos/datos.csv'


    df = transform_dataframe(path)
    zgr = df['ZGZ_NR']
    data = zgr.values

    # a diario
    long = int( len(data)/ 24)
    data_daily = data.reshape((long,24))
    data_daily = np.mean(data_daily, axis = 1)
    #******************************************
    def predict(coef, history):
        yhat = 0.0
        for i in range(1, len(coef) + 1):
            yhat += coef[i - 1] * history[-i]
        return yhat

    X = data_daily
    size = len(X) - 7
    train, test = X[0:size], X[size:]
    history = [x for x in train]
    predictions = list()
    for t in range(len(test)):
        model = ARIMA(history, order=(1, 0, 1))
        model_fit = model.fit(trend='nc', disp=False)
        ar_coef = model_fit.arparams
        yhat = predict(ar_coef, history)
        predictions.append(yhat)
        obs = test[t]
        history.append(obs)
        print('>predicted=%.3f, expected=%.3f' % (yhat, obs))
    rmse = np.sqrt(mean_squared_error(test, predictions))
    print('Test RMSE: %.3f' % rmse)

#--------------------------------------------------------------
#--------------------------------------------------------------
#--------------------------------------------------------------
arima()

