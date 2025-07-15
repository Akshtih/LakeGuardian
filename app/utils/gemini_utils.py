import os
import requests
import json
from flask import current_app
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_gemini():
    """Initialize the Gemini API. This is a placeholder function for compatibility."""
    logger.info("Initializing Gemini API (placeholder)")
    pass

def get_lake_chatbot_response(question):
    """Get a response from Gemini about lake pollution and conservation."""
    try:
        # Get API key from config
        api_key = current_app.config.get('GEMINI_API_KEY')
        if not api_key:
            return "Error: Gemini API key not configured. Please set the GEMINI_API_KEY in your environment variables."
            
        # Try different API endpoints in order
        endpoints = [
            # Version 1beta with gemini-pro model
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            # Version 1beta with gemini-1.0-pro model
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.0-pro:generateContent",
            # Version 1 with gemini-1.5-pro model
            "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"
        ]
        
        # Create a prompt with context about lake conservation
        prompt = f"""
        You are a lake conservation expert specialized in helping college students understand 
        and combat pollution in lakes and water bodies. You have specific knowledge about:
        
        - Types of common pollutants in lakes (plastics, chemicals, organic waste)
        - Environmental impact of different types of waste
        - Simple, practical conservation methods for students
        - How to organize effective cleanups
        - The ecosystem of freshwater lakes
        
        Answer the following question about lake conservation:
        
        {question}
        
        Make your answer concise (under 250 words), practical, and actionable for college students.
        Include 1-2 specific tips that are easy to implement.
        """
        
        # Prepare the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 800,
            }
        }
        
        # Try each endpoint until one works
        for endpoint in endpoints:
            try:
                url = f"{endpoint}?key={api_key}"
                logger.info(f"Trying endpoint: {endpoint.split('/models/')[0]}/models/[REDACTED]")
                
                # Make the API request
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, json=payload, headers=headers, timeout=10)
                
                # Check if request was successful
                if response.status_code == 200:
                    data = response.json()
                    if "candidates" in data and len(data["candidates"]) > 0:
                        if "content" in data["candidates"][0]:
                            content = data["candidates"][0]["content"]
                            if "parts" in content and len(content["parts"]) > 0:
                                return content["parts"][0]["text"]
                else:
                    logger.error(f"API Error with endpoint {endpoint}: {response.status_code} - {response.text}")
            except Exception as e:
                logger.error(f"Exception with endpoint {endpoint}: {str(e)}")
                continue
        
        # If all API calls fail, use the fallback responses
        return get_custom_response(question)
            
    except Exception as e:
        logger.error(f"Error with Gemini API: {str(e)}")
        return get_custom_response(question)

def get_custom_response(question):
    """
    Instead of predetermined answers, use a rule-based system 
    to dynamically generate responses based on keywords in the question.
    """
    question_lower = question.lower()
    
    # Extract keywords from question
    keywords = []
    important_words = ["plastic", "pollution", "waste", "cleanup", "organize", "student", 
                      "help", "protect", "conservation", "ecosystem", "decompose", 
                      "harmful", "impact", "water", "lake", "river", "fish"]
    
    for word in important_words:
        if word in question_lower:
            keywords.append(word)
    
    # Default response if no specific keywords found
    if not keywords:
        return f"""
I'm currently having trouble connecting to my knowledge base to give you a specific answer about "{question}".

Here are some general lake conservation tips:

1. Reduce your use of single-use plastics, especially near water bodies
2. Participate in or organize local lake cleanup events
3. Be mindful of what goes down drains, as many pollutants eventually reach lakes
4. Learn about native plants that help filter runoff and consider planting them near waterways
5. Consider joining a local conservation group to amplify your impact

Is there a specific aspect of lake conservation you'd like to focus on?
"""
    
    # Dynamically build a response based on keywords
    response_parts = [f"Regarding your question about {', '.join(keywords)}:"]
    
    if "plastic" in keywords:
        response_parts.append("""
Plastics are particularly harmful to lake ecosystems. When they break down into microplastics, they:
- Are ingested by fish and other aquatic life
- Can accumulate in the food chain
- May release harmful chemicals as they degrade

TIP: Replace single-use plastic items with reusable alternatives like steel water bottles and fabric shopping bags.
""")
    
    if "pollution" in keywords or "harmful" in keywords:
        response_parts.append("""
The most concerning lake pollutants include:
- Agricultural runoff (fertilizers and pesticides)
- Industrial chemicals
- Microplastics
- Sewage and household chemicals

These can cause algal blooms, reduced oxygen levels, and harm to wildlife.

TIP: Use eco-friendly cleaning and personal care products that won't harm aquatic life when they eventually reach waterways.
""")
    
    if "cleanup" in keywords or "organize" in keywords:
        response_parts.append("""
For effective lake cleanups:
1. Partner with local environmental organizations
2. Gather proper equipment: gloves, bags, grabbers
3. Create teams for different areas
4. Track the types and amounts of waste collected
5. Properly dispose of or recycle the collected materials

TIP: Create a recurring event (monthly or quarterly) rather than a one-time cleanup for lasting impact.
""")
    
    if "student" in keywords or "help" in keywords:
        response_parts.append("""
As a student, you can:
1. Form a campus environmental club focused on water conservation
2. Partner with science departments for water quality testing
3. Create educational campaigns about daily habits that impact water quality
4. Volunteer with local conservation organizations
5. Organize lake cleanups with fellow students

TIP: Start with a small, visible project like adopting a campus pond and work toward larger initiatives as you gain support.
""")
    
    if "decompose" in keywords:
        response_parts.append("""
Decomposition times in aquatic environments:
- Plastic bottles: 450+ years
- Fishing line: 600 years
- Aluminum cans: 200+ years
- Plastic bags: 10-20 years
- Apple core/fruit: 1-2 months
- Paper: 2-4 weeks (though chemicals in paper can persist longer)

TIP: Remember that "biodegradable" doesn't always mean safe for water - even biodegradable items can release harmful substances as they break down.
""")
    
    if "ecosystem" in keywords or "fish" in keywords:
        response_parts.append("""
Lake ecosystems are delicate interconnected webs where:
- Aquatic plants produce oxygen and provide habitat
- Fish and other organisms maintain balance
- Microorganisms break down waste
- Shoreline vegetation filters pollutants

When pollution disrupts any part of this system, it affects everything else.

TIP: Learn to identify invasive species in your area and report sightings to local environmental agencies.
""")
    
    # Return the combined response
    return "\n".join(response_parts)