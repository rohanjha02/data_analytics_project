# data_analysis_app/views.py
from django.shortcuts import render, HttpResponse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import base64
from io import StringIO
from django.shortcuts import render
from .models import HistoricalData
from django.http import HttpResponse
from django.conf import settings
import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
import matplotlib.pyplot as plt
import seaborn as sns
# Import necessary libraries
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pandas as pd
import pandas as pd
import os  # Import the os module for handling file paths

# Construct the absolute file path dynamically
file_path = os.path.join(os.path.dirname(__file__), 'model.csv')

# Read the CSV file using the constructed file path
df = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Data Analytics\\model.csv")
print(df)


def data_tab(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Data Analytics\\Data_analytics_CIA.csv")
 # Get the first ten rows of the dataset
    df_first_ten = df.head(10)

    # Get information about the columns (data types, non-null counts, null counts)
    columns_info = pd.DataFrame({
        'Column Name': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.notnull().sum(),
        'Null Count': df.isnull().sum()
    })

    # Convert DataFrame to HTML for rendering in template
    table_html = df_first_ten.to_html(classes='table table-hover table-striped-columns table-secondary')

    # Include the columns information in the HTML template
    columns_info_html = f"{columns_info.to_html(classes='table table-hover table-striped-columns table-info', index=False)}"

    return render(request, 'data_tab.html', {'table_html': table_html, 'columns_info_html': columns_info_html})


  
def descriptive_statistics_tab(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Data Analytics\\Data_analytics_CIA.csv")
    
    # Perform descriptive statistics using pandas
    descriptive_stats = df.describe().to_html(classes='table table-hover table-striped-columns table-info')

    return render(request, 'descriptive_statistics_tab.html', {'descriptive_stats': descriptive_stats})




def box_plot(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Data Analytics\\Data_analytics_CIA.csv")

    # Default settings for the plot
    default_category = 'Pclass'
    default_value = 'Fare'

    # Get user-selected options (if any)
    selected_category = request.GET.get('category', default_category)
    selected_value = request.GET.get('value', default_value)

    # Validate selected features
    if selected_category not in df.columns or selected_value not in df.columns:
        error_message = "Invalid features selected for box plot."
        return render(request, 'error_page.html', {'error_message': error_message})

    # Create an interactive box plot using Plotly
    fig = px.box(df, x=selected_category, y=selected_value, title=f'Box Plot: {selected_value} by {selected_category}')

    # Convert the plot to HTML for rendering in the template
    plot_html = fig.to_html(full_html=False)

    # Pass parameters to the template for customization options
    box_cus_options = {
        'categories': df.columns.tolist(),
        'default_category': default_category,
        'default_value': default_value,
        'selected_category': selected_category,
        'selected_value': selected_value,
    }
    return {'plot_html': plot_html, 'box_cus_options': box_cus_options}
    #return render(request, 'box_plot.html', {'plot_html': plot_html, 'customization_options': customization_options})


def exploratory_data_analysis_tab(request):
    # Read the provided dataset
    df = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Data Analytics\\Data_analytics_CIA.csv")

    # Default settings for the plot
    default_year = 1900

    # Get user-selected options (if any)
    selected_year = int(request.GET.get('year', default_year))

    # Filter the data for the selected year
    df_selected_year = df[df['year'] == selected_year]

    # Create a bar chart for population
    fig_population = px.bar(df_selected_year, x='country', y='population', title=f'Population in {selected_year}')

    # Create a bar chart for CO2 emissions
    fig_co2 = px.bar(df_selected_year, x='country', y='co2', title=f'CO2 Emissions in {selected_year}')

    # Convert the plots to HTML for rendering in the template
    plot_html_population = fig_population.to_html(full_html=False)
    plot_html_co2 = fig_co2.to_html(full_html=False)

    # Pass parameters to the template for customization options
    customization_options = {
        'years': df['year'].unique().tolist(),
        'default_year': default_year,
        'selected_year': selected_year,
    }

    return render(request, 'exploratory_data_analysis_tab.html', {
        'plot_html_population': plot_html_population,
        'plot_html_co2': plot_html_co2,
        'customization_options': customization_options,
    })



def predict(request):
    if request.method == 'POST':
        years_into_future = int(request.POST.get('years_into_future', 0))  # Ensure a default value is provided

        try:
            # Get the latest entry from the database
            latest_entry = HistoricalData.objects.latest('year')
        except HistoricalData.DoesNotExist:
            # Handle the case where no data is available
            latest_entry = None
            print("No historical data available.")

        if latest_entry:
            # Calculate average growth rate for population
            average_population_growth_rate = ((latest_entry.population / HistoricalData.objects.first().population) ** (1 / HistoricalData.objects.count())) - 1

            # Predict future population
            predicted_population = latest_entry.population * (1 + average_population_growth_rate) ** years_into_future

            # Calculate average growth rate for CO2
            average_co2_growth_rate = ((latest_entry.co2 / HistoricalData.objects.first().co2) ** (1 / HistoricalData.objects.count())) - 1

            # Predict future CO2 levels
            predicted_co2 = latest_entry.co2 * (1 + average_co2_growth_rate) ** years_into_future

            print(f"Form data: {request.POST}")
            print(f"Predicted Population: {predicted_population}, Predicted CO2: {predicted_co2}")

            return render(request, 'predict.html', {'predicted_population': predicted_population, 'predicted_co2': predicted_co2, 'years_into_future': years_into_future})
        else:
            # Handle the case where no data is available
            return render(request, 'predict.html', {'error_message': 'No historical data available.'})

    return render(request, 'predict.html')

def profile_view(request):
        return render(request, 'profile_view.html') 


def report(request):
    # Read your CSV file
    df = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Data Analytics\\Data_analytics_CIA.csv")

    # Perform any data analysis or modifications here (if needed)

    # Create 2 different dynamic visualizations
    plt.figure(figsize=(12, 6))

    # Visualization 1: Bar plot
    plt.subplot(1, 2, 1)
    sns.countplot(x='year', data=df)
    plt.title('Bar Plot')

    # Visualization 2: Scatter plot
    plt.subplot(1, 2, 2)
    sns.scatterplot(x='year', y='population', data=df)
    plt.title('Scatter Plot')

    # Display the plot in a new pop-up window
    plt.show()

    return render(request, 'report.html')






def export_to_csv(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Data Analytics\\Data_analytics_CIA.csv")

    # Generate CSV file
    csv_file = df.to_csv(index=False)

    # Create HTTP response with CSV file
    response = HttpResponse(csv_file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="titanic_data.csv"'
    
    return response


def export_to_excel(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\asus\\OneDrive\\Desktop\\Data Analytics\\Data_analytics_CIA.csv")

    # Generate Excel file
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    excel_file.seek(0)

    # Create HTTP response with Excel file
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="titanic_data.xlsx"'

    return response

