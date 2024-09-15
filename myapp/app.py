from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from shiny import App, ui, render

# %% Load data
# data_path = "Data"
file_name = "base_de_datos_2013_2016.xlsx"

data_file = Path(__file__).parent / file_name
data = pd.read_excel(data_file)

# UI
app_ui = ui.page_fluid(
    ui.row(
        ui.column(6, ui.output_plot("lineplot1")),
        ui.column(6, ui.output_plot("barplot1"))
    ),
    ui.row(
        ui.column(6, ui.output_plot("lineplot2")),
        ui.column(6, ui.output_plot("barplot2"))
    ),
    ui.input_select("group_by", "Group By", ["Date", "Month Name", "Product", "Segment", "Country"], selected="Date")
)

# Server
def server(input, output, session):
    @output
    @render.plot
    def lineplot1():
        group_by = input.group_by()
        if group_by == "Month Name":
            return plt.figure()  # Return an empty figure if Month Name is selected
        elif group_by == "Date":
            units_sold_by_date = data.groupby('Date')['Units Sold'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=units_sold_by_date, x='Date', y='Units Sold')
            plt.title('Units Sold by Date')
            plt.xlabel('Date')
            plt.ylabel('Units Sold')
            plt.xticks(rotation=45)
            plt.grid(True)
            return plt.gcf()
        else:
            plt.figure(figsize=(12, 6))
            for group in data[group_by].unique():
                units_sold_by_date = data.query(f"{group_by} == '{group}'").groupby('Date')['Units Sold'].sum().reset_index()
                sns.lineplot(data=units_sold_by_date, x='Date', y='Units Sold', label=group)
            plt.title(f'Units Sold by Date and {group_by}')
            plt.xlabel('Date')
            plt.ylabel('Units Sold')
            plt.xticks(rotation=45)
            plt.legend(title=group_by)
            plt.grid(True)
            return plt.gcf()

    @output
    @render.plot
    def barplot1():
        group_by = input.group_by()
        if group_by == "Date":
            units_sold_by_group = data.groupby("Date")['Units Sold'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            sns.barplot(data=units_sold_by_group, x=group_by, y='Units Sold')
            plt.title(f'Units Sold by {group_by}')
            plt.xlabel(group_by)
            plt.ylabel('Units Sold')
            plt.xticks(rotation=45)
            plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))  # Reduce the number of ticks
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Reduce grid size
            return plt.gcf()
        else:
            units_sold_by_group = data.groupby(group_by)['Units Sold'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            sns.barplot(data=units_sold_by_group, x=group_by, y='Units Sold')
            plt.title(f'Units Sold by {group_by}')
            plt.xlabel(group_by)
            plt.ylabel('Units Sold')
            plt.xticks(rotation=45)
            plt.grid(True)
            return plt.gcf()

    @output
    @render.plot
    def lineplot2():
        group_by = input.group_by()
        if group_by == "Month Name":
            return plt.figure()  # Return an empty figure if Month Name is selected
        elif group_by == "Date":
            profit_by_date = data.groupby('Date')['Profit'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            sns.lineplot(data=profit_by_date, x='Date', y='Profit')
            plt.title('Profit by Date')
            plt.xlabel('Date')
            plt.ylabel('Profit')
            plt.xticks(rotation=45)
            plt.grid(True)
            return plt.gcf()
        else:
            plt.figure(figsize=(12, 6))
            for group in data[group_by].unique():
                profit_by_date = data.query(f"{group_by} == '{group}'").groupby('Date')['Profit'].sum().reset_index()
                sns.lineplot(data=profit_by_date, x='Date', y='Profit', label=group)
            plt.title(f'Profit by Date and {group_by}')
            plt.xlabel('Date')
            plt.ylabel('Profit')
            plt.legend(title=group_by)
            plt.xticks(rotation=45)
            plt.grid(True)
            return plt.gcf()

    @output
    @render.plot
    def barplot2():
        group_by = input.group_by()
        if group_by == "Date":
            profit_by_group = data.groupby("Date")['Profit'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            sns.barplot(data=profit_by_group, x=group_by, y='Profit')
            plt.title(f'Profit by {group_by}')
            plt.xlabel(group_by)
            plt.ylabel('Profit')
            plt.xticks(rotation=45)
            plt.gca().xaxis.set_major_locator(MaxNLocator(nbins=10))  # Reduce the number of ticks
            plt.grid(True, which='both', linestyle='--', linewidth=0.5)  # Reduce grid size
            return plt.gcf()
        else:
            profit_by_group = data.groupby(group_by)['Profit'].sum().reset_index()
            plt.figure(figsize=(12, 6))
            sns.barplot(data=profit_by_group, x=group_by, y='Profit')
            plt.title(f'Profit by {group_by}')
            plt.xlabel(group_by)
            plt.ylabel('Profit')
            plt.xticks(rotation=45)
            plt.grid(True)
            return plt.gcf()

# to run the app
app = App(app_ui, server)