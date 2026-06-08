from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import replicate
import os
from dotenv import load_dotenv
import json

# Učitaj API ključeve iz .env fajla
load_dotenv()

app = FastAPI(title="BrandCraft.ai API")

# CORS - dozvoli frontendu da priča sa backendom
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicijalizacija OpenAI klijenta (ako imaš ključ)
openai_client = None
if os.getenv("OPENAI_API_KEY"):
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Model za zahtev
class BrandRequest(BaseModel):
    prompt: str
    business_type: str = "general"

# Model za odgovor
class BrandResponse(BaseModel):
    logo_url: str
    colors: dict
    fonts: dict
    tagline: str

@app.get("/")
def root():
    return {"message": "BrandCraft.ai API is running!", "status": "ok"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/generate")
async def generate_brand(request: BrandRequest):
    # Ako nema OpenAI ključa, vrati demo podatke
    if not openai_client:
        return BrandResponse(
            logo_url="https://placehold.co/512x512/667eea/white?text=Logo",
            colors={
                "primary": "#667eea",
                "secondary": "#764ba2", 
                "accent": "#f093fb",
                "light": "#f8f9fa",
                "dark": "#343a40"
            },
            fonts={
                "heading": "Poppins",
                "body": "Open Sans"
            },
            tagline="Your vibe, your brand"
        )
    
    try:
        # 1. OpenAI generiše strategiju
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """You are a brand strategist. Generate JSON with:
                    - colors: primary, secondary, accent, light, dark (hex codes)
                    - fonts: heading, body (Google Font names)
                    - tagline: catchy 5-8 word tagline
                    Only respond with valid JSON."""
                },
                {
                    "role": "user",
                    "content": f"Brand vibe: {request.prompt}"
                }
            ],
            response_format={"type": "json_object"}
        )
        
        strategy = json.loads(response.choices[0].message.content)
        
        # 2. Generiši logo (placeholder za sad)
        logo_url = "https://placehold.co/512x512/667eea/white?text=AI+Logo"
        
        return BrandResponse(
            logo_url=logo_url,
            colors=strategy.get("colors", {}),
            fonts=strategy.get("fonts", {}),
            tagline=strategy.get("tagline", "Your vibe, your brand")
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return BrandResponse(
            logo_url="https://placehold.co/512x512/667eea/white?text=Logo",
            colors={
                "primary": "#667eea",
                "secondary": "#764ba2",
                "accent": "#f093fb", 
                "light": "#f8f9fa",
                "dark": "#343a40"
            },
            fonts={
                "heading": "Poppins",
                "body": "Open Sans"
            },
            tagline="Your vibe, your brand"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)