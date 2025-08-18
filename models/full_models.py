from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Literal
from fastapi import UploadFile, Form
import uuid

# --- Modèle de Requête pour l'endpoint 'full' ---
# Nous n'utilisons pas de BaseModel pour l'entrée 'multipart/form-data' de FastAPI.
# Les champs seront passés directement à la fonction de l'endpoint.
# Cependant, nous pouvons définir un modèle de base pour la documentation.
class FullRequestBaseModel(BaseModel):
    """
    Data model for the full profile recommendation query.
    Note: This model is used for documentation purposes. The endpoint directly uses Form and UploadFile.
    """
    # Modèle de données pour la requête de recommandation de profil complet.
    # Note : Ce modèle est utilisé pour la documentation. L'endpoint utilise directement Form et UploadFile.
    age: Optional[float] = Field(
        None,
        description="The age of the student in years. Optional.",
        # L'âge de l'étudiant en années. Facultatif.
        example=21.5
    )
    gender: Literal["male", "female", "other", "undefined"] = Field(
        "undefined",
        description="The gender of the student. Must be one of 'male', 'female', 'other', or 'undefined'. It is 'undefined' by default.",
        # Le sexe de l'étudiant. Doit être l'une des valeurs 'male', 'female', 'other' ou 'undefined'. Il est 'undefined' par défaut.
        example="female"
    )
    description: Optional[str] = Field(
        None,
        description="A free-text description of the student's profile. Either 'description' or 'file' must be provided.",
        # Une description libre du profil de l'étudiant. Soit 'description', soit 'file' doit être fourni.
        example="I'm a good listener but struggle with time management."
        # Je suis un bon auditeur mais j'ai du mal à gérer mon temps.
    )

# --- Modèles de Réponse pour l'endpoint 'full' ---
# Ces modèles de réponse combinent les structures des réponses individuelles.
class Goal(BaseModel):
    id: str = Field(..., example="a1b2c3d4-e5f6-7890-1234-567890abcdef")
    description: str = Field(..., example="Develop a weekly study schedule to improve time management.")

class Mean(BaseModel):
    id: str = Field(..., example="f5e4d3c2-b1a0-9876-5432-10fedcba9876")
    description: str = Field(..., example="Use the Pomodoro Technique to structure study sessions.")

class FullResponseData(BaseModel):
    """
    Data model for the data field of the full recommendation response.
    """
    # Modèle de données pour le champ 'data' de la réponse de recommandation complète.
    strengths: Optional[List[str]] = Field(None, example=["Strong teamwork skills", "Excellent listening skills"])
    challenges: Optional[List[str]] = Field(None, example=["Difficulty with time management", "Anxiety before exams"])
    needs: Optional[List[str]] = Field(None, example=["Personalized study plan", "Stress management techniques"])
    goals: Optional[List[Goal]] = Field(None, example=[{"id": "...", "description": "..."}])
    means: Optional[List[Mean]] = Field(None, example=[{"id": "...", "description": "..."}])

class FullResponse(BaseModel):
    """
    Data model for the full recommendation response.
    """
    # Modèle de données pour la réponse de recommandation complète.
    data: Optional[FullResponseData] = Field(
        None,
        description="All generated recommendations.",
        # Toutes les recommandations générées.
    )
    error: bool = Field(
        ...,
        description="Indicates if an internal error occurred (True) or not (False).",
        # Indique si une erreur interne est survenue (True) ou non (False).
        example=False
    )
    message: Optional[str] = Field(
        None,
        description="Detailed error message in case of a problem. This field is only present if 'error' is True.",
        # Message d'erreur détaillé en cas de problème. Ce champ est présent uniquement si 'error' est True.
        example=None
    )

    class Config:
        json_schema_extra = {
            "example": {
                "data": {
                    "strengths": ["Strong teamwork skills", "Excellent listening skills"],
                    "challenges": ["Difficulty with time management"],
                    "needs": ["Personalized study plan"],
                    "goals": [
                        {"id": "...", "description": "Develop a weekly study schedule to improve time management."}
                    ],
                    "means": [
                        {"id": "...", "description": "Use the Pomodoro Technique to structure study sessions."}
                    ]
                },
                "error": False,
                "message": None
            }
        }