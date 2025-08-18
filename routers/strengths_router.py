# routers/strengths_router.py

from fastapi import APIRouter, HTTPException, BackgroundTasks, status
import asyncio
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from models.strengths_models import StrengthsRequest, StrengthsResponse
from recommendations.generate_strengths import StrengthsRecommendation
from utils.logging_setup import setup_logger # Importez la fonction ici

import utils.variables as variables

router = APIRouter(prefix="/strengths", tags=["Forces"])
strengths_logger = setup_logger("strengths") # Le logger est configuré une seule fois

executor = ThreadPoolExecutor(max_workers=5)

def get_recommendations_sync(age: float, description: str):
    """Synchronous function for generating recommendations."""
    #Fonction synchrone pour la génération des recommandations.
    
    recommender = StrengthsRecommendation()
    return recommender.recommend(age, description, variables.number_of_items)


# Les exemples pour la documentation
success_example = StrengthsResponse(data=["Good teamwor", "Excellent listening skills in class"], error=False)
internal_error_example = StrengthsResponse(error=True, message="Internal error in the recommendation algorithm.")#Erreur interne de l'algorithme de recommandation.
timeout_error_example = StrengthsResponse(error=True, message="The request took longer than the allowed 1 minute to process.")#Le traitement de la requête a dépassé le délai autorisé de 1 minute.

@router.post("/", 
             response_model=StrengthsResponse,
             status_code=status.HTTP_200_OK,
             summary="Recommends a student's strengths based on a free description.",#Recommande les forces d'un étudiant en fonction d'une description libre.
             description="Takes a description of the student as input and returns a list of recommended strengths. A timeout of 1 minute is applied.",#Prend en entrée une description de l'étudiant et retourne une liste de forces recommandées. Un timeout de 1 minute est appliqué.
             responses={
                 status.HTTP_200_OK: {
                     "description": "Success. Returns strength recommendations.",#Succès. Retourne les recommandations de forces.
                     "content": {
                         "application/json": {
                             "example": success_example.model_dump()
                         }
                     }
                 },
                 status.HTTP_500_INTERNAL_SERVER_ERROR: {
                     "description": "Internal application error.",#Erreur interne de l'application.
                     "content": {
                         "application/json": {
                             "example": internal_error_example.model_dump()
                         }
                     }
                 },
                 status.HTTP_504_GATEWAY_TIMEOUT: {
                     "description": "Erreur de timeout.",#Erreur de timeout.
                     "content": {
                         "application/json": {
                             "example": timeout_error_example.model_dump()
                         }
                     }
                 }
             })
async def get_strengths_recommendation(request: StrengthsRequest, background_tasks: BackgroundTasks = BackgroundTasks()):
    strengths_logger.info(f"Request received (Requête reçue): {request.model_dump_json()}")
    
    try:
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(executor, get_recommendations_sync, request.age, request.description)

        # future = executor.submit(get_recommendations_sync, request.age, request.description)
        result_dict = await asyncio.wait_for(future, timeout=60.0)
    except TimeoutError:
        error_message = "The request took longer than the allowed 1 minute to process."#Le traitement de la requête a dépassé le délai autorisé de 1 minute.
        strengths_logger.error(f"Timeout: {error_message}")
        response_data = {"error": True, "message": error_message}
        # Log de l'erreur de timeout
        background_tasks.add_task(strengths_logger.info, f"Réponse (erreur): {response_data}")
        # Lève une HTTPException avec le code d'erreur 504
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={"error": True, "message": error_message}
        )    
        
    except Exception as e:
        error_message = f"An unexpected internal error has occurred.: {str(e)}"#Une erreur interne inattendue est survenue
        strengths_logger.error(f"Unhandled internal error (fr: Erreur interne non gérée): {error_message}")
        response_data = {"error": True, "message": error_message}
        background_tasks.add_task(strengths_logger.info, f"Réponse (erreur): {response_data}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": error_message}
        )
        
    

    background_tasks.add_task(strengths_logger.info, f"Réponse: {result_dict}")
    
    if result_dict.get("error"):
        # C'est une erreur interne du code de recommandation
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": result_dict.get("message", "Internal error in the recommendation algorithm.")}#Erreur interne de l'algorithme de recommandation.
        )
    
    return StrengthsResponse(data=result_dict.get("data"), error=False)
