from fastapi import APIRouter, HTTPException, BackgroundTasks, status
import asyncio
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from models.challenges_models import ChallengesRequest, ChallengesResponse
from recommendations.generate_challenges import ChallengesRecommendation
from utils.logging_setup import setup_logger

import utils.variables as variables

router = APIRouter(prefix="/challenges", tags=["Challenges"]) # Le tag change
challenges_logger = setup_logger("challenges") # Le nom du logger est spécifique
executor = ThreadPoolExecutor(max_workers=5)

def get_recommendations_sync(age: float, description: str):
    """Synchronous function for generating recommendations."""
    # Fonction synchrone pour la génération des recommandations.
    recommender = ChallengesRecommendation()
    return recommender.recommend(age, description)

# Exemples pour la documentation
success_example = ChallengesResponse(data=["Difficulty with time management", "Stress before exams"], error=False)
internal_error_example = ChallengesResponse(error=True, message="Internal error in the recommendation algorithm.")
# Erreur interne de l'algorithme de recommandation.
timeout_error_example = ChallengesResponse(error=True, message="The request took longer than the allowed 1 minute to process.")
# Le traitement de la requête a dépassé le délai autorisé de 1 minute.


@router.post("/", 
             response_model=ChallengesResponse,
             status_code=status.HTTP_200_OK,
             summary="Recommends a student's challenges based on a free description of challenges.",
             # Recommande les défis d'un étudiant en fonction d'une description libre des défis.
             description="Takes a description of the student as input and returns a list of recommended challenges. A timeout of 1 minute is applied.",
             # Prend en entrée une description de l'étudiant et retourne une liste de défis recommandés. Un timeout de 1 minute est appliqué.
             responses={
                 status.HTTP_200_OK: {
                     "description": "Success. Returns challenge recommendations.",
                     # Succès. Retourne les recommandations de défis.
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
                 }
             })
async def get_challenges_recommendation(request: ChallengesRequest, background_tasks: BackgroundTasks = BackgroundTasks()):
    challenges_logger.info(f"Request received (fr: Requête reçue): {request.model_dump_json()}")
    
    try:
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(executor, get_recommendations_sync, request.age, request.description, variables.number_of_items)

        # future = executor.submit(get_recommendations_sync, request.age, request.description)
        result_dict = await asyncio.wait_for(future, timeout=60.0)
    except TimeoutError as exc:
        error_message = "The request took longer than the allowed 1 minute to process."
        # Le traitement de la requête a dépassé le délai autorisé de 1 minute.
        challenges_logger.error("Timeout: %s", error_message)
        response_data = {"error": True, "message": error_message}
        background_tasks.add_task(challenges_logger.info, f"Response (error): {response_data}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={"error": True, "message": error_message}
        ) from exc
        
    except Exception as e:
        error_message = f"An unexpected internal error has occurred.: {str(e)}"
        # Une erreur interne inattendue est survenue
        challenges_logger.error(f"Unhandled internal error: {error_message}")
        # Erreur interne non gérée
        response_data = {"error": True, "message": error_message}
        background_tasks.add_task(challenges_logger.info, f"Response (error): {response_data}")
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": error_message}
        )
        
    background_tasks.add_task(challenges_logger.info, f"Response: {result_dict}")
    
    if result_dict.get("error"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": result_dict.get("message", "Internal error in the recommendation algorithm.")}
            # Erreur interne de l'algorithme de recommandation.
        )
    
    return ChallengesResponse(data=result_dict.get("data"), error=False)