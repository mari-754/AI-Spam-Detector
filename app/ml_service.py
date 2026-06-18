# ml_service.py
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import torch

# --- Инициализация модели (глобально, при старте приложения) ---
MODEL_NAME = "AventIQ-AI/distilbert-spam-detector"
model = None
tokenizer = None

def load_model():
    """Загружает модель и токенизатор (вызывается один раз при старте)."""
    global model, tokenizer
    if model is None:
        print("Загрузка модели DistilBERT для определения спама...")
        # Загружаем модель и токенизатор с Hugging Face
        model = DistilBertForSequenceClassification.from_pretrained(MODEL_NAME)
        tokenizer = DistilBertTokenizerFast.from_pretrained(MODEL_NAME)
        # Переводим в режим оценки и в половину точности (fp16) для ускорения
        model.eval()
        model.half()
        print("Модель успешно загружена.")
    return model, tokenizer

def predict_spam(text: str) -> str:
    """
    Определяет, является ли текст спамом.
    Возвращает "Spam" или "Not Spam".
    """
    model, tokenizer = load_model()
    
    # Токенизируем входной текст
    inputs = tokenizer(
        text, 
        return_tensors="pt", 
        truncation=True, 
        padding=True, 
        max_length=128
    )
    
    # Делаем предсказание
    with torch.no_grad():
        outputs = model(**inputs)
        predicted_class = torch.argmax(outputs.logits, dim=1).item()
    
    label_map = {0: "Not Spam", 1: "Spam"}
    return label_map[predicted_class]

# --- Пример функции, которая может быть в вашем существующем файле ---
# Если у вас уже были функции для работы со спамом, вы можете их переписать,
# используя новую функцию predict_spam. Например:

# def analyze_message(message_text: str):
#     prediction = predict_spam(message_text)
#     # ... ваша логика сохранения результата в БД и т.д. ...
#     return {"message": message_text, "prediction": prediction}
