"""
Module for prepering data for further analysis.
And for analyzing data.
"""
import pandas as pd
import os
import geopy.distance as geodisc
import numpy as np
from datetime import datetime
import warnings

from .data_visualizer import DataVisualizer
from .data_cleaner import DataCleaner

class DataAnalyzer:
    """
    A class for analyzing data.
    """
    def __init__(self):
        self.visualizer = DataVisualizer()
        self.cleaner = DataCleaner()

    def calculate_velocity(self, lon1, lat1, lon2, lat2, start_time, end_time):
        """
        Method for calculating the velocity.
        """
        p1 = (lat1, lon1)
        p2 = (lat2, lon2)
        distance = geodisc.distance(p1, p2).meters
        start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        time_diff = (end_time - start_time).total_seconds()
        if time_diff == 0:
            return 0
        return round(abs((distance/1000.0) / (time_diff/3600.0)), 2)
    
    def add_velocity_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Method for adding velocity column.
        """
        cnt = 0
        for i in range(9, len(df.columns), 6):
            cnt += 1
            new_list = []
            for j in range (len(df)):
                new_list.append(self.calculate_velocity(df.iat[j, i-8], df.iat[j, i-5], df.iat[j, i-2], df.iat[j, i+1], df.iat[j, i-6], df.iat[j, i]))
            df[f'{cnt}_Velocity'] = new_list
        return df
                
    def find_number_of_speeding_buses(self) -> int:
        df = self.prepare_live_data()
        full_string = str(df.columns[-1])
        numeric_part = int(full_string.split('_')[0])
        conditions = (df.iloc[:, -numeric_part:] < 50).all(axis=1)
        df_selected = df.loc[conditions]
        # print(df_selected)
        return len(df) - len(df_selected)


    def find_speeding_lines(self) -> dict:
        df = self.prepare_live_data()
        full_string = str(df.columns[-1])
        numeric_part = int(full_string.split('_')[0])
        conditions = (df.iloc[:, -numeric_part:] > 50).any(axis=1)
        df_selected = df.loc[conditions]
        # print(len(df_selected))
        speeding_lines = {}
        for value in df_selected.iloc[:, 0]:
            # print(value)
            if value in speeding_lines:
                speeding_lines[value] += 1
                # print(value)
            else:
                # print(value)
                speeding_lines[value] = 1
        return speeding_lines
    
    def find_speeding_brigades(self) -> dict:
        df = self.prepare_live_data()
        full_string = str(df.columns[-1])
        numeric_part = int(full_string.split('_')[0])
        conditions = (df.iloc[:, -numeric_part:] > 50).any(axis=1)
        df_selected = df.loc[conditions]
        # print(len(df_selected))
        speeding_lines = {}
        for value in df_selected.iloc[:, 5]:
            # print(value)
            if value in speeding_lines:
                speeding_lines[value] += 1
                # print(value)
            else:
                # print(value)
                speeding_lines[value] = 1
        return speeding_lines

    def speed_places(self) -> pd.DataFrame:
        df = self.prepare_live_data()
        full_string = str(df.columns[-1])
        numeric_part = int(full_string.split('_')[0])
        conditions = (df.iloc[:, -numeric_part:] > 50).any(axis=1)
        df_selected = df.loc[conditions]
        speeding_places = {}
        cnt = 0
        for i in range(df_selected.shape[1] - 1, df_selected.shape[1]-1-numeric_part,-1):
            for j in range(0, len(df_selected)):

                if df_selected.iat[j, i] > 50:
                    lon = (df_selected.iat[j, cnt + 1] + df_selected.iat[j, cnt + 7])/2.0
                    lat = (df_selected.iat[j, cnt + 4] + df_selected.iat[j, cnt + 10])/2.0
                    point = (lon, lat)
               
                    speeding_places[point] = df_selected.iat[j, i]
            cnt+=6

        return speeding_places

    def prepare_live_data(self) -> pd.DataFrame:
        df = self.read_live_data_to_df()
        df = self.remove_buses_outside_warsaw(df)
        df = self.remove_buses_not_on_routes(df)
        df = self.add_velocity_column(df)
        df = self.remove_unreal_velocity(df)

        return df
    
    def remove_unreal_velocity(self,df: pd.DataFrame) -> pd.DataFrame:
        
        full_string = str(df.columns[-1])
        numeric_part = int(full_string.split('_')[0])
        conditions = (df.iloc[:, -numeric_part:] < 90).all(axis=1)

        df_selected = df.loc[conditions]
        return df_selected

    def remove_buses_outside_warsaw(self, df: pd.DataFrame) -> pd.DataFrame:
        east_bound = 20.0
        west_bound = 21.5
        north_bound = 52.5
        south_bound = 51.8

        for i in range(df.shape[1]):
            if i % 6 == 1:  # Dla kolumn o indeksach 1 + 6k
                condition1 = (df.iloc[:, i] >= east_bound) & (df.iloc[:, i] <= west_bound)
                df = df[condition1]
            elif i % 6 == 4:  # Dla kolumn o indeksach 4 + 6k
                condition2 = (df.iloc[:, i] >= south_bound) & (df.iloc[:, i] <= north_bound)
                df = df[condition2]
        return df

    def remove_buses_not_on_routes(self, df: pd.DataFrame) -> pd.DataFrame:
        condition = (df.iloc[:, 1] != df.iloc[:, -5]) | (df.iloc[:, 4] != df.iloc[:, -2])
        df = df[condition]
        return df
    
    def read_live_data_to_df(self) -> pd.DataFrame:
        """
        Method for reading data from csv to dataframe.
        """
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'data')
        path = os.path.normpath(path)
        path = os.path.join(path, 'live_data')
        df_list = []
        # print(path)
        for file in os.listdir(path):
            df = pd.read_csv(os.path.join(path, file))
            df_list.append(df)
        df = pd.concat(df_list, axis=1)
        return df


    def remove_outside_time_range(self, df: pd.DataFrame, start_time: str, end_time: str) -> pd.DataFrame:
        """
        Method for removing data outside time range.
        """
        for i in range(3, df.shape[1], 6):
            df.iloc[:, i] = pd.to_datetime(df.iloc[:, i], errors='coerce')

        df = df[df.apply(lambda row: row[3::5].between('2024-02-15 00:00:00', '2024-02-15 11:09:47').all(), axis=1)]
        return df

    def is_between(self, value, lower_bound, upper_bound):
        return lower_bound < value <= upper_bound

    def prepare_rectangle(self, n):
        x1 = 20.5
        x2 = 21.5
        x3 = 21.5
        x4 = 20.5
        y1 = 51.8
        y2 = 51.8
        y3 = 52.5
        y4 = 52.5

        if n <= 1:
            print("Liczba n musi być większa niż 1.")
            return

        side1 = x2-x1
        side2 = y3-y2

        width = side1
        height = side2

        small_width = width / n
        small_height = height / n

        data = []
        for i in range(n):
            for j in range(n):
                x_start = x1 + i * small_width
                y_start = y1 + j * small_height
                x_end = x_start + small_width
                y_end = y_start + small_height

                data.append([x_start, y_start, x_end, y_start, x_end, y_end, x_start, y_end])

        df = pd.DataFrame(data, columns=['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4'])

        return df
    


    def find_speeding_percentage(self, n : int) -> None:

        rectangle = self.prepare_rectangle(n)
        occurrences = []
        speeding_ = []
        points = []
        live_data = self.read_live_data_to_df()
        live_data = self.remove_buses_outside_warsaw(live_data)
        live_data = self.remove_buses_not_on_routes(live_data)
        for i in range(9, len(live_data.columns), 6):
            for j in range (len(live_data)):
                points.append((live_data.iat[j, i-8], live_data.iat[j, i-5], self.calculate_velocity(live_data.iat[j, i-8], live_data.iat[j, i-5], live_data.iat[j, i-2], live_data.iat[j, i+1], live_data.iat[j, i-6], live_data.iat[j, i])))

        for index, row in rectangle.iterrows():
            count = 0
            speeding = 0
            for point in points:
                x, y, z = point
                if self.is_between(x,row['x1'],row['x3']) and self.is_between(y,row['y1'],row['y3']):
                    count += 1
                    if z > 50:
                        speeding += 1
            occurrences.append(count)
            speeding_.append(speeding)

        rectangle['occurrence'] = occurrences
        rectangle['speeding'] = speeding_
        print(rectangle['speeding'].max())
        rectangle['percent'] = (rectangle['speeding'] / rectangle['occurrence']).replace([np.inf, -np.inf], 0) * 100
        rectangle['percent'] = rectangle['percent'].fillna(0) 
        self.visualizer.draw_squares(rectangle)

    def find_bus_stop(self, bustopId : str, busstopNR : str) -> pd.DataFrame:
        """
        Method for finding bus stop.
        """
        url_bus_stop = os.getcwd()
        url_bus_stop = os.path.join(url_bus_stop, 'data', 'bus_stops', 'bus_stops.csv')
        df = pd.read_csv(url_bus_stop)
        selected_row = df.loc[df['zespol'] == (bustopId)]
        selected_row = selected_row.loc[selected_row['slupek'] == int(busstopNR)]
        return selected_row

    def find_lines_for_stop(self, bustopId : str, busstopNR : str) -> pd.DataFrame:
        """
        Method for finding lines for bus stop.
        """
        url = os.getcwd()
        new_path = os.path.join(url, 'data', 'lines_for_stop', f'lines_for_{bustopId}_{busstopNR}.csv')
        new_path = os.path.normpath(new_path)
        # print(new_path)
        df = pd.read_csv(new_path)
        return df

    def collect_time_table_line_stopId_stopNr(self, line : str, stopId : str, stopNr : str) -> pd.DataFrame:
        """
        Method for collecting time table for line and bus stop.
        """
        url = os.getcwd()
        new_path = os.path.join(url, 'data', 'time_tables', f'time_table_{line}_{stopId}_{stopNr}.csv')
        new_path = os.path.normpath(new_path)
        df = pd.read_csv(new_path)
        return df
    
    def time_to_seconds2(self, time_str):
        try:
            date_part, time_part = time_str.split(' ')
            hours, minutes, seconds = map(int, time_part.split(':'))
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds
        except ValueError:
            print(f'Nieprawidłowy format czasu: {time_str}')
            return None
    def time_to_seconds1(self, time_str):
        try:
            hours, minutes, seconds = map(int, time_str.split(':'))
            total_seconds = hours * 3600 + minutes * 60 + seconds
            return total_seconds
        except ValueError:
            print(f'Nieprawidłowy format czasu: {time_str}')
            return None
    def calculate_time_diff(self, time1, time2):
        """
        Method for calculating time difference.
        """
        time1 = datetime.strptime(time1, '%H:%M:%S').time()
        time2 = datetime.strptime(time2, '%H:%M:%S').time()
        time_diff = (time1 - time2).total_seconds()
        return time_diff
    def analyze_delay_for_bus_stop(self, bustopId : str, busstopNR : str):
        with warnings.catch_warnings():
        # Ignoruj future warningi wewnątrz tego bloku
            warnings.simplefilter("ignore", category=FutureWarning)
            bus_stop_df = self.find_bus_stop(bustopId, busstopNR)
            lines_for_stop = self.find_lines_for_stop(bustopId, busstopNR)
            lines_for_stop.rename(columns={'0': 'line'}, inplace=True)
            live_data = self.prepare_live_data()
            lines_for_stop.iloc[:, 0] = lines_for_stop.iloc[:, 0].astype(str)
            selected_live_data = live_data[live_data.iloc[:, 0].isin(lines_for_stop['line'].values)]
            lines_for_stop['delayed'] = 0
            lines_for_stop['on_time'] = 0
            szer_geo = bus_stop_df.iloc[0]['szer_geo']
            dlug_geo = bus_stop_df.iloc[0]['dlug_geo']
            my_time_tables = {}
            for index, row in lines_for_stop.iterrows():
                line = row['line']
                time_table = self.collect_time_table_line_stopId_stopNr(line, bustopId, busstopNR)
                time_table['brygada'] = time_table['brygada'].astype(str)
                my_time_tables[line] = time_table
            for row in selected_live_data.iterrows():
                
                line = row[1][0]
                brigade = row[1][5]

                curr_timetable = my_time_tables[str(row[1][0])] 
                times_to_check = curr_timetable[curr_timetable['brygada'] == brigade]
                times_to_check = times_to_check.iloc[:, 3].values
                times_to_check = [time for time in times_to_check if time <= '23:59:59']
                copy_row = row[1].copy()
                for time in times_to_check:
                    for i in range(3, len(selected_live_data.columns), 6):
                        if type(copy_row[i]) is float:
                            break
                        time2 = datetime.strptime(time, '%H:%M:%S').time()
                        sec1 = self.time_to_seconds1(time)
                        sec2 = self.time_to_seconds2(copy_row[i])

                        diff = abs(sec1 - sec2)

                        if diff < 200:
                            distance = geodisc.distance((copy_row[i+1], copy_row[i-2]), (szer_geo, dlug_geo)).meters
                            if distance > 1600:
                                lines_for_stop.loc[lines_for_stop['line'] == line, 'delayed'] += 1
                            else:
                                lines_for_stop.loc[lines_for_stop['line'] == line, 'on_time'] += 1
            self.visualizer.plot_delay_ratio(lines_for_stop)
                    
    def find_maximum_speed(self, df):
        start_column_index = df.columns.get_loc('1_Velocity')
        max_velocity_in_row = df.iloc[:, start_column_index:].max(axis=1)
        max_df = pd.DataFrame({'maximum': max_velocity_in_row})
        return max_df

    def find_average_speed(self, df):
        start_column_index = df.columns.get_loc('1_Velocity')
        # print(df)
        average_velocity_in_row = df.iloc[:, start_column_index:].mean(axis=1)
        average_df = pd.DataFrame({'average': average_velocity_in_row})
        return average_df
        

    def analyze_speed_in_time(self, df, start_idx, end_idx):
        self.visualizer.plot_speed_in_time(df, start_idx, end_idx)



        

        