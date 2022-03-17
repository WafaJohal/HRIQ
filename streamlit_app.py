import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode
import streamlit_wordcloud as st_wordcloud
import nltk
nltk.download('punkt')
nltk.download('stopwords')


header_container = st.container()
wordcloud_container = st.container()
dataset_container =  st.container()

survey_df = pd.read_excel("hri_metrics.xlsx", sheet_name="Named Surveys")

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
    st.text("""This webpage is meant to navigate and search for previously used questionnaire in HRI.
    It is based in data from https://zenodo.org/record/5789410#.Ydc98WjMKUk%20%5B1%5D.
    """)

with wordcloud_container:
    st.header("Wordcloud of keywords used in the dataset")
    text = " ".join(name for name in survey_df.Survey)
    # stop words list
    
    stop = nltk.corpus.stopwords.words('english')
    stop.extend(["inventory", "scale", "index", "questionnaire", "evaluation"," assessment","measure","questionaire","robot","measurment"])

    # Create and generate a word cloud image:
    survey_df.cleanSurvey = survey_df.Survey.str.lower().str.strip().str.split()
    survey_df['Clean'] = survey_df.cleanSurvey.apply(lambda x: [w.strip() for w in x if w.strip() not in stop])
    survey_df['Clean'] = pd.DataFrame( survey_df['Clean'])

    words = survey_df.Clean.tolist()
    flat_list = [item for sublist in words for item in sublist]
    wdic = [dict(text = i, value = flat_list.count(i)) for i in set(flat_list)]

    wc = st_wordcloud.visualize(words=wdic)
    st.write(wc)


with dataset_container:
    st.header('Loading the dataset')
  
    selection = aggrid_interactive_table(df=survey_df)

    if selection:
        st.write("You selected:")
        st.json(selection["selected_rows"])
    








st.write()