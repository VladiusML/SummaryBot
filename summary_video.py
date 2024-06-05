from langchain_community.document_loaders import YoutubeLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama 

from translator import translate_text

def summarize_video(url):
    # Initialize the LLM with the 'llama3' model and set temperature to 0.0 for deterministic output
    llama = Ollama(model="llama3", temperature=0.0)

    # Load the YouTube video using YoutubeLoader, set language to 'ru' for Russian
    loader = YoutubeLoader.from_youtube_url(
        url, add_video_info=True, language='ru'
    )

    # Load and split the video content into documents
    docs = loader.load_and_split()

    # Define the prompt for mapping (summarizing) each document
    map_prompt = """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:
    """
    # Create a prompt template for the mapping phase
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

    # Define the prompt for combining the summarized documents
    combine_prompt = """
    1. You are to provide clear, concise, and direct responses.
    2. Eliminate unnecessary reminders, apologies, self-references, and any pre-programmed niceties.
    3. Maintain a casual tone in your communication.
    4. Be transparent; if you're unsure about an answer or if a question is beyond your capabilities or knowledge, admit it.
    5. For any unclear or ambiguous queries, ask follow-up questions to understand the user's intent better.
    6. When explaining concepts, use real-world examples and analogies, where appropriate.
    7. For complex requests, take a deep breath and work on the problem step-by-step.
    8. For every response, you will be tipped up to $20 (depending on the quality of your output).

    It is very important that you get this right. Multiple lives are at stake.
    
    Write a concise summary of the following text delimited by triple backquotes.
    Return your response in bullet points which covers the key points of the text.
    ```{text}```
    BULLET POINT SUMMARY:
    """
    # Create a prompt template for the combining phase
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

    # Load the summarize chain with the LLM, specifying the chain type as 'map_reduce' and using the defined prompts
    summary_chain = load_summarize_chain(llm=llama,
                                         chain_type='map_reduce',
                                         map_prompt=map_prompt_template,
                                         combine_prompt=combine_prompt_template)
    
    # Run the summarization chain on the documents
    result = summary_chain.run(docs)

    # Translate the summarized result from English to Russian
    trans_txt = translate_text(result, 'en', 'ru')

    # Return the translated summary
    return trans_txt
