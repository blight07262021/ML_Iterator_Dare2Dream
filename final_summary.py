from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine
import pandas as pd
from langchain_groq import ChatGroq
from langchain.schema import HumanMessage

app = FastAPI(
    title="User Feedback Summarization API",
    description="Generates hierarchical summaries of user feedback stored in a MySQL database using ChatGroq LLM.",
    version="1.0.0"
)

# ---------- FUNCTION ----------
def generate_hierarchical_summary(
    username: str,
    password: str,
    host: str,
    port: int,
    database: str,
    table_name: str,
    batch_size: int = 10,
    model_name: str = "llama-3.3-70b-versatile",
    temperature: float = 0.4
):
    """Generates a hierarchical (two-stage) summary of user feedback from MySQL."""
    connection_url = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_url)

    query = f"SELECT user_id, summary FROM {table_name};"
    df = pd.read_sql(query, engine)

    if df.empty:
        raise ValueError("No data found in the specified table.")

    print(f"Loaded {len(df)} rows of user feedback from {table_name}.")
    llm = ChatGroq(model=model_name, temperature=temperature)

    # --- Stage 1: Batch Summarization ---
    chunk_summaries = []
    for i in range(0, len(df), batch_size):
        batch = df.iloc[i:i + batch_size]
        feedback_list = "\n".join([f"User {row.user_id}: {row.summary}" for _, row in batch.iterrows()])

        prompt = f"""
        You are an AI analyst summarizing user feedback. Each line is from a different user.

        Your task:
        - Identify main themes or topics users mentioned.
        - Highlight unique or uncommon opinions explicitly.
        - Describe the overall sentiment (positive, negative, neutral proportions).

        Also include:
        - **Key Themes:** The main topics and ideas the user discussed.
        - **Core Motivations:** The underlying reasons for the user's preferences.
        - **Actionable Insights:** Specific takeaways a product manager could use.

        Feedbacks:
        {feedback_list}

        Return a structured batch summary.
        """

        response = llm.invoke([HumanMessage(content=prompt)])
        chunk_summary = response.content.strip()
        chunk_summaries.append(chunk_summary)

        print(f"Processed batch {i // batch_size + 1}/{(len(df) // batch_size) + 1}")

    # --- Stage 2: Global Summarization ---
    final_prompt = f"""
    You are an expert summarizer.
    Below are summaries of multiple batches of user feedback.

    Your task:
    - Combine all summaries into a single cohesive report.
    - Ensure proportional representation of all user sentiments and preferences.
    - Include both common and unique perspectives.

    Also include:
    - **Key Themes:** The main topics and ideas the user discussed.
    - **Core Motivations:** The underlying reasons for the user's preferences.
    - **Actionable Insights:** Specific takeaways a product manager could use.

    Batch Summaries:
    {chr(10).join(chunk_summaries)}

    Now generate a balanced final summary of overall user preferences and sentiment.
    """

    final_summary = llm.invoke([HumanMessage(content=final_prompt)]).content
    return final_summary


# ---------- API MODEL ----------
class SummaryRequest(BaseModel):
    username: str="root"
    password: str="1234567890"
    host: str = "localhost"
    port: int = 3306
    database: str="market_research"
    table_name: str="session_summary"
    batch_size: int = 10
    model_name: str = "llama-3.3-70b-versatile"
    temperature: float = 0.4


# ---------- API ROUTE ----------
@app.post("/generate_summary")
async def generate_summary(request: SummaryRequest):
    """API endpoint to generate hierarchical summary from MySQL feedback."""
    try:
        summary = generate_hierarchical_summary(
            username=request.username,
            password=request.password,
            host=request.host,
            port=request.port,
            database=request.database,
            table_name=request.table_name,
            batch_size=request.batch_size,
            model_name=request.model_name,
            temperature=request.temperature
        )
        return {"status": "success", "final_summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
