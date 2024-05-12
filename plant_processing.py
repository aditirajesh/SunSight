import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import numpy as np
class Source:

    def __init__(self,filename):
        self.filename = filename
        self.dataset = pd.read_csv(filename)
        self.df = pd.DataFrame(columns=['DATE','AMBIENT_TEMP','MODULE_TEMP','SUN_HOURS','YIELD'])

    def trim_dataset(self):
        self.dataset[['DATE', 'TIME']] = self.dataset.DATE_TIME.str.split(" ", expand = True)
        self.dataset.drop(["DATE_TIME","DC_POWER","AC_POWER"],axis=1,inplace=True)
        self.dataset = self.dataset[['DATE','TIME','AMBIENT_TEMPERATURE','MODULE_TEMPERATURE','IRRADIATION','DAILY_YIELD']]

        return self.dataset
    
    def avg_dataset(self):
        self.trim_dataset()
        for date in self.dataset['DATE'].unique():
            ambient_temperatures = list(self.dataset.loc[self.dataset['DATE'] == date, 'AMBIENT_TEMPERATURE'])
            module_temperatures = self.dataset.loc[self.dataset['DATE'] == date, 'MODULE_TEMPERATURE']
            irradiations = self.dataset.loc[self.dataset['DATE'] == date, 'IRRADIATION']

            ambient_temperatures = sum(ambient_temperatures)/len(ambient_temperatures)
            module_temperatures = sum(module_temperatures)/len(module_temperatures)
            irradiations = sum(irradiations)/4

            daily_yield = np.array(list(self.dataset.loc[(self.dataset['DATE'] == date),'DAILY_YIELD']))
            daily_yield = np.nanmax(daily_yield)
            self.df = self.df._append({'DATE':date,
                            'AMBIENT_TEMP':ambient_temperatures,
                            'MODULE_TEMP':module_temperatures,
                            'SUN_HOURS':irradiations,
                            'YIELD':daily_yield},ignore_index=True)
            
        return self.df

    def save_to_csv(self):
        df = self.avg_dataset()
        df.to_csv(self.filename,index=False)
        return 'done'
    
if __name__ == "__main__":
    filename = "/Users/aditirajesh/Desktop/program_files/python/python_6sem/DATA_PLANTS/plant2/data22_2.csv"
    source = Source(filename)
    print(source.save_to_csv())
    


    
