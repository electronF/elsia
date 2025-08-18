from pydantic import BaseModel, Field
from typing import Optional

class ChallengesRequest(BaseModel):
    """
    Data model for the student challenges analysis query.
    """
    # Modèle de données pour la requête d'analyse des défis de l'étudiant.
    age: Optional[float] = Field(
        None, 
        description="The age of the student in years. This field is optional and can be omitted. The value must be a number.",
        # L'âge de l'étudiant en années. Ce champ est facultatif et peut être omis. La valeur doit être un nombre.
        example=21.5
    )
    description: str = Field(
        ...,
        description="A free description of the student's challenges. This field is mandatory and must be a non-empty string.",
        # Une description libre des défis de l'étudiant. Ce champ est obligatoire et doit être une chaîne de caractères non vide.
        example="He has trouble managing his time and feels stressed before exams."
        # Il a du mal à gérer son temps et il se sens stressé avant les examens.
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 21.5,
                "description": "He has trouble managing his time and feels stressed before exams."
            }
        }

class ChallengesResponse(BaseModel):
    """
    Data model for challenges recommendation response.
    """
    # Modèle de données pour la réponse de recommandation des défis.
    data: Optional[list[str]] = Field(
        None,
        description="A list of phrases describing the recommended challenges. This field is present in case of success.",
        # Une liste de phrases décrivant les défis recommandés. Ce champ est présent en cas de succès.
        example=["Difficulty with time management", "Anxiety and stress before exams", "Lack of effective study methods"]
        # Difficulté avec la gestion du temps, Anxiété et stress avant les examens, Manque de méthodes d'étude efficaces
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
                "data": ["Difficulty with time management", "Anxiety and stress before exams"],
                "error": False,
                "message": None
            }
        }
