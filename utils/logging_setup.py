import logging
from datetime import date
import os

def setup_logger_old(endpoint_name: str) -> logging.Logger:
    """
    Configure un logger pour un endpoint donné, créant un fichier de log
    journalier dans un dossier de date.
    """
    today_str = date.today().isoformat()  # ex: '2025-08-07'
    log_dir = os.path.join("logs", today_str)

    # Crée le dossier de date s'il n'existe pas
    os.makedirs(log_dir, exist_ok=True)

    log_file_path = os.path.join(log_dir, f"{endpoint_name}_logs.log")

    # Crée un logger unique pour cet endpoint
    logger = logging.getLogger(endpoint_name)
    logger.setLevel(logging.INFO)

    # Configure le FileHandler pour écrire dans le bon fichier
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Ajoute le handler seulement s'il n'est pas déjà présent
    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger


def setup_logger(endpoint_name: str) -> logging.Logger:
    """
    Configure un logger pour un endpoint donné.
    Crée dynamiquement un dossier de log journalier et un fichier de log dédié.
    La configuration du logger est effectuée une seule fois.
    """
    today_str = date.today().isoformat()
    log_dir = os.path.join("logs", today_str)

    # Crée le dossier de date s'il n'existe pas
    os.makedirs(log_dir, exist_ok=True)

    log_file_path = os.path.join(log_dir, f"{endpoint_name}_logs.log")

    # Obtient ou crée un logger avec un nom unique pour l'endpoint
    logger = logging.getLogger(endpoint_name)
    logger.setLevel(logging.INFO)

    # Empêche la propagation au logger racine, évitant la duplication
    logger.propagate = False
    
    # Vérifie si le logger a déjà un handler pour ne pas le dupliquer
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Exemple d'utilisation dans un endpoint
# strengths_logger = setup_logger("strengths")
# strengths_logger.info("Requête reçue: ...")