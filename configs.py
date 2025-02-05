import tomli
import streamlit as st

with open("appconfig.toml", mode="rb") as fp:
    config = tomli.load(fp)

COLUMN_ORDER = ["docviewer_url", "title", "authored", "corpus", "classification", 
                "doc_id", "pg_cnt", "word_cnt", "char_cnt", "body"]
COLUMN_CONFIGS = {
    "doc_id": st.column_config.TextColumn("Document ID", 
                                          help="Unique Document ID", 
                                          width="medium"),
    "authored": st.column_config.DatetimeColumn("Date",
                                                help="Document Date",
                                                width="small"),
    "corpus": st.column_config.TextColumn("Corpus",
                                          help="Corpus document belongs to.\
                                                See http://history-lab.org for further explanation."),
    "classification": st.column_config.TextColumn("Classification",
                                                  help="Document's original \
                                                    classification"),
    "pg_cnt": st.column_config.NumberColumn("Pages",
                                            help="Document page count \
                                                (if available)",
                                            format="%5d",
                                            width="small"),
    "word_cnt": st.column_config.NumberColumn("Words",
                                              help="Document word count",
                                              width="small"),
    "char_cnt": st.column_config.NumberColumn("Characters",
                                              help="Document character count",
                                              width="small"),                           
    "title": st.column_config.TextColumn("Title",
                                         help="Document title",
                                         width="large"),
    "docviewer_url": st.column_config.LinkColumn("Document",
                                                help="Opens the document in the DocViewer",
                                                display_text="View",
                                                width="small"),
    "body": st.column_config.TextColumn("Plain Text",
                                        help="The document body in plain text, \
                                              often produced by OCR. \
                                              Double-click on a cell to see the \
                                              first 50,000 characters of text.\
                                              Click on the View link to see \
                                              the full text of large documents."),
    "score": st.column_config.NumberColumn("Score", 
                                           format="%.2f")
    }

def footer():
    st.divider()
    st.subheader("About")
    st.markdown("Columbia University's [History Lab](http://history-lab.org) \
                created, maintains, and enhances the FOIArchive and its associated tools.")
    logo, _, description, _ = st.columns([.2, .1, .4, .3])
    logo.image('static/NEH-Preferred-Seal820.jpeg', use_column_width=True)
    description.text("")
    description.markdown("FOIArchive Search has been made possible in part by \
                         the [National Endowment for the Humanities](https://neh.gov):\
                         Democracy demands wisdom.")

def page(page_name):
    st.set_page_config(page_title=f'{page_name} * HL-FOIA',
                       page_icon=config["favicon"],
                       menu_items={'Get Help': config["help_action"],
                                   'Report a bug': config["bug_action"],
                                   'About': f"### {config['gui_title']}\n" +
                                            f"{config['about_body']}"})

# Returns mailto link for search results email report
def search_results_email(query_display):
    address = "info@history-lab.org"
    subject = "FOIArchive%20Search%20Results%20Report"
    body = "What%20were%20you%20searching%20for?" + \
            "%0A%0A%0A%0APlease%20do%20not%20edit:%0A"
    body = body + query_display.replace(" ", "%20")
    return  f"mailto:{address}?&subject={subject}&body={body}" 