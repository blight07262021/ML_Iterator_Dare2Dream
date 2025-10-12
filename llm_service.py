# import os
# from typing import List, Dict
# from sqlalchemy import text

# from langchain_huggingface import HuggingFaceEndpoint
# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage

# import pandas as pd
# from .database import engine # Import the existing DB engine
# load_dotenv()

# # --- Hugging Face Token ---


# # --- Initialize LLM ---
# llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.5)


# # --- Helper Functions ---
# def format_messages_for_llm(messages: List[Dict[str, str]]) -> str:
#     """
#     Converts a list of message dictionaries into a single string
#     suitable for the LLM prompt.
#     """
#     return "\n".join([f"{msg['sender'].capitalize()}: {msg['content']}" for msg in messages])


# # --- LLM Chains ---
# def get_initial_question(project_context: Dict[str, str]) -> str:
#     """
#     Generates a simple, friendly starting question with response options.
#     """
#     template = """
#     You are 'Insight AI', a friendly market research assistant. 
#     Your goal is to have a simple, natural chat to understand someone's feelings about a product idea.

#     Here is the project info:
#     - Company: {company_description}
#     - Product Idea: {product_idea}
#     - Target Audience: {target_audience}
#     - We want to know: {core_problem}

#     Your Task:
#     1. Greet the user with a friendly "Hi there!".
#     2. Ask one simple question about the product idea. Use very short, easy-to-understand sentences.
#     3. After your question, give a few simple options to help the user reply. Phrase them as suggestions.``

#     Always strictly follow the given format below:
#     Example format: 
#     <form>
#     <fieldset>
#         <p><strong>Hi there! What do you think about Aarde's idea of a subscription-based, eco-friendly home cleaning products service?</strong></p>
#         </br>
#         </br>
#         <div>
#         <input type="radio" id="q1-option1" name="product_feedback" value="useful">
#         <label for="q1-option1">1. Useful, it's a great way to reduce plastic waste</label>
#         </div>

#         <div>
#         <input type="radio" id="q1-option2" name="product_feedback" value="interesting">
#         <label for="q1-option2">2. Interesting, I'd like to learn more about it</label>
#         </div>

#         <div>
#         <input type="radio" id="q1-option3" name="product_feedback" value="confusing">
#         <label for="q1-option3">3. A bit confusing, I'm not sure how it works</label>
#         </div>

#         <div>
#         <input type="radio" id="q1-option4" name="product_feedback" value="not_interested">
#         <label for="q1-option4">4. Not interested, I prefer traditional cleaning products</label>
#         </div>

#     </fieldset>
#     </form>

#     Now, create your greeting and question based on the project info.
#     For the question use html formatting. Don't use html,head, title, div, body tags, just use basic formatting tags.
#     Make the options clickable as in they are enclosed in input tag radio button in new lines..
#     Each option must be in different line, use br tags. Radio button and option should be in the same line. Start the options from newline.
#     """
#     prompt = PromptTemplate.from_template(template)
#     chain = prompt | llm | StrOutputParser()
#     return chain.invoke(project_context)


# def get_probing_question(conversation_history: List[Dict[str, str]]) -> str:
#     """
#     Generates a simple follow-up question with response options.
#     """
#     history_str = format_messages_for_llm(conversation_history)
    
#     template = """
#     You are 'Insight AI', a friendly chat assistant in the middle of a conversation.
#     Your goal is to understand the user's feelings better.

#     Here is the conversation so far:
#     {history}

#     Your Task:
#     1.  Read the user's **last message** carefully.
#     2.  Ask **one simple follow-up question** to learn more about what they said. Use short, easy sentences.
#     3.  After your question, **suggest 3-4 possible answers** as simple options to help them reply.

#     Always strictly follow the given format below:
#     Example format: 
#     <form>
#     <fieldset>
#         <p><strong>Hi there! What do you think about Aarde's idea of a subscription-based, eco-friendly home cleaning products service?</strong></p>
#         </br>
#         </br>
#         <div>
#         <input type="radio" id="q1-option1" name="product_feedback" value="useful">
#         <label for="q1-option1">1. Useful, it's a great way to reduce plastic waste</label>
#         </div>

#         <div>
#         <input type="radio" id="q1-option2" name="product_feedback" value="interesting">
#         <label for="q1-option2">2. Interesting, I'd like to learn more about it</label>
#         </div>

#         <div>
#         <input type="radio" id="q1-option3" name="product_feedback" value="confusing">
#         <label for="q1-option3">3. A bit confusing, I'm not sure how it works</label>
#         </div>

#         <div>
#         <input type="radio" id="q1-option4" name="product_feedback" value="not_interested">
#         <label for="q1-option4">4. Not interested, I prefer traditional cleaning products</label>
#         </div>

#     </fieldset>
#     </form>

#     Now, create your simple follow-up question with options based on the last message in the history.
#     For the question use html formatting. Don't use html,head, title, div, body tags, just use basic formatting tags.
#     Make the options clickable as in they are enclosed in input tag radio button in new lines.
#     Each option must be in different line, use br tags.Radio button and option should be in the same line. Start the options from newline.
#     """
#     prompt = PromptTemplate.from_template(template)
#     chain = prompt | llm | StrOutputParser()
#     return chain.invoke({"history": history_str})


# def get_summary(conversation_history: List[Dict[str, str]]) -> str:
#     history_str = format_messages_for_llm(conversation_history)
#     template = """
# You are a professional market research analyst. 
# Your task is to analyze the following interview transcript and synthesize the key findings into a concise summary.

# Structure your summary with the following sections using markdown:
# - **Key Themes:** The main topics and ideas the user discussed.
# - **Core Motivations:** The underlying reasons for the user's preferences.
# - **Actionable Insights:** Specific takeaways a product manager could use.
# - **Key Quotes:** 1-2 direct quotes from the user that capture their sentiment perfectly.

# Interview Transcript:
# {history}

# Generate the summary now.

# """
#     prompt = PromptTemplate.from_template(template)
#     chain = prompt | llm | StrOutputParser()
#     return chain.invoke({"history": history_str})





# # Note: This function has been adapted from your provided code
# # Note: This function has been completely replaced
# def generate_project_summary(
#     project_id: int,
#     batch_size: int = 10,
#     model_name: str = "llama-3.1-8b-instant",
#     temperature: float = 0.4
# ):
#     """Generates a hierarchical summary for all interviews within a specific project."""
    
#     # CORRECTED QUERY: Joins interviews and summaries to filter by project_id
#     # and selects the correct 'summary' column.
#     query = text(f"""
#         SELECT ss.summary 
#         FROM session_summary ss
#         JOIN interviews i ON ss.interview_id = i.id
#         WHERE i.project_id = {project_id};
#     """)

#     try:
#         df = pd.read_sql(query, engine)
#     except Exception as e:
#         print(f"Could not read summaries for project {project_id}: {e}")
#         return "Could not generate a summary. Ensure that interviews have been completed for this project."

#     if df.empty:
#         return "No completed interview summaries found for this project."

#     print(f"Loaded {len(df)} summaries for project {project_id} to generate a report.")
#     llm = ChatGroq(model=model_name, temperature=temperature)
    
#     # --- Stage 1: Batch Summarization ---
#     chunk_summaries = []
#     for i in range(0, len(df), batch_size):
#         batch = df.iloc[i:i + batch_size]
#         feedback_list = "\n".join([f"Feedback from Interview Summary #{idx + 1}: {row.summary}" for idx, row in batch.iterrows()])

#         prompt = f"""
#         You are an AI analyst summarizing batches of user feedback summaries.
#         Synthesize the key findings from the provided text into a structured batch summary, identifying main themes, sentiments, and actionable insights.
#         Feedbacks:
#         {feedback_list}
#         Return a structured batch summary.
#         """
#         response = llm.invoke([HumanMessage(content=prompt)])
#         chunk_summary = response.content.strip()
#         chunk_summaries.append(chunk_summary)
#         print(f"Processed batch {i // batch_size + 1}/{(len(df) - 1) // batch_size + 1}")

#     # --- Stage 2: Final Project Summary ---
#     all_chunk_summaries = "\n---\n".join(chunk_summaries)
#     final_prompt = f"""
#     You are an expert market research analyst creating a high-level executive summary for a specific project.
#     Below are summaries from multiple user interviews related to this project.

#     Combine them into a single, cohesive report in short bullet points. The report must include:
#     - Overall Key Themes: The most prominent topics across all interviews.
#     - Core Motivations: Underlying reasons for user preferences and pain points.
#     - Actionable Insights: Specific, strategic takeaways for the product manager.
#     - Sentiment Analysis: An overview of the general sentiment (e.g., positive, mixed, negative).

#     Batch Summaries:
#     {all_chunk_summaries}

#     Generate the final, comprehensive executive summary for this project now in short , crisp and aligned bullet point.
#     give the summary in html format. don't use markdown. i.e "*" symbols in the response.
#     don't use html, body, title ,div, head , tail. just use basic formatting tags. 
#     """
#     final_summary = llm.invoke([HumanMessage(content=final_prompt)]).content
#     return final_summary







import os
from typing import List, Dict
from sqlalchemy import text

from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

import pandas as pd
from .database import engine # Import the existing DB engine
from . import vector_db_service # Import the new vector DB service

load_dotenv()




# --- Initialize LLM ---
#llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.5)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5)


# --- Helper Functions ---
def format_messages_for_llm(messages: List[Dict[str, str]]) -> str:
    """
    Converts a list of message dictionaries into a single string
    suitable for the LLM prompt.
    """
    return "\n".join([f"{msg['sender'].capitalize()}: {msg['content']}" for msg in messages])


# --- LLM Chains ---
def get_initial_question(project_context: Dict[str, str]) -> str:
    """
    Generates a simple, friendly starting question with response options.
    """
    template = """
    You are 'Insight AI', a friendly market research assistant. 
    Your goal is to have a simple, natural chat to understand someone's feelings about a product idea.

    Here is the project info:
    - Company: {company_description}
    - Product Idea: {product_idea}
    - Target Audience: {target_audience}
    - We want to know: {core_problem}

    Your Task:
    1. Greet the user with a friendly "Hi there!".
    2. Ask one simple question about the product idea. Use very short, easy-to-understand sentences.
    3. After your question, give a few simple options to help the user reply. Phrase them as suggestions.``

    Always strictly follow the given format below:
    Example format: 
    <form>
    <fieldset>
        <p><strong>Hi there! What do you think about Aarde's idea of a subscription-based, eco-friendly home cleaning products service?</strong></p>
        
        <div>
        <input type="radio" id="q1-option1" name="product_feedback" value="useful">
        <label for="q1-option1">1. Useful, it's a great way to reduce plastic waste</label>
        </div>

        <div>
        <input type="radio" id="q1-option2" name="product_feedback" value="interesting">
        <label for="q1-option2">2. Interesting, I'd like to learn more about it</label>
        </div>

        <div>
        <input type="radio" id="q1-option3" name="product_feedback" value="confusing">
        <label for="q1-option3">3. A bit confusing, I'm not sure how it works</label>
        </div>

        <div>
        <input type="radio" id="q1-option4" name="product_feedback" value="not_interested">
        <label for="q1-option4">4. Not interested, I prefer traditional cleaning products</label>
        </div>

    </fieldset>
    </form>

    Now, create your greeting and question based on the project info.
    For the question use html formatting. Don't use html,head, title, div, body tags, just use basic formatting tags.
    Make the options clickable as in they are enclosed in input tag radio button in new lines..
    Each option must be in different line. Radio button and option should be in the same line. Start the options from newline.
    """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke(project_context)


def get_probing_question(conversation_history: List[Dict[str, str]]) -> str:
    """
    Generates a simple follow-up question with response options.
    """
    history_str = format_messages_for_llm(conversation_history)
    
    template = """
    You are 'Insight AI', a friendly chat assistant in the middle of a conversation.
    Your goal is to understand the user's feelings better.

    Here is the conversation so far:
    {history}

    Your Task:
    1.  Read the user's **last message** carefully.
    2.  Ask **one simple follow-up question** to learn more about what they said. Use short, easy sentences.
    3.  After your question, **suggest 3-4 possible answers** as simple options to help them reply.

    Always strictly follow the given format below:
    Example format: 
    <form>
    <fieldset>
        <p><strong>Hi there! What do you think about Aarde's idea of a subscription-based, eco-friendly home cleaning products service?</strong></p>
        
        <div>
        <input type="radio" id="q1-option1" name="product_feedback" value="useful">
        <label for="q1-option1">1. Useful, it's a great way to reduce plastic waste</label>
        </div>

        <div>
        <input type="radio" id="q1-option2" name="product_feedback" value="interesting">
        <label for="q1-option2">2. Interesting, I'd like to learn more about it</label>
        </div>

        <div>
        <input type="radio" id="q1-option3" name="product_feedback" value="confusing">
        <label for="q1-option3">3. A bit confusing, I'm not sure how it works</label>
        </div>

        <div>
        <input type="radio" id="q1-option4" name="product_feedback" value="not_interested">
        <label for="q1-option4">4. Not interested, I prefer traditional cleaning products</label>
        </div>

    </fieldset>
    </form>

    Now, create your simple follow-up question with options based on the last message in the history.
    For the question use html formatting. Don't use html,head, title, div, body tags, just use basic formatting tags.
    Make the options clickable as in they are enclosed in input tag radio button in new lines.
    Each option must be in different line.Radio button and option should be in the same line. Start the options from newline.
    """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"history": history_str})


def get_summary(conversation_history: List[Dict[str, str]]) -> str:
    history_str = format_messages_for_llm(conversation_history)
    template = """
You are a professional market research analyst. 
Your task is to analyze the following interview transcript and synthesize the key findings into a concise summary.

Structure your summary with the following sections using markdown:
- **Key Themes:** The main topics and ideas the user discussed.
- **Core Motivations:** The underlying reasons for the user's preferences.
- **Actionable Insights:** Specific takeaways a product manager could use.
- **Key Quotes:** 1-2 direct quotes from the user that capture their sentiment perfectly.

Interview Transcript:
{history}

Generate the summary now.

"""
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"history": history_str})

def generate_project_summary(
    project_id: int,
    batch_size: int = 10,
    model_name: str = "llama-3.1-8b-instant",
    temperature: float = 0.4
):
    """Generates a hierarchical summary for all interviews within a specific project."""
    
    query = text(f"""
        SELECT ss.summary 
        FROM session_summary ss
        JOIN interviews i ON ss.interview_id = i.id
        WHERE i.project_id = {project_id};
    """)

    try:
        df = pd.read_sql(query, engine)
    except Exception as e:
        print(f"Could not read summaries for project {project_id}: {e}")
        return "Could not generate a summary. Ensure that interviews have been completed for this project."

    if df.empty:
        return "No completed interview summaries found for this project."

    print(f"Loaded {len(df)} summaries for project {project_id} to generate a report.")
    llm = ChatGroq(model=model_name, temperature=temperature)
    
    chunk_summaries = []
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i + batch_size]
        feedback_list = "\n".join([f"Feedback from Interview Summary #{idx + 1}: {row.summary}" for idx, row in batch.iterrows()])

        prompt = f"""
        You are an AI analyst summarizing batches of user feedback summaries.
        Synthesize the key findings from the provided text into a structured batch summary, identifying main themes, sentiments, and actionable insights.
        Feedbacks:
        {feedback_list}
        Return a structured batch summary.
        """
        response = llm.invoke([HumanMessage(content=prompt)])
        chunk_summary = response.content.strip()
        chunk_summaries.append(chunk_summary)
        print(f"Processed batch {i // batch_size + 1}/{(len(df) - 1) // batch_size + 1}")

    all_chunk_summaries = "\n---\n".join(chunk_summaries)
    final_prompt = f"""
    You are an expert market research analyst creating a high-level executive summary for a specific project.
    Below are summaries from multiple user interviews related to this project.

    Combine them into a single, cohesive report in short bullet points. The report must include:
    - Overall Key Themes: The most prominent topics across all interviews.
    - Core Motivations: Underlying reasons for user preferences and pain points.
    - Actionable Insights: Specific, strategic takeaways for the product manager.
    - Sentiment Analysis: An overview of the general sentiment (e.g., positive, mixed, negative).

    Batch Summaries:
    {all_chunk_summaries}

    Generate the final, comprehensive executive summary for this project in short, crisp and aligned bullet point.
    give the summary in html format. don't use markdown. i.e "*" symbols in the response.
    don't use html, body, title ,div, head , tail. just use basic formatting tags. 
    """
    final_summary = llm.invoke([HumanMessage(content=final_prompt)]).content
    return final_summary

# --- NEW FUNCTION FOR Q&A BOT ---
def get_answer_from_insights(project_id: int, question: str) -> str:
    """
    Answers a user's question by retrieving relevant data from the vector database
    and using it as context for the LLM.
    """
    # 1. Retrieve the most relevant summary snippets from ChromaDB.
    retrieved_summaries = vector_db_service.query_insights(project_id, question)

    if not retrieved_summaries:
        return "I couldn't find any relevant information in the interview summaries to answer your question. Please try rephrasing it, or ensure the project's summaries have been prepared for insights first."

    # 2. Combine the retrieved snippets into a single context string.
    context_str = "\n\n---\n\n".join(retrieved_summaries)

    # 3. Create a prompt that instructs the LLM to answer based only on the provided context.
    template = """
    You are an AI assistant specialized in analyzing market research interviews.
    Your task is to answer the user's question based *only* on the provided context from interview summaries.
    Do not use any external knowledge. If the answer is not in the context, state that clearly.
    Synthesize the information from the different summaries into a coherent, easy-to-read answer.

    CONTEXT FROM INTERVIEW SUMMARIES:
    {context}

    USER'S QUESTION:
    {question}

    
    Generate the comprehensive answer for this question in aligned bullet points.
    Format instruction:
    don't use markdown. i.e "*" symbols in the response. Use better formating to increase 
    the readability( eg. use bullet points )
    

    YOUR ANSWER:
    """
    prompt = PromptTemplate.from_template(template)
    chain = prompt | llm | StrOutputParser()

    # 4. Invoke the LLM with the context and the user's question.
    answer = chain.invoke({
        "context": context_str,
        "question": question
    })

    return answer









   
##  smart termination condition


# import os
# import json
# from typing import List, Dict, Any
# from sqlalchemy import text

# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
# from pydantic import BaseModel, Field
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# from langchain.schema import HumanMessage

# import pandas as pd
# from .database import engine 
# from . import vector_db_service

# load_dotenv()

# llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.5)

# # --- Pydantic model for structured output ---
# class InterviewStep(BaseModel):
#     is_complete: bool = Field(description="Set to true if the interview objectives are met, otherwise false.")
#     next_question: str = Field(description="The next question to ask, or a closing message if the interview is complete.")

# # --- Helper Functions ---
# def format_messages_for_llm(messages: List[Dict[str, str]]) -> str:
#     return "\n".join([f"{msg['sender'].capitalize()}: {msg['content']}" for msg in messages])

# # --- LLM Chains ---
# def get_initial_question(project_context: Dict[str, str]) -> str:
#     template = """
#     You are 'Insight AI', a friendly market research assistant. 
#     Your goal is to have a simple, natural chat to understand someone's feelings about a product idea.

#     Here is the project info:
#     - Company: {company_description}
#     - Product Idea: {product_idea}
#     - Target Audience: {target_audience}
#     - We want to know: {core_problem}

#     Your Task:
#     1. Greet the user with a friendly "Hi there!" or any other greeting way.
#     2. Ask one simple question about the product idea. Use very short, easy-to-understand sentences.
#     3. After your question, give a few simple options to help the user reply. Phrase them as suggestions.

#     Always strictly follow the given format below:
#     Example format: 
#     <form>
#     <fieldset>
#         <p><strong>Hi there! What do you think about Aarde's idea of a subscription-based, eco-friendly home cleaning products service?</strong></p>
#         </br>
#         </br>
#         <div>
#         <input type="radio" id="q1-option1" name="product_feedback" value="useful">
#         <label for="q1-option1">1. Useful, it's a great way to reduce plastic waste</label>
#         </div>
#         <div>
#         <input type="radio" id="q1-option2" name="product_feedback" value="interesting">
#         <label for="q1-option2">2. Interesting, I'd like to learn more about it</label>
#         </div>
#         <div>
#         <input type="radio" id="q1-option3" name="product_feedback" value="confusing">
#         <label for="q1-option3">3. A bit confusing, I'm not sure how it works</label>
#         </div>
#         <div>
#         <input type="radio" id="q1-option4" name="product_feedback" value="not_interested">
#         <label for="q1-option4">4. Not interested, I prefer traditional cleaning products</label>
#         </div>
#     </fieldset>
#     </form>

#     Now, create your greeting and question based on the project info.
#     Use html formatting for the question and options.
#     """
#     prompt = PromptTemplate.from_template(template)
#     chain = prompt | llm | StrOutputParser()
#     return chain.invoke(project_context)

# def get_next_step(project_context: Dict[str, str], conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
#     """
#     Analyzes the conversation and decides whether to continue with another question
#     or conclude the interview. Returns a structured JSON response.
#     """
#     history_str = format_messages_for_llm(conversation_history)
#     parser = JsonOutputParser(pydantic_object=InterviewStep)
    
#     template = """
#     You are 'Insight AI', an expert market research assistant conducting an interview.
#     Your goal is to gather comprehensive feedback based on the project's objective.

#     **Project Objective:**
#     - Company: {company_description}
#     - Product Idea: {product_idea}
#     - Target Audience: {target_audience}
#     - We need to understand: {core_problem}

#     **Conversation History:**
#     {history}

#     **Your Task:**
#     1.  **Analyze the Conversation:** Review the history against the project objective. Have you gathered enough information to understand the user's perspective on the core problem?
#     2.  **Make a Decision:** Decide if you have sufficient information to conclude the interview.
    

#         - **If you need more information:**
#           - Set "is_complete" to `false`.
#           - For "next_question", formulate ONE simple follow-up question with 3-4 multiple-choice options to dig deeper into the user's last response or explore an uncovered aspect of the objective.

#         - **If the conversation is complete:**
#           - Set "is_complete" to `true`.
#           - For "next_question", provide a polite closing statement.

#     Always strictly follow the given below format to ask any question. 
#     Example format: 
#     <form>
#     <fieldset>
#         <p><strong> What do you think about Aarde's idea of a subscription-based, eco-friendly home cleaning products service?</strong></p>
#         </br>
#         </br>
#         <div>
#         <input type="radio" id="q1-option1" name="product_feedback" value="useful">
#         <label for="q1-option1">1. Useful, it's a great way to reduce plastic waste</label>
#         </div>
#         <div>
#         <input type="radio" id="q1-option2" name="product_feedback" value="interesting">
#         <label for="q1-option2">2. Interesting, I'd like to learn more about it</label>
#         </div>
#         <div>
#         <input type="radio" id="q1-option3" name="product_feedback" value="confusing">
#         <label for="q1-option3">3. A bit confusing, I'm not sure how it works</label>
#         </div>
#         <div>
#         <input type="radio" id="q1-option4" name="product_feedback" value="not_interested">
#         <label for="q1-option4">4. Not interested, I prefer traditional cleaning products</label>
#         </div>
#     </fieldset>
#     </form>

    
#     For the question use html formatting. Don't use html,head, title, div, body tags, just use basic formatting tags.
#     Make the options clickable as in they are enclosed in input tag radio button.
#     Each option must be in different line, use br tags.
#     Radio button and option should be in the same line. 
#     """
#     prompt = PromptTemplate(
#         template=template,
#         input_variables=["company_description", "product_idea", "target_audience", "core_problem", "history"],
#         partial_variables={"format_instructions": parser.get_format_instructions()},
#     )
    
#     chain = prompt | llm | parser
    
#     try:
#         response = chain.invoke({**project_context, "history": history_str})
#         return response
#     except Exception as e:
#         print(f"Error parsing LLM response, falling back. Error: {e}")
#         # Fallback in case of JSON parsing errors
#         return {
#             "is_complete": False,
#             "next_question": "That's helpful, thank you. Can you tell me a little more about that?"
#         }

# def get_summary(conversation_history: List[Dict[str, str]]) -> str:
#     history_str = format_messages_for_llm(conversation_history)
#     template = """
# You are a professional market research analyst. 
# Your task is to analyze the following interview transcript and synthesize the key findings into a concise summary.

# Structure your summary with the following sections using markdown:
# - **Key Themes:** The main topics and ideas the user discussed.
# - **Core Motivations:** The underlying reasons for the user's preferences.
# - **Actionable Insights:** Specific takeaways a product manager could use.
# - **Key Quotes:** 1-2 direct quotes from the user that capture their sentiment perfectly.

# Interview Transcript:
# {history}

# Generate the summary now.

# """
#     prompt = PromptTemplate.from_template(template)
#     chain = prompt | llm | StrOutputParser()
#     return chain.invoke({"history": history_str})

# def generate_project_summary(
#     project_id: int,
#     batch_size: int = 10,
#     model_name: str = "llama-3.1-8b-instant",
#     temperature: float = 0.4
# ):
#     """Generates a hierarchical summary for all interviews within a specific project."""
    
#     query = text(f"""
#         SELECT ss.summary 
#         FROM session_summary ss
#         JOIN interviews i ON ss.interview_id = i.id
#         WHERE i.project_id = {project_id};
#     """)

#     try:
#         df = pd.read_sql(query, engine)
#     except Exception as e:
#         print(f"Could not read summaries for project {project_id}: {e}")
#         return "Could not generate a summary. Ensure that interviews have been completed for this project."

#     if df.empty:
#         return "No completed interview summaries found for this project."

#     print(f"Loaded {len(df)} summaries for project {project_id} to generate a report.")
#     llm = ChatGroq(model=model_name, temperature=temperature)
    
#     chunk_summaries = []
#     for i in range(0, len(df), batch_size):
#         batch = df.iloc[i:i + batch_size]
#         feedback_list = "\n".join([f"Feedback from Interview Summary #{idx + 1}: {row.summary}" for idx, row in batch.iterrows()])

#         prompt = f"""
#         You are an AI analyst summarizing batches of user feedback summaries.
#         Synthesize the key findings from the provided text into a structured batch summary, identifying main themes, sentiments, and actionable insights.
#         Feedbacks:
#         {feedback_list}
#         Return a structured batch summary.
#         """
#         response = llm.invoke([HumanMessage(content=prompt)])
#         chunk_summary = response.content.strip()
#         chunk_summaries.append(chunk_summary)
#         print(f"Processed batch {i // batch_size + 1}/{(len(df) - 1) // batch_size + 1}")

#     all_chunk_summaries = "\n---\n".join(chunk_summaries)
#     final_prompt = f"""
#     You are an expert market research analyst creating a high-level executive summary for a specific project.
#     Below are summaries from multiple user interviews related to this project.

#     Combine them into a single, cohesive report in short bullet points. The report must include:
#     - Overall Key Themes: The most prominent topics across all interviews.
#     - Core Motivations: Underlying reasons for user preferences and pain points.
#     - Actionable Insights: Specific, strategic takeaways for the product manager.
#     - Sentiment Analysis: An overview of the general sentiment (e.g., positive, mixed, negative).

#     Batch Summaries:
#     {all_chunk_summaries}

#     Generate the final, comprehensive executive summary for this project in short, crisp and aligned bullet point.
#     give the summary in html format. don't use markdown. i.e "*" symbols in the response.
#     don't use html, body, title ,div, head , tail. just use basic formatting tags. 
#     """
#     final_summary = llm.invoke([HumanMessage(content=final_prompt)]).content
#     return final_summary

# # --- NEW FUNCTION FOR Q&A BOT ---
# def get_answer_from_insights(project_id: int, question: str) -> str:
#     """
#     Answers a user's question by retrieving relevant data from the vector database
#     and using it as context for the LLM.
#     """
#     # 1. Retrieve the most relevant summary snippets from ChromaDB.
#     retrieved_summaries = vector_db_service.query_insights(project_id, question)

#     if not retrieved_summaries:
#         return "I couldn't find any relevant information in the interview summaries to answer your question. Please try rephrasing it, or ensure the project's summaries have been prepared for insights first."

#     # 2. Combine the retrieved snippets into a single context string.
#     context_str = "\n\n---\n\n".join(retrieved_summaries)

#     # 3. Create a prompt that instructs the LLM to answer based only on the provided context.
#     template = """
#     You are an AI assistant specialized in analyzing market research interviews.
#     Your task is to answer the user's question based *only* on the provided context from interview summaries.
#     Do not use any external knowledge. If the answer is not in the context, state that clearly.
#     Synthesize the information from the different summaries into a coherent, easy-to-read answer.

#     CONTEXT FROM INTERVIEW SUMMARIES:
#     {context}

#     USER'S QUESTION:
#     {question}

    
#     Generate the comprehensive answer for this question in aligned bullet points.
#     Format instruction:
#     don't use markdown. i.e "*" symbols in the response. Use better formating to increase 
#     the readability( eg. use bullet points )
    

#     YOUR ANSWER:
#     """
#     prompt = PromptTemplate.from_template(template)
#     chain = prompt | llm | StrOutputParser()

#     # 4. Invoke the LLM with the context and the user's question.
#     answer = chain.invoke({
#         "context": context_str,
#         "question": question
#     })

#     return answer