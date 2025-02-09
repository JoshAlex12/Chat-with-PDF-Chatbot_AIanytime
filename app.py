import streamlit as st
from transformers import AutoTokenizer, AutoModelforSeq2SeqLM
from transformers import pipeline
import torch
import base64
import textwrap
from langchain.embeddings import SentenceTransformerEmbeddings 
from langchain.vectorstores import Chroma
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from constants import CHROMA_SETTINGS

checkpoint = "LaMini-T5-738M"
tokenizer = AutoTokenizer.from_pretrained(checkpoint)
base_model = AutoModelforSeq2SeqLM
from transformers import pipeline.from_pretrained(
  checkpoint,
  device_map="auto",
  torch_dtype=torch.float32
)

@st.cache_resource
def llm_pipeline():
  pipe=pipeline(
    'text2text generation',
    model = base_model,
    tokenizer=tokenizer,
    max_length=256,
    do_sample=True,
    Temprature=0.3;
    top_p=0.95
  )
  local_llm= HuggingfacePipeline(pipeline=pipe)
  return local_llm

@st.cache_resource
def qa_llm():
  llm = llm_pipeline()
  embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
  db = Chroma(persist_directory="db", embedding_function=embeddings, client_settings=CHROMA_SETTINGS)
  retriever = db.as_retriever()
  qa=RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuffs",
    retriever=retriever,
    return_source_documents=True
  )
  return qa

def process_answer(instruction):
  respnonse=''
  instruction=instruction
  qa=qa_llm()
  generated_text=qa(instruction)
  answer=generated_text['result']

def main():
  st.title('Search your pdf')
  with st.expander('About the app'):
    st.markdown(
      """
      This is a generative ai powered question answering app that responds to questions about your pdf file
      """
    )
    question =st.text_area("enter your question")
    if st.button("search"):
      st.info("your question: "+ question)
      st.info("your answer")
      answer,metadata=process_answer(question)
      st.write(answer)
      st.write(metadata)

if __name__=='__main__':
  main()
