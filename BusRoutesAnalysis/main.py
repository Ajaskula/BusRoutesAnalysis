import package.analyzer.data_analyzer as da
# import package.analyzer.data_visualizer as dv
import package.data_manager.data_collector as dc
import package.analyzer.data_visualizer as dv
# import package.analyzer.data_cleaner as dc

analyzer = da.DataAnalyzer()
collector = dc.DataCollector('d51d19a7-b4fd-40e8-a4ec-3a1e344a1fcf')

df = analyzer.read_live_data_to_df()
# print(df.iloc[:,-1])

# df = analyzer.remove_buses_not_on_routes(df)
# df = analyzer.remove_buses_outside_warsaw(df)
# print(df.iloc[:,])

# df = analyzer.add_velocity_column(df)
# print(df)
# df = analyzer.remove_unreal_velocity(df)
# print(df)
# conditions = (df.iloc[:, -4:] < 90).all(axis=1)

# Wybieranie wierszy, które spełniają warunki
# df_selected = df.loc[conditions]
# print(df_selected)
# print(analyzer.find_number_of_speeding_buses())
# print(analyzer.find_speeding_lines())
# df2 = analyzer.find_speeding_lines()
# df = analyzer.find_speeding_brigades()
# df3 = analyzer.speed_places()
# visualizer = dv.DataVisualizer()
# visualizer.visualize_speeding_lines(df2, 15)
# visualizer.visualize_speeding_brigades(df)
# visualizer.visualize_speeding_spots(df3)
# visualizer.download_and_save_warsaw_map('warsaw_map.shp')
# visualizer.visualize_speeding_spots(df3)
# collector.collect_bus_stops()
# visualizer.visualize_speeding_spots_with_shapefile(df3)
# visualizer.visualize_speeding_spots(df3)
# analyzer.find_speeding_percentage(100)
# collector.collect_time_tables()
# df = collector.collect_routes()
# print(df)
# collector.colllect_live_data_n_times_with_k_interval(10, 60)
# df = analyzer.analyze_delay_for_bus_stop('4217', '12') #regulska
# analyzer.analyze_speed_in_time(df, 1, 100)
# print(analyzer.find_average_speed(df))
# analyzer.add_velocity_column(df)
df = analyzer.prepare_live_data()
print(analyzer.find_average_speed(df))
# analyzer.analyze_speed_in_time(df, 1, 9)
analyzer.analyze_delay_for_bus_stop('4217', '12')
