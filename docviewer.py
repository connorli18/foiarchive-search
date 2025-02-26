import streamlit as st
import configs as c
doc_id = st.query_params.get('doc_id') 
c.page(f"{doc_id}")    # must be 1st streamlit cmd or strange behavior ensues
import datetime
import sqlgen as sg
import db
from collections import Counter
import re
from stopwords import get_stopwords
import pandas as pd

STOP_WORDS = set(get_stopwords("en"))

def display_date(date):
    if date:
        if date.time() == datetime.time(0, 0):
            date_str = f"{date.date().strftime('%b %d, %Y')}"
        else:
            date_str = f"{date.strftime('%b %d, %Y %H:%M:%S')}"
        st.markdown(f"**{date_str}**") 

def display_citation(title, corpus_name, doc_id):
    date_str = f"{datetime.date.today().strftime('%b %d, %Y')}"
    st.sidebar.markdown(f"### Citation:")
    citation_str = (f"{title}, _{corpus_name}_, Document ID Number: {doc_id}, "
                    f"http://www.history-lab.org [Accessed: {date_str}]")
    st.sidebar.markdown(citation_str)

def display_entities(doc_id):
    doc_entities_sql = sg.by_doc_id('doc_entities', doc_id)
    edf = db.execute(doc_entities_sql)
    entity_list = edf.iloc[0]['entity_list']
    if entity_list:
        st.sidebar.markdown("### Entities:")
        st.sidebar.write(entity_list)  

def display_topics(doc_id):
    doc_topics_sql = sg.by_doc_id('doc_topics', doc_id)
    tdf = db.execute(doc_topics_sql)
    if not tdf.empty:
        st.sidebar.markdown("### Topic(s):")
        st.sidebar.dataframe(tdf, hide_index=True)

def display_source(source):
    if source:
        st.markdown(f"[Source Document PDF]({source})")

def display_frus_body(id):
    qry = sg.by_doc_id('docviewer_frus', doc_id)
    results = db.execute(qry)
    source = results.iloc[0]['source']
    body = results.iloc[0]['body']
    st.markdown(f"[US State Department, Office of the Historian]({source})")
    st.markdown(body, unsafe_allow_html=True)

def display_body(doc):
    if doc.body:
        if doc.corpus == 'frus':
            display_frus_body(doc.doc_id)
        else:
            st.text(doc.body)
    else:
        st.write("No document body")
 
def display_cnt(type, cnt):
    if cnt:
        st.sidebar.markdown(f"### {type}: {cnt}")

def display_common_words(doc):
    words = re.findall(r'\b\w+\b', doc.body.lower())
    # set arbitrary length for 5 to filter out short words
    filtered_words = [word for word in words if word not in STOP_WORDS and len(word) >= 5]
    word_counts = Counter(filtered_words).most_common(10)
    df = pd.DataFrame(word_counts, columns=["Word", "Count"])
    st.write("###### Most Common Words")
    st.dataframe(df, hide_index=True, use_container_width=True, height=200)

def display_doc(doc):
    col1, col2, col3 = st.columns([10, 1, 5])
    with col1:
        st.subheader(doc.title)
        display_date(doc.authored)
        display_source(doc.source)
        display_body(doc)
        display_citation(doc.title, doc.corpus_title, doc.doc_id)
    
    with col3:
        st.subheader("Document NLP Analytics")
        display_common_words(doc)

    # Move sidebar content outside of the columns
    st.sidebar.markdown(f"### Original Classification: {doc.classification}") 
    display_entities(doc.doc_id)
    display_topics(doc.doc_id)
    display_cnt('Pages', doc.pg_cnt)
    display_cnt('Words', doc.word_cnt)

print(f'viewer|{datetime.datetime.now()}|{doc_id}', flush=True)    # logging
if doc_id:
    doc_sql = sg.by_doc_id('docviewer', doc_id)
    doc_df = db.execute(doc_sql)
    if doc_df.empty:
        st.warning(f"Warning: No document with ID {doc_id} found")
    else:                   # doc exists, display it
        display_doc(doc_df.iloc[0])
else:
    st.error("Error: No document ID provided")
c.footer()
