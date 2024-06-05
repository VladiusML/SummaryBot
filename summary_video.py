from langchain_community.document_loaders import YoutubeLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama 

from translator import translate_text


def summarize_video(url):
    llama = Ollama(model = "llama3", temperature = 0.0)

    loader = YoutubeLoader.from_youtube_url(
        url, add_video_info = True, language = 'ru'
    )

    docs = loader.load_and_split()

    map_prompt = """
    Write a concise summary of the following:
    "{text}"
    CONCISE SUMMARY:
    """
    map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])

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
    combine_prompt_template = PromptTemplate(template=combine_prompt, input_variables=["text"])

    summary_chain = load_summarize_chain(llm=llama,
                                     chain_type='map_reduce',
                                     map_prompt=map_prompt_template,
                                     combine_prompt=combine_prompt_template)
    
    result = summary_chain.run(docs)
    trans_txt = translate_text(result, 'en', 'ru')

    return trans_txt