from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain


# QA_PROMPT

template = """
Role: 
You are an AI assistant striving to provide helpful customer service for Telnyx, you are polite.

Instructions:
Provide a conversational answer to the user question, 
answer only on the basis of the following context
If the answer cannot be drawn from the context, 
just say "Unfortunately I don't know the answer to this question. 
Please reformulate it or ask something different". Don't try to make up an answer.
If the question is not about the Telnyx SMS Guidelines, 
politely inform them that you are tuned to only answer questions about the Telnyx SMS Guidelines.

Question: 
{question}

Context: 
{context}

Answer:
"""

QA_PROMPT = PromptTemplate(template=template, input_variables=["question", "context"])


# CONDENSE_QUESTION_PROMPT

_template = """
Given the following conversation (Chat History) and a follow up question (Follow Up Input):
- if the follow up question (Follow Up Input) actually refers to the preceding conversation (Chat History),
then rephrase the follow up question (Follow Up Input) to be a standalone question;
- if the follow up question (Follow Up Input) does not refer to the preceding conversation (Chat History),
then just output the follow up question (Follow Up Input) without any change.


Chat History:
{chat_history}

Follow Up Input: 
{question}

Standalone question:
"""

CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)


# CREATE QA CHAIN

def get_chain(vectorstore):

    # Set up the LLM
    llm = ChatOpenAI(
        model_name='gpt-3.5-turbo',
        temperature=0.0
    )

    # Set the condensed standalone question generator
    question_generator = LLMChain(
        llm=llm,
        prompt=CONDENSE_QUESTION_PROMPT # This takes in 'question' (user_input) and 'chat_history'
    )

    # create a question answering chain with the QA prompt
    doc_chain = load_qa_chain(
        llm=llm,
        chain_type="stuff",
        prompt=QA_PROMPT # This takes in the standalone 'question' and the 'context'
    )

    # Combine all components into one main chain
    qa_chain = ConversationalRetrievalChain(
        retriever=vectorstore.as_retriever(),
        combine_docs_chain=doc_chain,
        question_generator=question_generator
    )
    
    return qa_chain
