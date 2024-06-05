from langchain_community.document_loaders import WebBaseLoader
from langchain_community.llms import Ollama 
from langchain.chains import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

from translator import translate_text

def summarize_article(url: str) -> str:
    # Initialize the LLM with the 'llama3' model and set temperature to 0.0 for deterministic output
    llm = Ollama(model="llama3", temperature=0.0)

    # Load the web page content using WebBaseLoader
    loader = WebBaseLoader(url)
    docs = loader.load()

    # Define the template for summarizing the content
    template = """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:"""

    # Create a prompt template from the defined template
    prompt = PromptTemplate.from_template(template)
    
    # Create an LLMChain with the language model and the prompt template
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    
    # Create a StuffDocumentsChain to handle document processing with the LLMChain
    stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")
    
    # Invoke the chain on the loaded documents to get the summary response
    response = stuff_chain.invoke(docs)
    
    # Translate the summarized text from English to Russian
    trans_text = translate_text(response['output_text'], 'en', 'ru')
    
    # Return the translated summary
    return trans_text
