from fastapi import APIRouter, HTTPException, BackgroundTasks, status, UploadFile, File, Form
from typing import Optional, List, Literal
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import asyncio
import os
import uuid
import shutil
import mimetypes

from models.full_models import FullResponse, FullResponseData
from recommendations.generate_full import FullRecommendation
from utils.logging_setup import setup_logger

import utils.variables as variables


router = APIRouter(prefix="/profile/full", tags=["Full Profile"])
full_logger = setup_logger("full")
executor = ThreadPoolExecutor(max_workers=5)
full_recommender = FullRecommendation()

# Définition des types de fichiers supportés
SUPPORTED_FILE_TYPES = {
    'application/pdf': '.pdf',
    'text/plain': '.txt',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx'
}

# Créez un dossier temporaire pour les fichiers
TEMP_FILE_UPLOAD_DIR = "temp_uploads"
os.makedirs(TEMP_FILE_UPLOAD_DIR, exist_ok=True)

def get_recommendations_sync(age: float, gender: str, description: str, file_path: Optional[str], number_items: int = 10):
    """
    Fonction synchrone qui appelle l'orchestrateur de recommandation.
    """
    # Ici, nous transmettons le chemin du fichier (s'il existe) à la logique de génération.
    return asyncio.run(full_recommender.recommend(
                age=age,
                gender=gender,
                description=description,
                file=file_path,
                number_items=number_items
            )
    )

@router.post("/",
             response_model=FullResponse,
             status_code=status.HTTP_200_OK,
             summary="Recommends a full student profile based on a free-text description and an optional file.",
             description="""Takes a mandatory free-text description and an optional file (.txt, .pdf, .docx) describing the student's profile. Along with age and gender, it returns a full profile including strengths, challenges, needs, goals, and means.
             
             - **The `description` field is mandatory.**
             - If a `file` is provided, it will be saved to disk with a temporary name, and its path will be transmitted along with the description for a richer analysis.
             
             A timeout of 5 minutes is applied for file processing and full generation.""",
             responses={
                 status.HTTP_200_OK: {
                     "description": "Success. Returns the full student profile recommendations.",
                 },
                 status.HTTP_400_BAD_REQUEST: {
                     "description": "Bad Request: Missing mandatory description or unsupported file type.",
                     "content": {
                         "application/json": {
                             "examples": {
                                 "missing_description": {"detail": "The 'description' field is mandatory."},
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
    description: str = Form(...),
    file: Optional[UploadFile] = File(None),
    age: Optional[float] = Form(None),
    gender: Literal["male", "female", "other", "undefined"] = Form("undefined"),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    potential_filename = uuid.uuid4()
    full_logger.info(f"Request received for full profile. Age: {age}, Gender: {gender},  description: {description}, potential_file_name: {potential_filename}")

    file_path = None
    if file:
        file_extension = mimetypes.guess_extension(file.content_type)
        if file_extension not in SUPPORTED_FILE_TYPES.values():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {file_extension}. Supported types are: {', '.join(SUPPORTED_FILE_TYPES.values())}"
            )
        
        # Sauvegarde du fichier avec un nom temporaire
        temp_filename = f"{potential_filename}{file_extension}"
        file_path = os.path.join(TEMP_FILE_UPLOAD_DIR, temp_filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        full_logger.info(f"File saved to temporary path: {file_path}")
    

    try:
        # future = executor.submit(get_recommendations_sync, age, gender, description, file_path)
        # result_dict = await asyncio.wait_for(future, timeout=60.0)
        
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(executor, get_recommendations_sync, age, gender, description, file_path, variables.number_of_items)

        # future = executor.submit(get_recommendations_sync, request.age, request.description)
        result_dict = await asyncio.wait_for(future, timeout=60.0)
        
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
        
    finally:
        # Nettoyage du fichier temporaire si tout s'est bien passé
        # if file_path and os.path.exists(file_path):
        #     os.remove(file_path)
        #     full_logger.info(f"Temporary file deleted: {file_path}")
        pass

    background_tasks.add_task(full_logger.info, f"Response: {result_dict}")

    if result_dict.get("error"):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": True, "message": result_dict.get("message", "Internal error in the full recommendation algorithm.")}
        )
    
    return FullResponse(data=FullResponseData(**result_dict.get("data")), error=False)