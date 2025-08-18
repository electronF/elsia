from typing import Optional

class StrengthsRecommandation:
    def recommend(self, age: Optional[float], description: str) -> dict:
        """
        Simule la logique de génération de recommandations de forces.
        Cette fonction est un placeholder.
        """
        try:
            # Simule une erreur interne aléatoire pour les tests
            import random
            if random.random() < 0.2:
                raise ValueError("Erreur interne simulée lors de la génération des forces.")

            # Simule le traitement de la description et retourne des recommandations
            # Remplacez cette logique par votre propre implémentation
            print(f"Génération de recommandations pour l'âge {age} et la description : {description}")
            
            recommendations = [
                "Capacité d'écoute exceptionnelle et empathie",
                "Force de proposition et créativité",
                "Excellentes compétences en travail d'équipe"
            ]

            return {"error": False, "data": recommendations}
        
        except Exception as e:
            # Capture toutes les erreurs pour les retourner de manière structurée
            return {"error": True, "data": None, "message": str(e)}