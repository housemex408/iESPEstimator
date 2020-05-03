import numpy as np
import pandas as pd
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn import metrics
from tabulate import tabulate
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import shapiro
from scipy.special import inv_boxcox
from scipy.stats import boxcox
sys.path.append(os.path.abspath(__file__))
import Utilities as utils
import Constants as c

class EffortMeasurements:
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

    def forecast_effort(self):
        data = {
            c.DATE: self.df.index,
            c.NT: self.df[self.type]
        }
        NT = pd.DataFrame(data) 

        NT.columns = ['ds','y']
        NT['y_orig'] = NT['y']
        NT['y'], lam = boxcox(NT['y'])

        m_NT = Prophet(interval_width=0.90)
        m_NT.fit(NT)
        future_NT = m_NT.make_future_dataframe(periods=months, freq='m')
        forecast_NT = m_NT.predict(future_NT)

        m_NT.plot(forecast_NT)

        forecast_NT_inv = pd.DataFrame()
        forecast_NT_inv['ds'] = forecast_NT['ds']
        forecast_NT_inv[['yhat','yhat_upper','yhat_lower']] = forecast_NT[['yhat','yhat_upper','yhat_lower']].apply(lambda x: inv_boxcox(x, lam))

        m_NT.history['y_t'] = m_NT.history['y']
        m_NT.history['y'] = m_NT.history['y_orig']

        NT['y_t'] = NT['y']
        NT['y'] = NT['y_orig']

        m_NT.plot(forecast_NT_inv)

        self.forecast = forecast_NT_inv

        return self.forecast
    
    def predict_effort(self):
        if self.type == c.LINE_CC:
            self.X = self.df[[c.NT_CC, c.NO_CC]]
            self.Y = self.df[c.LINE_CC]
        elif self.type == c.LINE_EC:
            self.X = self.df[[c.NT_EC, c.NO_EC]]
            self.Y = self.df[c.LINE_EC]
        elif self.type == c.MODULE_CC:
            self.X = self.df[[c.NT_CC, c.NO_CC]]
            self.Y = self.df[c.MODULE_CC]
        elif self.type == c.MODULE_EC:
            self.X = self.df[[c.NT_EC, c.NO_EC]]
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

class iROIEstimator:
    cwd = "scripts/exports"

    def __init__(self, project):
        self.project_name = project.split('/')[1]
        self.file_template = "{cwd}/{project_name}/{project_name}_dataset_{task}.csv"    
        self.line_cc = None;
        self.line_ec = None;
        self.module_cc = None;
        self.module_ec = None;
    
    def execute(self):
        for task in c.TASK_LIST:
            tasks = self.file_template.format(cwd=self.cwd, project_name=self.project_name, task = task)
            df = pd.read_csv(tasks)
            
            df[c.DATE] = pd.to_datetime(df[c.DATE])
            df = df.dropna(subset=[c.TASK])
            df.fillna(df.mean(), inplace=True)
            if df.isna().values.any():
                df.fillna(0, inplace=True)

            t_records = len(df)

            # Edge case when < 2 tasks detected
            if t_records < 2:
                break
            
            self.predict_effort(task, df)
    
    def predict_effort(self, task, df):
        # LINE_CC
        self.line_cc = EffortMeasurements(self.project_name, c.LINE_CC, task, df)
        line_cc_results = self.line_cc.predict_effort()
        print("\n{0} - {1} - {2} prediction count: {3}".format(self.project_name, task, c.LINE_CC, line_cc_results.size))
        self.line_cc.calculate_perf_measurements()
        line_cc_output = self.line_cc.create_output_df()
        print(line_cc_output.head())

        # LINE_EC
        self.line_ec = EffortMeasurements(self.project_name, c.LINE_EC, task, df)
        line_ec_results = self.line_ec.predict_effort()
        print("\n{0} - {1} - {2} prediction count: {3}".format(self.project_name, task, c.LINE_EC, line_ec_results.size))
        self.line_ec.calculate_perf_measurements()
        line_ec_output = self.line_ec.create_output_df()
        print(line_ec_output.head())

        # MODULE_CC
        self.module_cc = EffortMeasurements(self.project_name, c.MODULE_CC, task, df)
        module_cc_results = self.module_cc.predict_effort()
        print("\n{0} - {1} - {2} prediction count: {3}".format(self.project_name, task, c.MODULE_CC, module_cc_results.size))
        self.module_cc.calculate_perf_measurements()
        module_cc_output = self.module_cc.create_output_df()
        print(module_cc_output.head())
        

        # MODULE_EC
        self.module_ec = EffortMeasurements(self.project_name, c.MODULE_EC, task, df)
        module_ec_results = self.module_ec.predict_effort()
        print("\n{0} - {1} - {2} prediction count: {3}".format(self.project_name, task, c.MODULE_EC, module_ec_results.size))
        self.module_ec.calculate_perf_measurements()
        module_ec_output = self.module_ec.create_output_df()
        print(module_ec_output.head())

    # def forecastEffort(self):
        # FORECASTING
        # for task in c.TASK_LIST:
        #     forecast_NT = forecastVariable(c.NT_CC, df, predictionMonths)
        #     forecast_NO = forecastVariable(c.NO_CC, df, predictionMonths)
        #     forecast_T_Module= forecastVariable(c.T_MODULE, df, predictionMonths)

        #     data = {
        #         c.NT_CC: forecast_NT['yhat'],
        #         c.NO_CC: forecast_NO['yhat'],
        #         c.T_MODULE: forecast_T_Module['yhat']
        #     }
        #     dateIndex = forecast_NT['ds']
        #     results = predictFutureEffort(data, dateIndex, c.MODULE_CC, rf_regressor)
        #     displayFutureEffort(results, c.MODULE_CC, predictionYears)
    

    # def calculateROI():

    # def printLine():

angular = iROIEstimator("angular/angular")
angular.execute()