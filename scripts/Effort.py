import numpy as np
import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn import metrics
from tabulate import tabulate
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import shapiro
import matplotlib.pyplot as plt
import scipy.stats as st
from scipy.special import inv_boxcox
from scipy.stats import boxcox
from fbprophet import Prophet
from datetime import datetime
sys.path.append(os.path.abspath(__file__))
import Utilities as utils
import Constants as c

class Effort:
    def __init__(self, project, value, task, df):
        self.type = value
        self.task = task
        self.df = df
        self.t_records = len(self.df)
        self.project_name = project
        self.model = None
        self.predictions = None
        self.r_squared = None
        self.r_squared_adj = None
        self.mae = None
        self.mse = None
        self.rmse = None
        self.pred25 = None
        self.pred50 = None
        self.predicted_effort = None
        self.shapiro_wilk_test = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.X = None
        self.Y = None
        self.results = None

    def forecast_variable(self, variable, predicton_months):
        data = {
            c.DATE: self.df.index,
            c.NT: self.df[variable]
        }
        NT = pd.DataFrame(data) 

        NT.columns = ['ds','y']
        NT['y'].replace(0, 1, inplace = True)
        NT['y_orig'] = NT['y']
        NT['y'], lam = boxcox(NT['y'])

        m_NT = Prophet(interval_width=0.90)
        m_NT.fit(NT)
        future_NT = m_NT.make_future_dataframe(periods = predicton_months, freq='m')
        forecast_NT = m_NT.predict(future_NT)

        # m_NT.plot(forecast_NT)

        forecast_NT_inv = pd.DataFrame()
        forecast_NT_inv['ds'] = forecast_NT['ds']
        forecast_NT_inv[['yhat','yhat_upper','yhat_lower']] = forecast_NT[['yhat','yhat_upper','yhat_lower']].apply(lambda x: inv_boxcox(x, lam))

        m_NT.history['y_t'] = m_NT.history['y']
        m_NT.history['y'] = m_NT.history['y_orig']

        NT['y_t'] = NT['y']
        NT['y'] = NT['y_orig']

        # m_NT.plot(forecast_NT_inv)
        forecast_NT_inv['yhat'].fillna(forecast_NT_inv['yhat'].tail(24).mean(), inplace=True)

        self.forecast = forecast_NT_inv

        return self.forecast

    def forecast_effort(self, data, dateIndex, variable, rf_regressor):
        X_Future = pd.DataFrame(data) 
        y_pred_rf = rf_regressor.predict(X_Future)
        y_pred_index = dateIndex

        resultData = {variable: y_pred_rf.round(2), c.DATE: y_pred_index}
        results = pd.DataFrame(resultData) 
        return results
    
    def predict_effort(self):
        if self.type == c.LINE_CC:
            self.X = self.df[[c.NT_CC, c.NO_CC]]
            self.Y = self.df[c.LINE_CC]
        elif self.type == c.LINE_EC:
            self.X = self.df[[c.NT_EC, c.NO_EC]]
            self.Y = self.df[c.LINE_EC]
        elif self.type == c.MODULE_CC:
            self.X = self.df[[c.NT_CC, c.NO_CC, c.T_MODULE]]
            self.Y = self.df[c.MODULE_CC]
        elif self.type == c.MODULE_EC:
            self.X = self.df[[c.NT_EC, c.NO_EC, c.T_MODULE]]
            self.Y = self.df[c.MODULE_EC]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.Y, train_size=0.75, test_size=0.25, random_state=0)
        self.model = RandomForestRegressor(n_estimators=300, random_state=0)
        self.model.fit(self.X_train, self.y_train)
        self.predictions = self.model.predict(self.X_test)

        return self.predictions

    def calculate_diff(self):
        data = {
            c.OBSERVED:self.y_test, 
            c.PREDICTED:self.predictions.round(2), 
            c.DIFFERENCE:abs(self.y_test - self.predictions).round(2), 
            c.PERCENT_ERROR:(abs(self.y_test - self.predictions)/self.y_test).round(2)
        }
        self.results = pd.DataFrame(data)
        return self.results
    
    def calculate_perf_measurements(self):
        self.calculate_diff()
        self.r_squared = round(self.model.score(self.X_test, self.y_test), 2)
        self.r_squared_adj = round(utils.calculated_rsquared_adj(self.X, self.X_test, self.r_squared), 2)
        self.mae = round(metrics.mean_absolute_error(self.y_test, self.predictions), 2)
        self.mse = round(metrics.mean_squared_error(self.y_test, self.predictions), 2)
        self.rmse = round(np.sqrt(metrics.mean_squared_error(self.y_test, self.predictions)), 2)
        self.pred25 = round(utils.calculate_PRED(0.25, self.results), 2)
        self.pred50 = round(utils.calculate_PRED(0.50, self.results), 2)

    def create_output_df(self):
        row_df = pd.DataFrame({c.PROJECT: [self.project_name],
                      c.MODEL: [self.type],
                      c.TASK: [self.task],
                      c.R_SQUARED: [self.r_squared],
                      c.R_SQUARED_ADJ: [self.r_squared_adj],
                      c.MAE: [self.mae],
                      c.MSE: [self.mse],
                      c.RMSE: [self.rmse],
                      c.PRED_25: [self.pred25],
                      c.PRED_50: [self.pred50],
                      c.T_RECORDS: self.t_records})
        return row_df
