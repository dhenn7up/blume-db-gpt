import os
import openai
from dotenv import load_dotenv, find_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain.schema.output_parser import OutputParserException
from langchain.agents import tool
from plotly.graph_objects import Figure
from plotly.io import from_json
import json
from langchain.agents import tool

if os.environ.get("OPENAI_API_KEY") is not None:
    openai.api_key = os.environ["OPENAI_API_KEY"]
else:
    _ = load_dotenv(find_dotenv())  # read local .env file
    openai.api_key = os.environ["OPENAI_API_KEY"]


@tool
def plotChart(data: str) -> int:
    """
    Plots json data using plotly Figure. Use it only for plotting charts and graphs.

    Args:
        data (str): A JSON string representing the figure configuration.

    Returns:
        int: A status code indicating the operation's success (0) or failure (-1).
    """
    try:
        # Attempt to load JSON data
        figure_dict = json.loads(data)

        fig = Figure()
        if "data" in figure_dict:
            for trace_data in figure_dict["data"]:
                fig.add_trace(trace_data)
        if "layout" in figure_dict:
            fig.update_layout(**figure_dict["layout"])

        # Plot the figure using Streamlit
        st.plotly_chart(fig)

        # Return success status
        return 0
    except Exception as e:
        print(f"Failed to plot chart: {e}")
        # Return failure status
        return -1


def chat_with_data_api(df, model="gpt-4o"):
    """
    A function that answers data questions from a dataframe.
    """

    llm = ChatOpenAI(model=model)
    tools = [plotChart]
    pandas_df_agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True,
        return_intermediate_steps=True,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        extra_tools=tools,
    )

    try:
        answer = pandas_df_agent(st.session_state.messages)
        if answer["intermediate_steps"]:
            action = answer["intermediate_steps"][-1][0].tool_input["query"]
            st.write(f"Executed the code ```{action}```")
        return answer["output"]
    except OutputParserException:
        error_msg = """OutputParserException error occured in LangChain agent.
            Refine your query."""
        return error_msg
    except:  # noqa: E722
        answer = "Unknown error occured in LangChain agent. Refine your query"
        return error_msg
