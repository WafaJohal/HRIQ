import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
#import streamlit_wordcloud as wordcloud



header_container = st.container()
dataset_container =  st.container()


def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(
        df, enableRowGroup=True, enableValue=True, enablePivot=True
    )

    options.configure_side_bar()

    options.configure_selection("single")
    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


with header_container:
    st.title("HRI Questionnaires")
    st.text('this webpage is meant to navigate an search for previously used questionnaire in HRI')


with dataset_container:
    st.header('Loading the dataset')
    survey_df = pd.read_excel("hri_metrics.xlsx", sheet_name="Named Surveys")
    selection = aggrid_interactive_table(df=survey_df)

    if selection:
        st.write("You selected:")
        st.json(selection["selected_rows"])
    








st.write()