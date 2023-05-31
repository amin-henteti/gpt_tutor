import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime

ONLINE_CSV = 'https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv'
def main():
    st.title("Object Examples")

    # Define the button options and their corresponding functions
    button_options = {
        "Standard": display_standard_example,
        "Integer": display_integer_example,
        "DataFrame": display_dataframe_example,
        "Plot": display_plot_example
    }

    st.subheader('selectbox')
    # Create the buttons
    buttons = st.selectbox("Select an object example:",
                           list(button_options.keys()))
    button_clicked = st.button("Display")

    # Handle button click
    if button_clicked:
        print("button display is clicked")
        if buttons in button_options:
            print(f"buttons {buttons} clicked")
            display_function = button_options[buttons]
            display_function()
    else:
        print("button display is Not clicked")

    st.subheader('Slider')
    # Create a slider for selecting a value within a range
    selected_value = st.slider("Select a value", 0, 100, 50)
    st.write(f"Selected value: {selected_value}")

    # second slider (use 0.0 float to infer that the slider should use fractional steps)
    another_selected_value = st.slider("select decimal number",
                                       min_value=0.0,
                                       max_value=10.0,
                                       value=(2.0, 7.5),
                                       step=0.7)
    st.write(f"decimal value is set to {another_selected_value}")

    st.subheader('select_slider')
    # Create a select slider for color wavelength
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    selected_color = st.select_slider('Select a color',
                                      options=colors,
                                      value=(colors[0], colors[-1]),
                                      format_func=lambda x: x)
    st.write(f'You selected {selected_color} color')

    st.subheader('radio')
    # Create a select slider for color wavelength
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    selected_color = st.radio('Select a color', options=colors)
    st.write(f'from the radio options You selected **{selected_color}** color')

    st.subheader("line_chart")
    df = create_dataframe()
    st.write("Here's a DataFrame with funny data:")
    st.write(df)
    # display_line_chart(df)
    st.line_chart(df)
    st.write("""
    The line chart above represents my daily journey:\n
    In the morning, my productivity is just average. Not a morning person!\n
    In the afternoon, it takes a nosedive. Lunchtime laziness!\n
    But in the evening, I bounce back, reaching peak productivity!\n
    And here's the secret: my happiness is fueled by caffeine.\n
    As the day progresses, my caffeine level drops, affecting my happiness.\n
    Clearly, I need more coffee to keep my happiness levels high!
    """)

    fruits = ['Apple', 'Banana', 'Orange', 'Mango']

    selected_fruit = st.selectbox(label='Select your favorite fruit',
                                  options=fruits,
                                  index=1,
                                  help='Choose a fruit from the dropdown menu')
    st.write(f'You selected: {selected_fruit}')

    st.subheader("multiselect")

    cities = ['Paris', 'New York', 'Tokyo', 'London', 'Sydney', 'Rome']

    selected_cities = st.multiselect(
        'Select your dream travel destinations',
        cities,
        default=['Paris', 'Tokyo'],
        help='Choose multiple cities you would love to visit')

    st.write('You selected the following cities:')
    for city in selected_cities:
        st.write(city)

    st.subheader("checkbox")
    options = {
        'Feature 1': "include color",
        'Feature 2': "parametrize length",
        'Feature 3': "calculate worth",
    }

    for key, value in options.items():
        options[key] = st.checkbox(label=key, value=False, help=value)

    for key, value in options.items():
        if value:
            st.write(f'{key} is enabled!')

    st.header('st.latex')

    st.latex(r'''
        a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
        \sum_{k=0}^{n-1} ar^k =
        a \left(\frac{1-r^{n}}{1-r}\right)
        ''')
    st.latex(
        r"\alpha^2 + \beta^2 = \gamma^2")  # Display the Pythagorean theorem


def display_standard_example():
    st.write("This is a standard example object: a string.")


def display_integer_example():
    number = 42
    st.write(f"This is an integer example object: {number}.")


def display_dataframe_example():
    data = {'Name': ['Alice', 'Bob', 'Charlie'], 'Age': [25, 30, 35]}
    df = pd.DataFrame(data)
    st.write("This is a DataFrame example object:")
    st.write(df)


def display_plot_example():
    df = pd.DataFrame(np.random.randn(200, 4),
                      columns=['x', 'y', 'size', 'worth'])
    c = alt.Chart(df).mark_circle().encode(x='x',
                                           y='y',
                                           size='size',
                                           color='worth',
                                           tooltip=['x', 'y', 'size'])
    st.write(c)
    # Create an Altair scatter plot
    chart = alt.Chart(df).mark_point().encode(x='x',
                                              y='y',
                                              color='worth',
                                              tooltip=['size']).properties(
                                                  width=350, height=350)
    # Display the Altair chart using st.altair_chart
    st.altair_chart(chart)
    # advanced concepts
    # Create a slider using Streamlit
    slider_value = st.slider("Gem Worth Threshold",
                             min_value=0,
                             max_value=100,
                             value=50)

    # Update the chart based on the slider value
    filtered_chart = chart.transform_filter(alt.datum.worth >= slider_value)

    # Display the filtered chart with the slider
    st.altair_chart(filtered_chart)


def create_dataframe():
    data = {
        'Time': ['Morning', 'Afternoon', 'Evening'],
        'Productivity': [5, 2, 9],
        'Happiness': [8, 9, 3],
        'Caffeine Level': [10, 8, 2]
    }
    df = pd.DataFrame(data)
    df.set_index('Time', inplace=True)
    return df


if __name__ == "__main__":
    # Custom theme configuration
    custom_theme = {
        "primaryColor": "#ff0000",  # Set the primary color to red
        "backgroundColor": "#f0f0f0",  # Set the background color to light gray
        "font": "sans serif"  # Set the font to sans serif
    }
    # this dict content should be saved in a file .streamlit/config.toml

    # Apply the custom theme
    st.set_page_config(page_title="Custom Theme Example",
                       page_icon="🎨",
                       layout="wide")

    main()

    import os, time
    with st.expander('About this app'):
        st.write('You can now display the progress of your calculations in a Streamlit app with the `st.progress` command.')

    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)

    st.balloons()

    st.subheader("secrets")
    # Everything is accessible via the st.secrets dict:
    st.write("admin username:", st.secrets["admin_username"])
    st.write("admin password:", st.secrets["admin_password"])
    st.write("My db secrets:", st.secrets["database"]["list_data"])

    # And the root-level secrets are also accessible as environment variables:

    import os, time
    st.write("Has environment variables been set:",
             os.environ["admin_username"] == st.secrets["admin_username"], "got same as in the streamlit secrets")

    st.subheader('Input CSV')
    uploaded_file = st.file_uploader(
        label="Upload a CSV file",
        type=("csv", "txt"),
        accept_multiple_files=False,
        key="csv-uploader",
        help="Only CSV and TXT file types are allowed."
    )
    if uploaded_file is not None:
        st.write(str(uploaded_file))
        file_bytes = uploaded_file.read()
        # Check if the file size exceeds the maximum allowed size
        # Set the maximum upload size to 1 KB (1024 bytes)
        max_size_bytes = 1024
        if len(file_bytes) > max_size_bytes:
            st.error("File size exceeds the maximum allowed size tiny (1 KB). Please upload a smaller file.")
        else:
            # Process the uploaded file
            st.success(f"File uploaded successfully! len={len(file_bytes)}")
            uploaded_file.seek(0)
            df = pd.read_csv(uploaded_file)
            st.subheader('DataFrame')
            st.write(df)
            st.subheader('Descriptive Statistics')
            st.write(df.describe())
    else:
        st.info('☝️ Upload a CSV file')
  