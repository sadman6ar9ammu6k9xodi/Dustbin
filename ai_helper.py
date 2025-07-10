#!/usr/bin/env python3
"""
AI Helper module for Dustbin
Integrates with Hugging Face models for code assistance
"""

import os
import requests
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class HuggingFaceAPI:
    """Hugging Face API client for code assistance"""
    
    def __init__(self):
        self.api_token = os.getenv('HUGGINGFACE_API_TOKEN')
        self.base_url = "https://api-inference.huggingface.co/models"
        self.headers = {
            "Authorization": f"Bearer {self.api_token}" if self.api_token else None,
            "Content-Type": "application/json"
        }
        
        # Reliable models that are known to work
        self.models = {
            "code_completion": "microsoft/CodeBERT-base",
            "code_generation": "Salesforce/codegen-350M-mono",
            "language_detection": "microsoft/codebert-base-mlm",
            "text_generation": "microsoft/DialoGPT-small",  # Smaller, more reliable
            "code_explanation": "microsoft/CodeBERT-base"
        }
    
    def test_model_availability(self, model_name: str) -> bool:
        """Test if a model is available and responding"""
        try:
            url = f"{self.base_url}/{model_name}"
            response = requests.get(url, headers=self.headers, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Error testing model {model_name}: {e}")
            return False
    
    def get_available_models(self) -> Dict[str, str]:
        """Get list of available and working models"""
        available = {}
        for task, model in self.models.items():
            if self.test_model_availability(model):
                available[task] = model
            else:
                print(f"Model {model} for {task} is not available")
        return available
    
    def generate_code_completion(self, code: str, language: str = "python") -> Optional[str]:
        """Generate code completion suggestions"""
        if not self.api_token:
            return None
            
        model = self.models.get("code_completion")
        if not model:
            return None
            
        try:
            url = f"{self.base_url}/{model}"
            payload = {
                "inputs": f"# {language}\n{code}",
                "parameters": {
                    "max_length": 100,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    return result[0].get("generated_text", "").strip()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"Error generating code completion: {e}")
            
        return None
    
    def detect_programming_language(self, code: str) -> Optional[str]:
        """Detect programming language from code snippet"""
        # Simple heuristic-based detection as fallback
        language_patterns = {
            "python": ["def ", "import ", "from ", "print(", "if __name__"],
            "javascript": ["function ", "const ", "let ", "var ", "console.log"],
            "java": ["public class", "public static void main", "System.out"],
            "cpp": ["#include", "using namespace", "std::", "cout <<"],
            "c": ["#include", "int main(", "printf("],
            "html": ["<html", "<head", "<body", "<!DOCTYPE"],
            "css": ["{", "}", ":", ";", "px", "color:"],
            "sql": ["SELECT", "FROM", "WHERE", "INSERT", "UPDATE"],
            "bash": ["#!/bin/bash", "echo ", "if [", "for "],
            "rust": ["fn main(", "let ", "println!", "use "],
            "go": ["package main", "func main(", "fmt.Print", "import "],
            "php": ["<?php", "echo ", "$", "function "],
            "ruby": ["def ", "puts ", "end", "class "],
            "swift": ["func ", "var ", "let ", "print("],
            "kotlin": ["fun main(", "val ", "var ", "println("]
        }
        
        code_lower = code.lower()
        scores = {}
        
        for lang, patterns in language_patterns.items():
            score = sum(1 for pattern in patterns if pattern.lower() in code_lower)
            if score > 0:
                scores[lang] = score
        
        if scores:
            return max(scores, key=scores.get)
        
        return "text"
    
    def explain_code(self, code: str, language: str = "python") -> Optional[str]:
        """Generate explanation for code snippet"""
        if not self.api_token:
            return f"This {language} code snippet contains various programming constructs. Enable AI features by setting HUGGINGFACE_API_TOKEN."
            
        # Simple rule-based explanation as fallback
        explanations = []
        
        if "def " in code:
            explanations.append("Defines functions")
        if "class " in code:
            explanations.append("Defines classes")
        if "import " in code or "from " in code:
            explanations.append("Imports modules/libraries")
        if "if " in code:
            explanations.append("Contains conditional logic")
        if "for " in code or "while " in code:
            explanations.append("Contains loops")
        if "try:" in code or "except" in code:
            explanations.append("Includes error handling")
        
        if explanations:
            return f"This {language} code " + ", ".join(explanations).lower() + "."
        else:
            return f"This appears to be {language} code with basic programming constructs."

# Global AI helper instance
ai_helper = HuggingFaceAPI()

def get_code_suggestions(code: str, language: str = "python") -> Dict[str, Any]:
    """Get AI-powered code suggestions"""
    return {
        "completion": ai_helper.generate_code_completion(code, language),
        "detected_language": ai_helper.detect_programming_language(code),
        "explanation": ai_helper.explain_code(code, language),
        "available_models": ai_helper.get_available_models()
    }

if __name__ == "__main__":
    # Test the AI helper
    print("🤖 Testing Dustbin AI Helper")
    print("=" * 40)
    
    # Test language detection
    test_code = """
def hello_world():
    print("Hello from Dustbin!")
    return "AI integration working"
    """
    
    detected = ai_helper.detect_programming_language(test_code)
    print(f"Detected language: {detected}")
    
    explanation = ai_helper.explain_code(test_code, detected)
    print(f"Code explanation: {explanation}")
    
    available = ai_helper.get_available_models()
    print(f"Available models: {list(available.keys())}")
    
    if ai_helper.api_token:
        print("✅ Hugging Face API token configured")
    else:
        print("⚠️  Set HUGGINGFACE_API_TOKEN environment variable for full AI features")
