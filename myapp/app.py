from pathlib import Path
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from shiny import App, ui, render
from numpy.polynomial import Polynomial

# %% Load data
file_name = "base_de_datos_2013_2016.xlsx"
data_file = Path(__file__).parent / file_name
data = pd.read_excel(data_file)

# UI
app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav_panel("Units Sold & Profit",
            ui.row(
                ui.column(6, ui.output_plot("lineplot1")),
                ui.column(6, ui.output_plot("barplot1"))
            ),
            ui.row(
                ui.column(6, ui.output_plot("lineplot2")),
                ui.column(6, ui.output_plot("barplot2"))
            ),
            ui.input_select("group_by", "Group By", ["Date", "Month Name", "Product", "Segment", "Country"], selected="Date")
        ),

        ui.nav_panel("Units Sold vs Profit",
            ui.row(
                ui.column(6, ui.output_plot("scatterplot")),
                ui.column(6, 
                    ui.h3("Observations"),
                    ui.tags.ul(
                        ui.tags.li("Some entries show sales prices lower than manufacturing costs. Since Dim_Avg_Price has similar information, these entries were not considered anomalous. More data is needed for a conclusive analysis."),
                        ui.h4("Other observations"),
                        ui.tags.li("Sales peak in October and December, with smaller peaks in June, September, February, and April."),
                        ui.tags.li("All products follow similar sales patterns."),
                        ui.tags.li("Paseo leads in sales, nearly doubling the rest; others have uniform sales distribution."),
                        ui.tags.li("The government holds the largest market share by a significant margin."),
                        ui.tags.li("Sales are uniformly distributed across countries."),
                        ui.tags.li("Three linear groups observed in profit vs. units sold for the government, aligning with COGS/Units Sold ratios.")
                    )
                )
            ),
            ui.input_select("segment_select", "Select Segment", data['Segment'].unique().tolist(), selected=data['Segment'].unique()[0])
        )
    )
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

    @output
    @render.plot
    def scatterplot():
        segment = input.segment_select()
        segment_data = data[data['Segment'] == segment]
        
        plt.figure(figsize=(12, 6))
        plt.scatter(segment_data['Units Sold'], segment_data['Profit'], label='Data')
        
        p = Polynomial.fit(segment_data['Units Sold'], segment_data['Profit'], 1)
        trendline = p.linspace(n=100)
        
        plt.plot(trendline[0], trendline[1], color='red', label='Trend Line')
        plt.title(f'Profit vs Units Sold for {segment}')
        plt.xlabel('Units Sold')
        plt.ylabel('Profit')
        plt.grid(True)
        plt.legend()
        return plt.gcf()

# to run the app
app = App(app_ui, server)