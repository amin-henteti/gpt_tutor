import streamlit as st
import pandas as pd
from streamlit_pandas_profiling import st_profile_report
from pandas_profiling import ProfileReport

st.header('`streamlit_pandas_profiling`')

df = pd.read_csv(
    'https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv'
)

# Configure the report options
config = {
    "samples": {
        "caption": "55"
    },
    # "correlations_threshold": 0.5,
    #     "spearman": {"threshold": 0.5},
    #     "kendall": {"threshold": 0.5}
    # }
}

# Generate the report with custom options
report = ProfileReport(df, **config)

st_profile_report(report)
report.to_file("report.html")
