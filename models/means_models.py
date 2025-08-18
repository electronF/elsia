from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, Literal
import uuid

class MeansRequest(BaseModel):
    """
    Data model for the student means recommendation query.
    """
    # Modèle de données pour la requête de recommandation de moyens pour l'étudiant.
    age: Optional[float] = Field(
        None, 
        description="The age of the student in years. This field is optional and can be omitted. The value must be a number.",
        # L'âge de l'étudiant en années. Ce champ est facultatif et peut être omis. La valeur doit être un nombre.
        example=21.5
    )
    gender: Literal["male", "female", "other", "undefined"] = Field(
        "undefined",
        description="The gender of the student. Must be one of 'male', 'female', 'other', or 'undefined'. It is set to 'undefined' by default.",
        # Le sexe de l'étudiant. Doit être l'une des valeurs 'male', 'female', 'other' ou 'undefined'. Il est 'undefined' par défaut.
        example="female"
    )
    strengths: Optional[List[str]] = Field(
        None,
        description="A list of the student's strengths. This field is optional.",
        # Une liste des forces de l'étudiant. Ce champ est facultatif.
        example=["Strong teamwork skills", "Excellent listening skills"]
    )
    challenges: Optional[List[str]] = Field(
        None,
        description="A list of the student's challenges. This field is optional.",
        # Une liste des défis de l'étudiant. Ce champ est facultatif.
        example=["Difficulty with time management", "Anxiety before exams"]
    )
    needs: Optional[List[str]] = Field(
        None,
        description="A list of the student's needs. This field is optional.",
        # Une liste des besoins de l'étudiant. Ce champ est facultatif.
        example=["Personalized study plan", "Stress management techniques"]
    )
    goals: List[str] = Field(
        ...,
        description="A list of the student's goals for which means are to be recommended. This field is mandatory.",
        # Une liste des objectifs de l'étudiant pour lesquels des moyens doivent être recommandés. Ce champ est obligatoire.
        example=["Develop a weekly study schedule", "Learn relaxation techniques"]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 21.5,
                "gender": "female",
                "strengths": ["Strong teamwork skills"],
                "challenges": ["Difficulty with time management"],
                "needs": ["Personalized study plan"],
                "goals": ["Develop a weekly study schedule"]
            }
        }

class Mean(BaseModel):
    """
    Data model for a single recommended mean.
    """
    # Modèle de données pour un moyen recommandé unique.
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the mean.",
        # Identifiant unique du moyen.
        example="a1b2c3d4-e5f6-7890-1234-567890abcdef"
    )
    description: str = Field(
        ...,
        description="The description of the recommended mean.",
        # La description du moyen recommandé.
        example="Use the Pomodoro Technique to structure study sessions."
        # Utiliser la Technique Pomodoro pour structurer les sessions d'étude.
    )

class MeansResponse(BaseModel):
    """
    Data model for means recommendation response.
    """
    # Modèle de données pour la réponse de recommandation des moyens.
    data: Optional[List[Mean]] = Field(
        None,
        description="A list of recommended means. This field is present in case of success.",
        # Une liste de moyens recommandés. Ce champ est présent en cas de succès.
        example=[
            {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "description": "Use the Pomodoro Technique to structure study sessions."},
            {"id": "f5e4d3c2-b1a0-9876-5432-10fedcba9876", "description": "Practice deep breathing exercises before a test."}
        ]
    )
    error: bool = Field(
        ..., 
        description="Indicates whether an internal error occurred (True) or not (False).",
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
                "data": [
                    {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "description": "Use the Pomodoro Technique to structure study sessions."},
                    {"id": "f5e4d3c2-b1a0-9876-5432-10fedcba9876", "description": "Practice deep breathing exercises before a test."}
                ],
                "error": False,
                "message": None
            }
        }