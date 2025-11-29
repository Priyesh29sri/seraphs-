"""
LLM Client with Gemini Support
Unified client for Google Gemini, Claude, and GPT-4
"""

import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LLMClient:
    """
    Unified LLM client supporting multiple providers.
    
    Providers:
    1. Google Gemini (Primary) - gemini-1.5-pro
    2. Anthropic Claude (Fallback) - claude-3-5-sonnet
    3. OpenAI GPT-4 (Fallback) - gpt-4-turbo
    """
    
    def __init__(self):
        self.primary_provider = os.getenv('LLM_PRIMARY_PROVIDER', 'gemini')
        self.primary_model = os.getenv('LLM_PRIMARY_MODEL', 'gemini-1.5-pro')
        self.temperature = float(os.getenv('LLM_TEMPERATURE', '0.1'))
        self.max_tokens = int(os.getenv('LLM_MAX_TOKENS', '8192'))
        
        # Initialize clients
        self._init_gemini()
        self._init_claude()
        self._init_openai()
        
        print(f"[LLM] Primary provider: {self.primary_provider}")
        print(f"[LLM] Primary model: {self.primary_model}")
    
    def _init_gemini(self):
        """Initialize Gemini client"""
        try:
            import google.generativeai as genai
            
            api_key = os.getenv('GOOGLE_API_KEY')
            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_client = genai
                self.has_gemini = True
                print(f"[LLM] ✓ Gemini configured")
            else:
                self.has_gemini = False
                print(f"[LLM] ✗ Gemini: No API key (set GOOGLE_API_KEY)")
        except ImportError:
            self.has_gemini = False
            print(f"[LLM] ✗ Gemini: Install with 'pip install google-generativeai'")
    
    def _init_claude(self):
        """Initialize Claude client"""
        try:
            import anthropic
            
            api_key = os.getenv('ANTHROPIC_API_KEY')
            if api_key:
                self.claude_client = anthropic.Anthropic(api_key=api_key)
                self.has_claude = True
                print(f"[LLM] ✓ Claude configured (fallback)")
            else:
                self.has_claude = False
                print(f"[LLM] ✗ Claude: No API key")
        except ImportError:
            self.has_claude = False
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            import openai
            
            api_key = os.getenv('OPENAI_API_KEY')
            if api_key:
                self.openai_client = openai.OpenAI(api_key=api_key)
                self.has_openai = True
                print(f"[LLM] ✓ OpenAI configured (fallback)")
            else:
                self.has_openai = False
        except ImportError:
            self.has_openai = False
    
    def call_gemini(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """
        Call Google Gemini API.
        
        Args:
            system_prompt: System instructions
            user_prompt: User message
            temperature: Override default temperature
            max_tokens: Override default max tokens
            
        Returns:
            {
                "content": str,
                "model": str,
                "tokens_used": {"input": int, "output": int},
                "cost": float
            }
        """
        if not self.has_gemini:
            raise Exception("Gemini not available")
        
        temp = temperature if temperature is not None else self.temperature
        max_tok = max_tokens if max_tokens is not None else self.max_tokens
        
        # Create model
        model = self.gemini_client.GenerativeModel(
            model_name=self.primary_model,
            generation_config={
                "temperature": temp,
                "max_output_tokens": max_tok,
            },
            system_instruction=system_prompt
        )
        
        # Generate response
        response = model.generate_content(user_prompt)
        
        # Extract text
        content = response.text
        
        # Calculate tokens and cost
        # Gemini pricing: $0.00125/1K input, $0.005/1K output for gemini-1.5-pro
        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count
        
        cost = (input_tokens / 1000 * 0.00125) + (output_tokens / 1000 * 0.005)
        
        return {
            "content": content,
            "model": self.primary_model,
            "tokens_used": {
                "input": input_tokens,
                "output": output_tokens
            },
            "cost": round(cost, 4)
        }
    
    def call_claude(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict:
        """Call Anthropic Claude API"""
        if not self.has_claude:
            raise Exception("Claude not available")
        
        temp = temperature if temperature is not None else self.temperature
        max_tok = max_tokens if max_tokens is not None else self.max_tokens
        
        response = self.claude_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tok,
            temperature=temp,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        content = response.content[0].text
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        
        # Claude pricing: $3/M input, $15/M output
        cost = (input_tokens / 1_000_000 * 3.0) + (output_tokens / 1_000_000 * 15.0)
        
        return {
            "content": content,
            "model": "claude-3-5-sonnet-20241022",
            "tokens_used": {"input": input_tokens, "output": output_tokens},
            "cost": round(cost, 4)
        }
    
    def call_with_fallback(
        self,
        system_prompt: str,
        user_prompt: str,
        **kwargs
    ) -> Dict:
        """
        Call LLM with automatic fallback.
        
        Tries: Primary → Claude → OpenAI → Simulated
        """
        # Try primary provider (Gemini)
        if self.primary_provider == 'gemini' and self.has_gemini:
            try:
                return self.call_gemini(system_prompt, user_prompt, **kwargs)
            except Exception as e:
                print(f"[LLM] Gemini failed: {e}, trying fallback...")
        
        # Try Claude fallback
        if self.has_claude:
            try:
                return self.call_claude(system_prompt, user_prompt, **kwargs)
            except Exception as e:
                print(f"[LLM] Claude failed: {e}, trying OpenAI...")
        
        # Try OpenAI fallback
        if self.has_openai:
            try:
                return self.call_openai(system_prompt, user_prompt, **kwargs)
            except Exception as e:
                print(f"[LLM] OpenAI failed: {e}, using simulation...")
        
        # Fallback to simulation
        print(f"[LLM] Using simulated responses (no API keys configured)")
        return self._simulate_response(system_prompt, user_prompt)
    
    def call_openai(self, system_prompt: str, user_prompt: str, **kwargs) -> Dict:
        """Call OpenAI GPT-4"""
        if not self.has_openai:
            raise Exception("OpenAI not available")
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=kwargs.get('temperature', self.temperature),
            max_tokens=kwargs.get('max_tokens', self.max_tokens)
        )
        
        return {
            "content": response.choices[0].message.content,
            "model": "gpt-4-turbo-preview",
            "tokens_used": {
                "input": response.usage.prompt_tokens,
                "output": response.usage.completion_tokens
            },
            "cost": 0.01  # Approximate
        }
    
    def _simulate_response(self, system_prompt: str, user_prompt: str) -> Dict:
        """Simulated response for demo/testing"""
        return {
            "content": '{"simulated": true, "message": "Using simulated LLM response"}',
            "model": "simulated",
            "tokens_used": {"input": 100, "output": 50},
            "cost": 0.0
        }


# Global singleton
_llm_client = None

def get_llm_client() -> LLMClient:
    """Get singleton LLM client"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
