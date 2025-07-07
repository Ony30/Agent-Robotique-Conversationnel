from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Lecture du contenu du fichier "madagascar_wikipedia.txt"
try:
    with open("context/madagascar_wikipedia.txt", "r", encoding="utf-8") as f:
        fixed_context = f.read()  # Chargement du contexte depuis le fichier
except FileNotFoundError:
    raise Exception("Le fichier 'madagascar_wikipedia.txt' n'a pas été trouvé")

# Initialisation du modèle CamemBERT
nlp = pipeline(
    "question-answering",
    model="etalab-ia/camembert-base-squadFR-fquad-piaf",
    tokenizer="etalab-ia/camembert-base-squadFR-fquad-piaf",
    device = 0
)

# Définition de l'application FastAPI
app = FastAPI()

# Schéma pour les requêtes de l'API (sans "context")
class QARequest(BaseModel):
    question: str

# Route pour le question-answering avec un contexte provenant du fichier
@app.post("/predict")
async def predict(request: QARequest):
    try:
        # Exécuter l'inférence avec le contexte chargé depuis le fichier
        result = nlp({
            "question": request.question,
            "context": fixed_context  # Utilisation du contexte chargé
        })
        return {"answer": result["answer"], "score": result["score"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur : {str(e)}")

