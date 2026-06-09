from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv
import json
import random

# Učitaj API ključeve iz .env fajla (ako ih budeš koristila)
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

# Funkcije za generisanje boja na osnovu prompta
def generate_colors_from_prompt(prompt: str):
    lower_prompt = prompt.lower()
    
    if 'industrial' in lower_prompt or 'brick' in lower_prompt:
        return {
            "primary": "#C41E3A",
            "secondary": "#2C2C2C",
            "accent": "#D4AF37",
            "light": "#F5F5F5",
            "dark": "#1A1A1A"
        }
    elif 'modern' in lower_prompt or 'minimal' in lower_prompt or 'tech' in lower_prompt:
        return {
            "primary": "#2D2D2D",
            "secondary": "#F5F5F5",
            "accent": "#00C2A0",
            "light": "#FFFFFF",
            "dark": "#000000"
        }
    elif 'vintage' in lower_prompt or 'rustic' in lower_prompt or 'book' in lower_prompt:
        return {
            "primary": "#8B4513",
            "secondary": "#F4ECD8",
            "accent": "#CD853F",
            "light": "#FFF8F0",
            "dark": "#3E2723"
        }
    elif 'cozy' in lower_prompt or 'warm' in lower_prompt or 'cafe' in lower_prompt:
        return {
            "primary": "#D2691E",
            "secondary": "#FFE4B5",
            "accent": "#FF6347",
            "light": "#FFF5EE",
            "dark": "#5C4033"
        }
    elif 'bold' in lower_prompt or 'energetic' in lower_prompt:
        return {
            "primary": "#FF4757",
            "secondary": "#2ED573",
            "accent": "#FFA502",
            "light": "#F1F2F6",
            "dark": "#2F3542"
        }
    else:
        return {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "accent": "#f093fb",
            "light": "#f8f9fa",
            "dark": "#343a40"
        }

# Funkcije za generisanje fontova
def generate_fonts_from_prompt(prompt: str):
    lower_prompt = prompt.lower()
    
    if 'modern' in lower_prompt or 'tech' in lower_prompt:
        return {
            "heading": "Inter",
            "body": "Inter"
        }
    elif 'vintage' in lower_prompt or 'book' in lower_prompt:
        return {
            "heading": "Playfair Display",
            "body": "Lora"
        }
    else:
        return {
            "heading": "Poppins",
            "body": "Open Sans"
        }

# Funkcija za generisanje tagline-a
def generate_tagline_from_prompt(prompt: str):
    lower_prompt = prompt.lower()
    
    if 'coffee' in lower_prompt:
        return "Fresh coffee, great vibes"
    elif 'tech' in lower_prompt:
        return "Innovation meets design"
    elif 'book' in lower_prompt:
        return "Stories that matter"
    else:
        return "Your vibe, your brand"

# Funkcija za generisanje logoa preko Pollinations.ai (besplatno!)
async def generate_logo_with_pollinations(prompt: str) -> str:
    try:
        # Kreiraj URL za Pollinations.ai
        logo_prompt = f"Professional logo for {prompt}, minimalist, clean, vector style, simple, modern, no text"
        encoded_prompt = logo_prompt.replace(" ", "%20")
        logo_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=512&height=512"
        
        # Proveri da li URL radi
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.head(logo_url)
            if response.status_code == 200:
                return logo_url
            else:
                return "https://placehold.co/512x512/667eea/white?text=Logo"
    except Exception as e:
        print(f"Logo generation error: {e}")
        return "https://placehold.co/512x512/667eea/white?text=Logo"

@app.get("/")
def root():
    return {"message": "BrandCraft.ai API is running!", "status": "ok"}

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/generate")
async def generate_brand(request: BrandRequest):
    try:
        # 1. Generiši boje na osnovu prompta
        colors = generate_colors_from_prompt(request.prompt)
        
        # 2. Generiši fontove
        fonts = generate_fonts_from_prompt(request.prompt)
        
        # 3. Generiši tagline
        tagline = generate_tagline_from_prompt(request.prompt)
        
        # 4. Generiši logo preko Pollinations.ai
        logo_url = await generate_logo_with_pollinations(request.prompt)
        
        return BrandResponse(
            logo_url=logo_url,
            colors=colors,
            fonts=fonts,
            tagline=tagline
        )
        
    except Exception as e:
        print(f"Error: {e}")
        # U slučaju greške, vrati placeholder
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