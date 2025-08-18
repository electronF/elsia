from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from routers import strengths_router, challenges_router, goals_router, means_router, full_router
from utils.logging_setup import setup_logger
from recommendations.generate_full import FullRecommendation # Importez l'orchestrateur
from concurrent.futures import ThreadPoolExecutor

# Configuration du logger principal
main_logger = setup_logger("main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire de contexte pour le cycle de vie de l'application (startup et shutdown).
    """
    main_logger.info("Application starting up...")
    # Démarrage de l'executor et autres ressources si nécessaire
    FullRecommendation.executor = ThreadPoolExecutor(max_workers=5)
    main_logger.info("Thread pool executor for full_recommender started.")
    yield
    main_logger.info("Application shutting down...")
    # Arrêt de l'executor et nettoyage des ressources
    FullRecommendation.executor.shutdown(wait=True)
    main_logger.info("Thread pool executor for full_recommender shut down.")

# Créez une instance de FastAPI
app = FastAPI(
    title="API assistance for the implementation of response plans for students",
    # API d'assitance pour la mise en oeuvre des plans d'intervention pour Étudiants
    description="""An API to generate personalised recommendations for students, including strengths, challenges, needs, goals and resources.""",
    #Une API pour générer des recommandations personnalisées pour les étudiants, incluant les forces, les défis, les besoins, les objectifs et les moyens."""
    version="1.0.0",
    docs_url="/documentation",
    redoc_url=None,
    lifespan=lifespan
)

# Créez le routeur principal pour regrouper tous les autres
api_router = APIRouter(prefix="/api/v1")

# Inclure les routeurs spécifiques pour chaque endpoint
api_router.include_router(strengths_router.router)
api_router.include_router(challenges_router.router)
api_router.include_router(goals_router.router)
api_router.include_router(means_router.router)
api_router.include_router(full_router.router)

# Inclure le routeur principal dans l'application
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the Student Recommendation API! Access the documentation at /documentation"}