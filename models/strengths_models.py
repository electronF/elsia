from pydantic import BaseModel, Field
from typing import Optional

class StrengthsRequest(BaseModel):
    """
    Data model for the student strengths analysis query.
    """
    age: Optional[float] = Field(
        None, 
        description="The age of the student in years. This field is optional and can be omitted. The value must be a number.",#L'âge de l'étudiant en années. Ce champ est facultatif et peut être omis. La valeur doit être un nombre.
        example=21.5
    )
    description: str = Field(
        ...,
        description="A free description of the student's strengths. This field is mandatory and must be a non-empty string.",#Une description libre des points forts de l'étudiant. Ce champ est obligatoire et doit être une chaîne de caractères non vide.
        example="He enjoys working in a team, is a good listener and is creative."#Il aime bien travailler en équipe, il a une grande capacité d'écoute et il est créatif.
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 21.5,
                "description": "He enjoys working in a team, is a good listener and is creative."
            }
        }

class StrengthsResponse(BaseModel):
    """
    Data model for force recommendation response.
    """#Modèle de données pour la réponse de recommandation des forces.
    
    data: Optional[list[str]] = Field(
        None,
        description="A list of phrases describing the recommended strengths. This field is present in case of success.",#Une liste de phrases décrivant les forces recommandées. Ce champ est présent en cas de succès.
        example=["Good collaboration with classmates", "Excellent listening skills when listening to others and during lessons", "Creative thinking during practical exercises"] #["Bonne collaboration avec ses camarades", "Excellente écoute des autres et des cours", "Pensée créative durant les exercices pratique"]
    )
    error: bool = Field(
        ..., 
        description="Indicates whether an internal error occurred (True) or not (False).",#Indique si une erreur interne est survenue (True) ou non (False).
        example=False
    )
    message: Optional[str] = Field(
        None, 
        description="Detailed error message in case of a problem. This field is only present if 'error' is True.",#Message d'erreur détaillé en cas de problème. Ce champ est présent uniquement si 'error' est True.
        example=None
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "data": ["Good collaboration with classmates", "Excellent listening skills when listening to others and during lessons", "Creative thinking during practical exercises"],
                "error": False,
                "message": None
            }
        }