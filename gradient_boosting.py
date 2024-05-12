import pandas as pd 
import numpy as np 
from xgboost import XGBRegressor
from datetime import date,timedelta
from sklearn.model_selection import train_test_split,RandomizedSearchCV
from extract_data import request_data
import schedule
import time 

def gradient_boosting():
    df = pd.read_csv("/Users/aditirajesh/Desktop/program_files/python/python_6sem/DATA_PLANTS/plant2/data6_2.csv")
    df['YIELD'] = pd.to_numeric(df['YIELD'])
    df['DATE'] = pd.to_datetime(df['DATE'])

    x = df.iloc[:,1:4].values
    y = df.iloc[:,-1].values

    #x_train,x_test,y_train,y_test = train_test_split(x,y,random_state=1)

    xg_regressor= XGBRegressor(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bytree=0.9, gamma=0.1, learning_rate=1,
       max_delta_step=0, max_depth=5, min_child_weight=7, missing=1,
       n_estimators=1200, n_jobs=1, nthread=None, random_state=0, reg_alpha=0,
       reg_lambda=1, scale_pos_weight=1, seed=None,
       subsample=1,
       objective="reg:squarederror")
    
    xg_regressor.fit(x,y)
    print('regression complete')

    return xg_regressor

gradient_boosting()

def realtime_data(ambient_temp,modular_temp,irradiance):
    data = request_data()

    ambient_temp.append(data[0])
    modular_temp.append(data[1])
    irradiance.append(data[2])

    

    ambient_mean = sum(ambient_temp)/len(ambient_temp)
    modular_mean = sum(modular_temp)/len(modular_temp)
    sunhours = sum(irradiance)/4

    return [ambient_mean,modular_mean,sunhours]

print(realtime_data([],[],[]))

yield_obtained = None
def get_data():
    global ambient_mean,modular_mean,sunhours,irradiance,modular_temp,ambient_temp,yield_obtained

    ambient_temp = []
    modular_temp = []
    irradiance = []

    data = np.array(realtime_data(ambient_temp,modular_temp,irradiance))

    xg_regressor = gradient_boosting()
    yield_obtained= xg_regressor.predict(data)

    return yield_obtained 

'''schedule.every(1).second.do(get_data)

# Main loop to keep the program running
while True:
    schedule.run_pending()
    time.sleep(1)  # Optional: Adjust sleep time as needed to reduce CPU usage
    if yield_obtained is not None:
        print("Result from function:", yield_obtained)
        yield_obtained = None  # '''




    






