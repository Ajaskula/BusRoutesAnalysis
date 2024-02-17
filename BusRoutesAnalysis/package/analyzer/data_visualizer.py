"""
Module for visualizing data.
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg

class DataVisualizer:
    """
    Class for visualizing data.
    """
    def __init__(self):
        pass

    def visualize_speeding_lines(self, bus_line_dict: dict, keys_per_plot: int = 10):
        """
        Method for visualizing speeding lines.
        """
        keys = list(bus_line_dict.keys())
        values = list(bus_line_dict.values())

        keys_per_plot = min(keys_per_plot, len(keys))

        for i in range(0, len(keys), keys_per_plot):
            current_keys = keys[i:i + keys_per_plot]
            current_values = values[i:i + keys_per_plot]

            # Utwórz wykres dla aktualnych kluczy i wartości
            plt.bar(current_keys, current_values, color='orange')
            plt.xlabel('Numer linii autobusowej')
            plt.ylabel('Liczba autobusów')
            plt.title(f'Liczba autobusów dla poszczególnych linii ({i+1}-{i+len(current_keys)})')
            plt.show()
    
    # def visualize_speeding_brigades(self, bus_line_dict: dict):
    #     """
    #     Method for visualizing speeding brigades.
    #     """
    #     plt.bar(bus_line_dict.keys(),bus_line_dict.values(),  color='green')
    #     plt.ylabel('Liczba autobusów dla poszczególnych brygad')
    #     plt.xlabel('Numer brygady autobusowej')
    #     plt.title('Liczba autobusów dla poszczególnych brygad, które przekroczyły prędkość')
    #     plt.show()

    def visualize_speeding_brigades(self, bus_line_dict: dict):
        """
        Method for visualizing speeding brigades.
        """
        brigades = list(bus_line_dict.keys())
        buses = list(bus_line_dict.values())
        
        num_brigades = len(brigades)
        num_plots = (num_brigades // 7) + (num_brigades % 7 > 0)  # Calculate the number of plots needed

        for i in range(num_plots):
            start_index = i * 7
            end_index = min((i + 1) * 7, num_brigades)

            plt.bar(brigades[start_index:end_index], buses[start_index:end_index], color='green')
            plt.ylabel('Liczba autobusów dla poszczególnych brygad')
            plt.xlabel('Numer brygady autobusowej')
            plt.title(f'Liczba autobusów dla brygad {start_index + 1} - {end_index}, które przekroczyły prędkość')
            plt.show()
        
    def visualize_speed_places(self, df: dict):
        """
        Method for visualizing speeding places.
        """
        print(df)
        return df

    def visualize_speeding_spots(self, data_dict: dict):
        """
        Function for visualizing density using scatter plot with a background image.

        Parameters:
        - data_dict: A dictionary where keys are tuples (float, float) and values are counts.
        """
        keys, counts = zip(*data_dict.items())

        x_values, y_values = zip(*keys)

        normalized_counts = np.array(counts) / max(counts)
        background = mpimg.imread('/home/ajask/Desktop/Python1/BusRoutesAnalysis/package/analyzer/1.png')

        plt.scatter(x_values, y_values, c=normalized_counts, s=normalized_counts * 100, alpha=0.7, cmap='viridis')

        plt.imshow(background, extent=[min(x_values), max(x_values), min(y_values), max(y_values)], aspect='auto', alpha=0.5)

        plt.xlabel('Długość geograficzna')
        plt.ylabel('Szerokość geograficzna')
        plt.title('Wykres punktowy z kolorami i rozmiarami zależnymi od krotności')

        cbar = plt.colorbar()
        cbar.set_label('Krotność')

        plt.show()
    
    def draw_squares(self, df):
        """
        Method for drawing squares on a plot.
        """
        fig, ax = plt.subplots()
        # for val in df['percent']:
        #     # print(val)
        for i in range(len(df)):
            plt.fill([df.iloc[i]['x1'], df.iloc[i]['x2'], df.iloc[i]['x3'], df.iloc[i]['x4'], df.iloc[i]['x1']],
                    [df.iloc[i]['y1'], df.iloc[i]['y2'], df.iloc[i]['y3'], df.iloc[i]['y4'], df.iloc[i]['y1']],
                    color=plt.cm.viridis(df.iloc[i]['percent']/df['percent'].max()))

        plt.axis('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Heat map of speeding places')
        norm = plt.Normalize(vmin=0.0, vmax=100.0)
        sm = plt.cm.ScalarMappable(cmap=plt.cm.viridis, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax)
        cbar.set_label('Speeding_percentage')

        plt.show()

    def plot_delay_ratio(self, df):
        """
        Method for plotting the ratio of delayed and on-time arrivals for each bus line.
        """
        grouped_df = df.groupby('line').agg({'delayed': 'sum', 'on_time': 'sum'})

        plt.figure(figsize=(12, 6))
        bar_width = 0.35
        index = range(len(grouped_df.index))

        plt.bar(index, grouped_df['delayed'], width=bar_width, label='Opóźnione', color='red')
        plt.bar([i + bar_width for i in index], grouped_df['on_time'], width=bar_width, label='Punktualne', color='green')

        plt.title('Liczba opóźnień i liczba punktualnych przyjazdów dla każdej linii')
        plt.xlabel('Linia')
        plt.ylabel('Liczba zdarzeń')
        plt.xticks([i + bar_width/2 for i in index], grouped_df.index)  # Przesunięcie etykiet o połowę szerokości słupka
        plt.legend()
        plt.show()

    def plot_speed_in_time(self, df, start_row, end_row):
        """
        Method for plotting speed in time.
        """
        selected_df = df.iloc[start_row:end_row+1, :]

        velocity_columns = [col for col in selected_df.columns if 'Velocity' in col]

        plt.figure(figsize=(12, 6))

        for index, row in selected_df.iterrows():
            plt.plot(velocity_columns, row[velocity_columns], label=f'Autobus {index}')

        plt.xticks(range(len(selected_df)), [f'{index}' for index in selected_df.index])

        plt.xlabel('Autobusy')
        plt.ylabel('Wartości Prędkości')
        plt.title('Zmiany Prędkości dla Wybranych Wierszy')
        plt.legend()
        plt.grid(True)
        plt.show()
        

