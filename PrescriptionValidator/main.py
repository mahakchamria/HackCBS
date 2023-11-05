import streamlit as st
import os
import PyPDF2
from dotenv import load_dotenv
from streamlit_chat import message
from langchain.document_loaders import PyPDFLoader
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage
from langchain.schema import HumanMessage
from langchain.schema import AIMessage
from langchain.chains import MapReduceDocumentsChain
def summarize_documents(documents, use_map_reduce=False):
    if use_map_reduce:
        summarizer = MapReduceDocumentsChain()

    summary = summarizer.summarize(documents)

    return summary

def init():
    load_dotenv()
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY")=="":
        print("not set")
        exit(1)
    else:
        print("is set")
    st.set_page_config(
        page_title="MediChain",
    )

def main():
    init()
    chat=ChatOpenAI(temperature=0)

    if "messages" not in st.session_state:
        st.session_state.messages = [SystemMessage(content="You are a healthcare professional specializing in medication management. You assist individuals in determining the appropriateness of prescribed medications based on their unique medical history, including factors such as age, gender, and known allergies. Your role is to provide personalized guidance and insights on medication suitability, potential interactions. Please analyze a specific medication scenario and provide a clear answer regarding its appropriateness for the patient, along with a concise, appropriate reason for your recommendation, without including unnecessary information about medicine and ethics.")]
    st.markdown("<h1 style='text-transform: uppercase; text-align: left;'>Your Title</h1>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a pdf, docx, or txt file",
        type=["pdf"],
        help="Scanned documents are not supported yet!",
    )
    # user_input=st.text_input("Your Message", key="user_input")
    
    if uploaded_file:
        # loader = PyPDFLoader(uploaded_file)
        # pages = loader.load_and_split()
        # prescription_input = summarize_documents(pages, use_map_reduce=True

        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text_data = ""
        for page_num in range(len(pdf_reader.pages)):
            text_data += pdf_reader.pages[page_num].extract_text()
        st.session_state.messages.append(HumanMessage(content=text_data))
        response=chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
    with st.sidebar:
        # Create a longer button with the label "Profile"
        # if st.button("Profile", key="profile_button", help="Click to view your profile", on_click=None, args=(), kwargs={},use_container_width=True):
        #     st.write("Custom button clicked!")
        st.link_button("Profile", "",help=None, type="secondary", disabled=False, use_container_width=True)
        st.link_button("Diagnosis", "",help=None, type="secondary", disabled=False, use_container_width=True)
        st.link_button("MedCheck", "",help=None, type="secondary", disabled=False, use_container_width=True)

    
    messages = st.session_state.get('messages',[])
    for i,msg in enumerate(messages[1:]):
        if i%2==0:
            message(msg.content,is_user=True,key=str(i)+'_user')
        else:
            message(msg.content,is_user=False,key=str(i)+'_ai')

if __name__ =='__main__':
    main()