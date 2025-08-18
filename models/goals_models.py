from pydantic import BaseModel, Field, conlist, constr, ValidationError, model_validator
from typing import Optional, List, Literal

import uuid

class GoalsRequest(BaseModel):
    """
    Data model for the student goals analysis query.
    """
    # Modèle de données pour la requête d'analyse des objectifs de l'étudiant.
    age: Optional[float] = Field(
        None, 
        description="The student's age in years. This field is optional.",
        # L'âge de l'étudiant en années. Ce champ est facultatif.
        example=21.5
    )
    
    # constr(pattern=r"^(male|female|other|undefined)$")
    gender: Literal["male", "female", "other", "undefined"]  = Field(
        "undefined", 
        description="The student's gender. Must be one of: 'male', 'female', 'other', or 'undefined'.",
        # Le sexe de l'étudiant. Doit être l'un des suivants : 'male', 'female', 'other', ou 'undefined'.
        example="female"
    )
    strengths: Optional[List[str]] = Field(
        None,
        description="A list of the student's strengths. This field is optional.",
        # Une liste des forces de l'étudiant. Ce champ est facultatif.
        example=["Strong teamwork skills", "Excellent listening skills", "Creative problem-solving"]
    )
    challenges: Optional[List[str]] = Field(
        None,
        description="A list of the student's challenges. At least one of 'challenges' or 'needs' must be provided.",
        # Une liste des défis de l'étudiant. Au moins un des champs 'challenges' ou 'needs' doit être fourni.
        example=["Difficulty with time management", "Anxiety before exams"]
    )
    needs: Optional[List[str]] = Field(
        None,
        description="A list of the student's needs. At least one of 'challenges' or 'needs' must be provided.",
        # Une liste des besoins de l'étudiant. Au moins un des champs 'challenges' ou 'needs' doit être fourni.
        example=["Need for better study methods", "Stress management techniques"]
    )

    class Config:
        json_schema_extra = {
            "example": {
                "age": 21.5,
                "gender": "female",
                "strengths": ["Strong teamwork skills", "Excellent listening skills", "Creative problem-solving"],
                "challenges": ["Difficulty with time management", "Anxiety before exams"],
                "needs": []
            }
        }
    
    # Custom validation to ensure at least one of 'challenges' or 'needs' is provided
    # Validation personnalisée pour s'assurer qu'au moins un des champs 'challenges' ou 'needs' est fourni
    
    # @classmethod
    # def __pydantic_validator__(cls, v, info):
    #     if not (v.get('challenges') or v.get('needs')):
    #         raise ValueError("At least one of 'challenges' or 'needs' must be provided.")
    #     return v
    
    @model_validator(mode='after')
    def validate_challenges_or_needs(cls, values):
        """
        Validates that at least one of 'challenges' or 'needs' is provided.
        """
        if not (values.challenges or values.needs):
            raise ValueError("At least one of 'challenges' or 'needs' must be provided.")
        return values
    

class Goal(BaseModel):
    """
    Data model for a single recommended goal.
    """
    # Modèle de données pour un objectif recommandé unique.
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique identifier for the goal.",
        # Identifiant unique de l'objectif.
        example="a1b2c3d4-e5f6-7890-1234-567890abcdef"
    )
    description: str = Field(
        ...,
        description="The description of the recommended goal.",
        # La description de l'objectif recommandé.
        example="Develop a weekly study schedule to improve time management."
        # Développer un emploi du temps d'étude hebdomadaire pour améliorer la gestion du temps.
    )



class GoalsResponse(BaseModel):
    """
    Data model for goals recommendation response.
    """
    # Modèle de données pour la réponse de recommandation des objectifs.
    data: Optional[List[Goal]] = Field(
        None,
        description="A list of recommended goals. This field is present in case of success.",
        # Une liste d'objectifs recommandés. Ce champ est présent en cas de succès.
        example=[
            {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "description": "Develop a weekly study schedule to improve time management."},
            {"id": "f5e4d3c2-b1a0-9876-5432-10fedcba9876", "description": "Learn and apply relaxation techniques to manage pre-exam stress."}
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
                    {"id": "a1b2c3d4-e5f6-7890-1234-567890abcdef", "description": "Develop a weekly study schedule to improve time management."},
                    {"id": "f5e4d3c2-b1a0-9876-5432-10fedcba9876", "description": "Learn and apply relaxation techniques to manage pre-exam stress."}
                ],
                "error": False,
                "message": None
            }
        }



# class GoalsResponse(BaseModel):
#     """
#     Data model for goals recommendation response.
#     """
#     # Modèle de données pour la réponse de recommandation des objectifs.
#     data: Optional[list[str]] = Field(
#         None,
#         description="A list of phrases describing the recommended goals. This field is present in case of success.",
#         # Une liste de phrases décrivant les objectifs recommandés. Ce champ est présent en cas de succès.
#         example=["Develop a weekly study schedule", "Master time management techniques"]
#         # Développer un emploi du temps d'étude hebdomadaire, Maîtriser les techniques de gestion du temps
#     )
#     error: bool = Field(
#         ..., 
#         description="Indicates whether an internal error occurred (True) or not (False).",
#         # Indique si une erreur interne est survenue (True) ou non (False).
#         example=False
#     )
#     message: Optional[str] = Field(
#         None, 
#         description="Detailed error message in case of a problem. This field is only present if 'error' is True.",
#         # Message d'erreur détaillé en cas de problème. Ce champ est présent uniquement si 'error' est True.
#         example=None
#     )

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "data": ["Develop a weekly study schedule", "Master time management techniques"],
#                 "error": False,
#                 "message": None
#             }
#         }