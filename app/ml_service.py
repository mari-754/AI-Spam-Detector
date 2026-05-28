from transformers import pipeline
import logging
import os
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SpamDetector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        model_name = os.getenv("MODEL_NAME", "mrm8488/bert-tiny-finetuned-sms-spam-detection")
        try:
            logger.info(f"Loading model: {model_name}")
            # device=-1 means use CPU (important for college computers)
            self.classifier = pipeline("text-classification", model=model_name, device=-1)
            self.model_name = model_name
            logger.info("Model loaded successfully!")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise

    def predict(self, text: str) -> Dict[str, Any]:
        try:
            # Get prediction
            result = self.classifier(text)[0]

            # Convert labels to SPAM/NOT SPAM format
            label = result['label']
            score = result['score']

            # Handle different label formats from different models
            if label in ['LABEL_1', 'SPAM', 'spam', '1']:
                result_label = "SPAM"
            elif label in ['LABEL_0', 'NOT SPAM', 'not_spam', 'ham', '0']:
                result_label = "NOT SPAM"
            else:
                # Fallback: if it's already SPAM/NOT SPAM
                result_label = label.upper()

            logger.info(f"Prediction: {result_label} with confidence {score:.3f}")

            return {
                "result": result_label,
                "score": round(score, 3),
                "model_name": self.model_name
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise

# Create singleton instance
spam_detector = SpamDetector()
