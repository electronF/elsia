from typing import Optional, List
from fastapi import APIRouter, HTTPException, BackgroundTasks, status
import asyncio
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from models.goals_models import GoalsRequest, GoalsResponse, Goal
from recommendations.generate_goals import GoalsRecommendation
from utils.logging_setup import setup_logger

import utils.variables as variables

router = APIRouter(prefix="/goals", tags=["Goals"])
goals_logger = setup_logger("goals")
executor = ThreadPoolExecutor(max_workers=5)

def get_recommendations_sync(age: Optional[float], gender: str, strengths: Optional[List[str]], challenges: Optional[List[str]], needs: Optional[List[str]], number_items:int=10):
    """
    Synchronous function for generating goal recommendations.
    """
    # Fonction synchrone pour la génération des recommandations d'objectifs.
    recommender = GoalsRecommendation()
    return recommender.recommend(age, gender, strengths, challenges, needs, number_items)

# Exemples pour la documentation
success_example = GoalsResponse(
    data=[
        Goal(id="a1b2c3d4-e5f6-7890-1234-567890abcdef", description="Develop a weekly study schedule to improve time management."),
        Goal(id="f5e4d3c2-b1a0-9876-5432-10fedcba9876", description="Learn and apply relaxation techniques to manage pre-exam stress.")
    ], 
    error=False
)
internal_error_example = GoalsResponse(error=True, message="Internal error in the recommendation algorithm.")
# Erreur interne de l'algorithme de recommandation.
timeout_error_example = GoalsResponse(error=True, message="The request took longer than the allowed 1 minute to process.")
# Le traitement de la requête a dépassé le délai autorisé de 1 minute.

@router.post("/",
             response_model=GoalsResponse,
             status_code=status.HTTP_200_OK,
             summary="Recommends student goals based on their age(optional), sex(optional), strengths, challenges, and needs.",
             # Recommande des objectifs pour un étudiant en fonction de ses forces, défis et besoins.
             description="Takes a student's profile (strengths, challenges, needs, age, and gender) as input and returns a list of recommended goals. A timeout of 1 minute is applied.",
             # Prend en entrée le profil de l'étudiant (forces, défis, besoins, âge et sexe) et retourne une liste d'objectifs recommandés. Un timeout de 1 minute est appliqué.
             responses={
                 status.HTTP_200_OK: {
                     "description": "Success. Returns goal recommendations.",
                     # Succès. Retourne les recommandations d'objectifs.
                     "content": {
                         "application/json": {
                             "example": success_example.model_dump()
                         }
                     }
                 },
                 status.HTTP_500_INTERNAL_SERVER_ERROR: {
                     "description": "Internal application error.",
                     # Erreur interne de l'application.
                     "content": {
                         "application/json": {
                             "example": internal_error_example.model_dump()
                         }
                     }
                 },
                 status.HTTP_504_GATEWAY_TIMEOUT: {
                     "description": "Timeout error.",
                     # Erreur de timeout.
                     "content": {
                         "application/json": {
                             "example": timeout_error_example.model_dump()
                         }
                     }
                 },
                 status.HTTP_422_UNPROCESSABLE_ENTITY: {
                    "description": "Validation Error: At least one of 'challenges' or 'needs' must be provided.",
                    # Erreur de validation : au moins un des champs 'challenges' ou 'needs' doit être fourni.
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": [
                                    {
                                        "loc": ["body"],
                                        "msg": "At least one of 'challenges' or 'needs' must be provided.",
                                        "type": "value_error"
                                    }
                                ]
                            }
                        }
                    }
                 }
             })


async def get_goals_recommendation(request: GoalsRequest, background_tasks: BackgroundTasks = BackgroundTasks()):
    goals_logger.info(f"Request received (fr: Requête reçue): {request.model_dump_json()}")
    
    # Validation personnalisée (gérée par Pydantic grâce au @model_validator)
    # L'exception sera automatiquement capturée par FastAPI et renverra un statut 422.
    
    try:
        # future = executor.submit(get_recommendations_sync, request.model_dump())
        # result_dict = await asyncio.wait_for(future, timeout=60.0)
        
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(executor, get_recommendations_sync, request.age, request.gender, request.strengths, request.challenges, request.needs, variables.number_of_items)

        # future = executor.submit(get_recommendations_sync, request.age, request.description)
        result_dict = await asyncio.wait_for(future, timeout=60.0)
        
    except TimeoutError:
        error_message = "The request took longer than the allowed 1 minute to process."
        # Le traitement de la requête a dépassé le délai autorisé de 1 minute.
        goals_logger.error(f"Timeout: {error_message}")
        response_data = {"error": True, "message": error_message}
        background_tasks.add_task(goals_logger.info, f"Response (error): {response_data}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={"error": True, "message": error_message}
        )
    except Exception as e:
        error_message = f"An unexpected internal error has occurred.: {str(e)}"
        # Une erreur interne inattendue est survenue
        goals_logger.error(f"Unhandled internal error: {error_message}")
        response_data = {"error": True, "message": error_message}
        background_tasks.add_task(goals_logger.info, f"Response (error): {response_data}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": error_message}
        )

    background_tasks.add_task(goals_logger.info, f"Response: {result_dict}")
    
    if result_dict.get("error"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": result_dict.get("message", "Internal error in the recommendation algorithm.")}
            # Erreur interne de l'algorithme de recommandation.
        )
    
    # La réponse de succès est envoyée avec le statut 200 par défaut.
    return GoalsResponse(data=result_dict.get("data"), error=False)