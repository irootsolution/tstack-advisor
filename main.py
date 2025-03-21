import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai

# Load API Key from .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

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
        
        # Initialize Gemini model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Generate response
        response = model.generate_content(prompt)
    
        return {"recommendation": response.text}
    except Exception as e:
        return {"error": str(e)}