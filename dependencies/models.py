from functools import lru_cache

import time

class FakeLegalModel:
    """
    Simulates ML model loading
    
    In real app, this would be:
    - model = torch.load("model.pth")
    - model = joblib.load("sklearn_model.pkl")
    - model = transformers.AutoModel.from_pretrained("...")
    """
    def __init__(self):
        print("Loading Legal AI Model... (this takes time!)")
        time.sleep(2)  # Simulate slow model loading
        print("Model loaded successfully!")
        self.model_version = "v1.2.3"
    
    def predict_category(self, text: str) -> tuple[str, float]:
        """Predict legal category"""
        text_lower = text.lower()
        
        if "property" in text_lower:
            return "Property Law", 0.89
        elif "contract" in text_lower:
            return "Contract Law", 0.85
        elif "family" in text_lower or "divorce" in text_lower:
            return "Family Law", 0.82
        else:
            return "General Law", 0.60
    
    def predict_crime(self, text: str) -> tuple[str, float]:
        """Predict crime type"""
        text_lower = text.lower()
        
        if "theft" in text_lower:
            return "IPC 379 - Theft", 0.92
        elif "assault" in text_lower:
            return "IPC 323 - Assault", 0.88
        elif "fraud" in text_lower:
            return "IPC 420 - Cheating", 0.85
        else:
            return "IPC General Section", 0.65


@lru_cache()  # IMPORTANT: Load model once, cache forever!
def get_legal_model() -> FakeLegalModel:
    """
    Get ML model instance
    
    WHY: Loading models is SLOW (takes seconds)
    HOW: @lru_cache loads once, reuses forever
    WHEN: First request loads model, subsequent requests use cached model
    
    In production, this saves HUGE amounts of time!
    """
    return FakeLegalModel()