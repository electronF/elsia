from fastapi import APIRouter, HTTPException, BackgroundTasks, status, UploadFile, File, Form
from typing import Optional, List, Literal
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import asyncio
import io
import mimetypes
from models.full_models import FullResponse, FullResponseData
from recommendations.generate_full import FullRecommendation
from utils.logging_setup import setup_logger

router = APIRouter(prefix="/profile/full", tags=["Full Profile"])
full_logger = setup_logger("full")
executor = ThreadPoolExecutor(max_workers=5)
full_recommender = FullRecommendation() # Instancie l'orchestrateur une seule fois

# Définition des types de fichiers supportés
SUPPORTED_FILE_TYPES = {
    'application/pdf': '.pdf',
    'text/plain': '.txt',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx'
}

def process_file_content(file: UploadFile) -> str:
    """
    Simulates reading the contents of a file and processing it as text.
    In a real implementation, this would involve using libraries
    such as “pypdf”, “python-docx”, or a text analysis API.
    """
    # Simule la lecture du contenu d'un fichier et son traitement en texte.
    # Dans une implémentation réelle, cela impliquerait l'utilisation de librairies
    # comme 'pypdf', 'python-docx', ou d'une API d'analyse de texte.
    
    try:
        content = file.file.read().decode("utf-8")
        return content
    except Exception as e:
        full_logger.error(f"Failed to read and process file content: {str(e)}")
        raise ValueError("Failed to process the uploaded file.")


def get_recommendations_sync(age: float, gender: str, profile_text: str, file : Optional[object]):
    """
    Synchronous function that calls the recommendation orchestrator.
    """
    #Fonction synchrone qui appelle l'orchestrateur de recommandation.
    
    return asyncio.run(full_recommender.recommend(age=age, gender=gender, profile_text=profile_text, file=file))

@router.post("/",
            response_model=FullResponse,
            status_code=status.HTTP_200_OK,
            summary="Recommends a full student profile based on a free-text description or a file.",
            #Recommande un profil étudiant complet basé sur une description en texte libre ou un fichier.
            description="""Takes a free-text description or a file (.txt, .pdf, .docx) describing the student's profile, along with optional age and gender, and returns a full profile including strengths, challenges, needs, goals, and means.
            
            - **Either `description` or `file` must be provided.**
            - If both are provided, the content of the `file` will be used and `description` will be ignored.
            
            A timeout of 5 minutes is applied for file processing and full generation.""",
            
            # Accepte une description en texte libre ou un fichier (.txt, .pdf, .docx) décrivant le profil de l'étudiant, ainsi que son âge et son sexe (facultatif), et renvoie un profil complet comprenant ses points forts, ses défis, ses besoins, ses objectifs et ses moyens.
             
            # - **Il faut fournir soit la « description », soit le « fichier ».**
            # - Si les deux sont fournis, le contenu du « fichier » sera utilisé et la « description » sera ignorée.

            # Un délai d'attente de 5 minutes est appliqué pour le traitement du fichier et la génération complète.
             
             
            responses={
                status.HTTP_200_OK: {
                    "description": "Success. Returns the full student profile recommendations.",
                },
                status.HTTP_400_BAD_REQUEST: {
                    "description": "Bad Request: No description or file provided, or unsupported file type.",
                    "content": {
                        "application/json": {
                            "examples": {
                                "no_input": {"detail": "Either a 'description' or a 'file' must be provided."},
                                "unsupported_file": {"detail": "Unsupported file type: .csv"}
                            }
                        }
                    }
                },
                status.HTTP_500_INTERNAL_SERVER_ERROR: {
                    "description": "Internal application error.",
                },
                status.HTTP_504_GATEWAY_TIMEOUT: {
                    "description": "Timeout error.",
                }
            })
async def get_full_recommendation(
    description: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    age: Optional[float] = Form(None),
    gender: Literal["male", "female", "other", "undefined"] = Form("undefined"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    # Logique de validation manuelle pour la description et le fichier
    if not description and not file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Either a 'description' or a 'file' must be provided."
        )

    profile_description = description
    profile_file = None
    if file:
        # Validation du type de fichier
        file_extension = mimetypes.guess_extension(file.content_type)
        if file_extension not in SUPPORTED_FILE_TYPES.values():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file_extension}. Supported types are: {', '.join(SUPPORTED_FILE_TYPES.values())}"
            )
        
        # Le contenu du fichier est prioritaire
        profile_text = process_file_content(file)

    full_logger.info(f"Request received for full profile. Description length: {len(profile_text) if profile_text else 0}, Age: {age}, Gender: {gender}")

    try:
        # Soumission de la tâche à l'executor
        future = executor.submit(get_recommendations_sync, age, gender, profile_text, file)
        # Timeout étendu pour ce cas complexe
        result_dict = await asyncio.wait_for(future, timeout=300.0)
    except TimeoutError:
        error_message = "The request took longer than the allowed 5 minutes to process."
        full_logger.error(f"Timeout: {error_message}")
        background_tasks.add_task(full_logger.info, f"Response (error): {error_message}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail={"error": True, "message": error_message}
        )
    except Exception as e:
        error_message = f"An unexpected internal error has occurred during processing: {str(e)}"
        full_logger.error(f"Unhandled internal error: {error_message}")
        background_tasks.add_task(full_logger.info, f"Response (error): {error_message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": error_message}
        )
    
    background_tasks.add_task(full_logger.info, f"Response: {result_dict}")

    if result_dict.get("error"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": result_dict.get("message", "Internal error in the full recommendation algorithm.")}
        )
    
    return FullResponse(data=FullResponseData(**result_dict.get("data")), error=False)