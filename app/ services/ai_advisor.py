import google.generativeai as genai
from app.core.config import settings

# Configure Gemini with your API Key
genai.configure(api_key=settings.GEMINI_API_KEY)

class AIAdvisorService:
    def __init__(self):
        # We use 'flash' for speed and cost-efficiency
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.system_prompt = (
            "You are WikiKisan AI, an expert agricultural advisor. "
            "Your goal is to provide accurate, sustainable, and practical farming advice "
            "to Indian farmers. Focus on crop health, soil quality, and pest management. "
            "If a query is not related to farming, politely decline to answer."
        )

    async def get_farming_advice(self, user_query: str, context: dict = None) -> str:
        """
        Generates AI advice. Context can include weather or market data.
        """
        full_prompt = f"{self.system_prompt}\n\n"
        
        if context:
            full_prompt += f"Context: Current Weather is {context.get('weather')}. "
            full_prompt += f"Market Price is {context.get('price')}.\n"
            
        full_prompt += f"Farmer Question: {user_query}"

        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"I'm sorry, I'm having trouble connecting to my knowledge base. Error: {str(e)}"

# Global instance
ai_advisor = AIAdvisorService()
