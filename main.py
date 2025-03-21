import os
import openai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load API Key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Request body model
class TechQuery(BaseModel):
    project_type: str
    scalability_needs: str
    budget: str

@app.post("/recommend")
async def recommend_tech_stack(query: TechQuery):
    try:
        prompt = f"""
        Recommend a backend framework, database, and cloud service for a project.
        - Project Type: {query.project_type}
        - Scalability Needs: {query.scalability_needs}
        - Budget: {query.budget}

        Provide a brief reason for each choice.
        """
        client = openai.OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a software architect helping users choose tech stacks."},
                    {"role": "user", "content": prompt}]
        )
    
        return {"recommendation": response["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}