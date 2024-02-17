"""
Module for saving data to the local storage.
"""

import pandas as pd
import time
import os
import re

from .data_requester import DataRequester

class DataCollector:
    """
    Class for saving data to the local storage.
    """
    def __init__(self, api_key : str):
        self.my_requester = DataRequester(api_key)

    def save_data_to_csv(self, data : pd.DataFrame, folder_name : str, filename : str):
        """
        Method for saving data to the local storage.
        """
        current_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_path, '..', '..', 'data')
        file_path = os.path.normpath(file_path)
        os.makedirs(file_path, exist_ok=True)
        file_path = os.path.join(file_path, folder_name)
        os.makedirs(file_path, exist_ok=True)
        file_path = os.path.join(file_path, filename)
        
        with open(file_path, 'w') as file:
            data.to_csv(file, index=False)
    
    def colllect_live_data_n_times_with_k_interval(self, n : int, k : int):
        """
        Method for saving data to the local storage n times with k interval.
        """
        folder_name = 'live_data'
        filename = 'live_locations.csv'
        for i in range(1,n+1):
            response = None
            while not isinstance(response, list):
                response = self.my_requester.get_live_locations('1')
            df = pd.DataFrame(response)
            self.save_data_to_csv(df, folder_name, f'{i}_{filename}')
            time.sleep(k)

    def collect_bus_stops(self):
        """
        Method for saving bus stops to the local storage.
        """
        folder_name = 'bus_stops'
        filename = 'bus_stops.csv'
        response = self.my_requester.get_bus_stops()

        data = pd.DataFrame([{item['key']: item['value'] for item in r['values']} for r in response]).iloc[:, :-1]

        # print(data.head(5))

        
        self.save_data_to_csv(data, folder_name, filename)
    
    def collect_lines_for_bus_stop(self):
        """
        Method for saving bus stops to the local storage.
        """
        url = os.getcwd()
        new_path = os.path.join(url, 'data', 'bus_stops', 'bus_stops.csv')
        new_path = os.path.normpath(new_path)
        df = pd.read_csv(new_path)

        for index, row in df.iterrows():
            bus_stop_id = row['zespol']
            busstopNR = row['slupek']

            folder_name = 'lines_for_stop'
            filename = f'lines_for_{bus_stop_id}_{busstopNR}.csv'
            response = self.my_requester.get_lines_for_stop(bus_stop_id, busstopNR)
            while not isinstance(response, list):
                response = self.my_requester.get_lines_for_stop(bus_stop_id, busstopNR)
            if response:
                values_list = [inner_dict['value'] for outer_dict in response for inner_dict in outer_dict['values']]
                data = pd.DataFrame(values_list)
                self.save_data_to_csv(data, folder_name, filename)

    def collect_time_tables_line_stopId_stopNr(self, line : str, stopId : str, stopNr : str):
        return self.my_requester.get_line_schedule(line, stopId, stopNr)
    
    def collect_time_tables(self):
        url = os.getcwd()
        url = os.path.join(url, 'data', 'lines_for_stop')

        csv_files = [f for f in os.listdir(url) if f.endswith('.csv')]
        for csv_file in csv_files:
            match = re.match(r"lines_for_(\d+)_(\w+)\.csv", csv_file)
            # print("tutaj dochodze")
            if match:
                bus_stop_id = match.group(1)
                busstopNR = match.group(2)
            path = f'{url}/{csv_file}'
            # print(path)
            df = pd.read_csv(path)
            for index, row in df.iterrows():
                line = row['0']
                # print(line)
                folder_name = 'time_tables'
                filename = f'time_table_{line}_{bus_stop_id}_{busstopNR}.csv'
                response = self.collect_time_tables_line_stopId_stopNr(line, bus_stop_id, busstopNR)
                while not isinstance(response, list):
                    response = self.collect_time_tables_line_stopId_stopNr(line, bus_stop_id, busstopNR)
                df_empty = pd.DataFrame(columns=['brygada', 'kierunek', 'trasa', 'czas'])
                for r in response:
                    
                    r = r['values']
                    
                    new_row = {}
                    for entry in r:
                        if entry['key'] in df_empty.columns:
                            new_row[entry['key']] = entry['value']
                    df_empty = pd.concat([df_empty, pd.DataFrame([new_row])], ignore_index=True)
                
                self.save_data_to_csv(df_empty, folder_name, filename)

    def collect_routes(self):
        folder_name = 'routes'
        filename = 'routes.csv'
        response = self.my_requester.get_routes()
        data = pd.DataFrame(response)
        self.save_data_to_csv(data, folder_name, filename)
        # print(data.head(5))

                
                
            


