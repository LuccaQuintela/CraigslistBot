import os
import yaml
import json
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
from openai import OpenAI
from utilities.config import Config

class LLMClient:
    """
    Base class for LLM clients that provides core functionality for interacting with OpenAI's API.
    Handles initialization, system prompts, and basic message sending.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model: str = None, 
                 **kwargs):
        """
        Initialize the LLM client.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable OPENAI_API_KEY
            model: The model to use for completions
            **kwargs: Additional arguments to pass to OpenAI client
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("API key must be provided either as parameter or OPENAI_API_KEY environment variable")
        
        self.model = model or Config.get('model')
        self.client = OpenAI(api_key=self.api_key, **kwargs)
        self.system_prompt = ""
        self.conversation_history: List[Dict[str, str]] = []
        
    def _set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt for the conversation."""
        self.system_prompt = prompt

    def _read_from_file(self, file_path:str, **kwargs):
        """Reads from a file and any kwargs are injected into the text like an fstring"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if kwargs:
                    content = content.format(**kwargs)
                return content.strip()
                
        except FileNotFoundError:
            raise FileNotFoundError(f"System prompt file not found: {file_path}")
    
    def _load_system_prompt_from_file(self, file_path: Optional[str] = None) -> None:
        """Load system prompt from a text file."""
        if file_path is None:
            file_path = Path(__file__).parent / "prompts/system.txt"

        system = self._read_from_file(file_path)
        self._set_system_prompt(system)
    
    def _add_message(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        if role not in ["user", "assistant", "system"]:
            raise ValueError("Role must be 'user', 'assistant', or 'system'")
        
        self.conversation_history.append({"role": role, "content": content})
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
    
    def send_message(self, 
                     message: str, 
                     role: str = "user", 
                     temperature: float = None, 
                     max_tokens: int = None, 
                     **kwargs) -> str:
        """
        Send a message to the LLM.
        
        Args:
            message: The message content to send
            role: The role of the message (default = "user")
            temperature: Sampling temperature (0-2) (default = 0.7)
            max_tokens: Maximum tokens in response (default = 1000)
            **kwargs: Additional parameters for the API call
            
        Returns:
            The response content from the LLM
        """
        self._add_message(role, message)
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        
        messages.extend(self.conversation_history)
        
        temperature = temperature or Config.get('temperature')
        max_tokens = max_tokens or Config.get('max_tokens')

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            
            response_content = response.choices[0].message.content
            self._add_message("assistant", response_content)
            return response_content
            
        except Exception as e:
            raise RuntimeError(f"Error calling OpenAI API: {str(e)}")

class ListingEvaluatorLLMClient(LLMClient):
    """
    Specialized LLM client for evaluating Craigslist listings.
    Inherits from LLMClient and adds specific functionality for listing evaluation.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 model: str = "gpt-3.5-turbo", 
                 **kwargs):
        """
        Initialize the Listing Evaluator LLM Client.
        
        Args:
            api_key: OpenAI API key. If None, will try to get from environment variable OPENAI_API_KEY
            model: The model to use for completions
            **kwargs: Additional arguments to pass to OpenAI client
        """
        super().__init__(api_key, model, **kwargs)
        self._load_system_prompt_from_file()
    
    def evaluate_listings(self, listings: List[Dict[str, Any]]) -> List[tuple]:
        """
        Evaluate a Craigslist listing.
        
        Args:
            listing_data: Dictionary containing listing information (title, price, description, etc.)
            
        Returns:
            Detailed evaluation of the listing
        """
        formatted_listings = self._format_listings(listings)
        file_path = file_path = Path(__file__).parent / "prompts/evaluation.txt"

        evaluation_prompt = self._read_from_file(
            file_path = file_path,
            search_query = Config.get('search_query'),
            search_details = Config.get('search_details'),
            length = len(listings),
            formatted_listings = formatted_listings,
        )
        response = self.send_message(evaluation_prompt)
        self.clear_history

        try:
            scores = json.loads(response)
            results = [(score, listing["url"]) for score, listing in zip(scores, listings)]
            return results
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Couldn't load LLM evaluation scores into list with JSON: {e}\nresponse: {response}")
    
    def _format_listing(self, listing_data: Dict[str, Any]) -> str:
        """Format listing data into a readable string for evaluation."""
        formatted = []
        
        for key, value in listing_data.items():
            formatted.append(f"{key.title()}: {value}")
        
        return "\n".join(formatted)
    
    def _format_listings(self, listings: List[Dict[str, Any]]) -> str:
        formatted = []

        for index, listing in enumerate(listings):
            listing_string = f"Listing {index + 1}\n" + self._format_listing(listing)
            formatted.append(listing_string)

        return "\n\n".join(formatted)
            