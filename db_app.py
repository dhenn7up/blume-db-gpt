import os
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_experimental.sql import SQLDatabaseChain
from langchain_community.utilities import SQLDatabase
import chainlit as cl
from dotenv import load_dotenv
from pg_link import PG_LINK
from langchain.schema.runnable.config import RunnableConfig

# Load environment variables
load_dotenv(".env")


@cl.on_chat_start
def main():
    # Instantiate required classes for the user session
    db = SQLDatabase.from_uri(PG_LINK)
    # Setup the database chain
    db_chain = SQLDatabaseChain.from_llm(ChatOpenAI(), db, verbose=True)

    # Store the chain in the user session for reusability
    cl.user_session.set("llm_chain", db_chain)


@cl.on_message
async def main(message: str):
    # Retrieve the chain from the user session
    llm_chain = cl.user_session.get("llm_chain")
    QUERY = """
    Given an input question, first create a syntactically correct postgresql query to run, then look at the results of the query and return the answer.
    Use the following format:

    Question: Question here
    SQLQuery: SQL Query to run
    SQLResult: Result of the SQLQuery
    Answer: Final answer here

    {question}
    """

    question = QUERY.format(question=message.content)
    # Call the chain asynchronously
    res = await llm_chain.acall(
        question, callbacks=[cl.AsyncLangchainCallbackHandler()]
    )
    await cl.Message(content=res["result"]).send()
