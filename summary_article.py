from langchain_community.document_loaders import WebBaseLoader
from langchain_community.llms import Ollama 
from langchain.chains import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

from translator import translate_text

def summarize_article(url: str) -> str:
    llm = Ollama(model = "llama3", temperature = 0.0)

    loader = WebBaseLoader(url)
    docs = loader.load()

    template = """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:"""

    prompt = PromptTemplate.from_template(template)
    
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    response=stuff_chain.invoke(docs)
    trans_text = translate_text(response['output_text'], 'en', 'ru')
    return trans_text

 