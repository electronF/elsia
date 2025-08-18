from fastapi import APIRouter, HTTPException, BackgroundTasks, status
import asyncio
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from models.means_models import MeansRequest, MeansResponse, Mean
from recommendations.generate_means import MeansRecommendation
from utils.logging_setup import setup_logger

import utils.variables as variables


router = APIRouter(prefix="/means", tags=["Means"])
means_logger = setup_logger("means")
executor = ThreadPoolExecutor(max_workers=5)

def get_recommendations_sync(request_data: dict, number_items: int = 10):
    """
    Synchronous function for generating means recommendations.
    """
    # Fonction synchrone pour la génération des recommandations de moyens.
    recommender = MeansRecommendation()
    
    return recommender.recommend(age=request_data["age"], gender=request_data["gender"], strengths=request_data["strengths"], challenges=request_data["challenges"], needs=request_data["needs"], goals=request_data["goals"], number_items=request_data.get("number_items", number_items))

# Examples for documentation
# Exemples pour la documentation
success_example = MeansResponse(
    data=[
        Mean(id="a1b2c3d4-e5f6-7890-1234-567890abcdef", description="Use the Pomodoro Technique to structure study sessions."),
        Mean(id="f5e4d3c2-b1a0-9876-5432-10fedcba9876", description="Practice deep breathing exercises before a test.")
    ], 
    error=False
)
internal_error_example = MeansResponse(error=True, message="Internal error in the recommendation algorithm.")
# Erreur interne de l'algorithme de recommandation.
timeout_error_example = MeansResponse(error=True, message="The request took longer than the allowed 1 minute to process.")
# Le traitement de la requête a dépassé le délai autorisé de 1 minute.

@router.post("/",
             response_model=MeansResponse,
             status_code=status.HTTP_200_OK,
             summary="Recommends student means to achieve goals.",
             # Recommande des moyens pour que l'étudiant atteigne ses objectifs.
             description="Takes a student's profile (strengths, challenges, needs, age, and gender) and their goals as input, then returns a list of recommended means. A timeout of 1 minute is applied.",
             # Prend en entrée le profil de l'étudiant (forces, défis, besoins, âge et sexe) et ses objectifs, puis retourne une liste de moyens recommandés. Un timeout de 1 minute est appliqué.
             responses={
                 status.HTTP_200_OK: {
                     "description": "Success. Returns means recommendations.",
                     # Succès. Retourne les recommandations de moyens.
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


async def get_means_recommendation(request: MeansRequest, background_tasks: BackgroundTasks = BackgroundTasks()):
    means_logger.info(f"Request received (fr: Requête reçue): {request.model_dump_json()}")
    
    try:
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(executor, get_recommendations_sync, request.model_dump(), variables.number_of_items)
        
        

        # future = executor.submit(get_recommendations_sync, request.age, request.description)
        result_dict = await asyncio.wait_for(future, timeout=60.0)
    except TimeoutError:
        error_message = "The request took longer than the allowed 1 minute to process."
        # Le traitement de la requête a dépassé le délai autorisé de 1 minute.
        means_logger.error(f"Timeout: {error_message}")
        response_data = {"error": True, "message": error_message}
        background_tasks.add_task(means_logger.info, f"Response (error): {response_data}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={"error": True, "message": error_message}
        )
    except Exception as e:
        error_message = f"An unexpected internal error has occurred.: {str(e)}"
        # Une erreur interne inattendue est survenue
        means_logger.error(f"Unhandled internal error: {error_message}")
        response_data = {"error": True, "message": error_message}
        background_tasks.add_task(means_logger.info, f"Response (error): {response_data}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": error_message}
        )

    background_tasks.add_task(means_logger.info, f"Response: {result_dict}")
    
    if result_dict.get("error"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": result_dict.get("message", "Internal error in the recommendation algorithm.")}
            # Erreur interne de l'algorithme de recommandation.
        )
    
    # La réponse de succès est envoyée avec le statut 200 par défaut.
    return MeansResponse(data=result_dict.get("data"), error=False)