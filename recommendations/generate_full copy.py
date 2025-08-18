from typing import Optional, List, Dict
from recommendations.generate_strengths import StrengthsRecommendation
from recommendations.generate_challenges import ChallengesRecommendation
from recommendations.generate_goals import GoalsRecommendation
from recommendations.generate_means import MeansRecommendation
import asyncio

class FullRecommendation:
    """
    Class to orchestrate the generation of a full student profile.
    """
    # Classe pour orchestrer la génération d'un profil étudiant complet.
    def __init__(self, language: str = "en"):
        # Initialise les classes de recommandation pour chaque domaine

        
        # self.language = language
        # if self.language == "fr":
        #     with open("./prompts/profile_goals_means_template_fr.txt", "r", encoding="utf-8") as file:
        #         self.full_recommend_prompt_template = file.read()
        # else:
        #     with open("./prompts/profile_goals_means_template_en.txt", "r", encoding="utf-8") as file:
        #         self.full_recommend_prompt_template = file.read() 

    async def recommend(self, age: Optional[float], gender: str, profile_text: str, file: Optional[object], number_items:int=10) -> dict:
        """
        Generates a full profile including strengths, challenges, needs, goals, and means.
        This function orchestrates the calls to all other recommendation modules.
        """
        # Génère un profil complet incluant les forces, défis, besoins, objectifs et moyens.
        # Cette fonction orchestre les appels à tous les autres modules de recommandation.
        try:
            # Step 1: Generate strengths and challenges/needs from the profile text
            # Étape 1: Générer les forces et les défis/besoins à partir du texte du profil
            strengths_result = self.strengths_recommender.recommend(age=age, description=profile_text, number_items=number_items)
            challenges_result = self.challenges_recommender.recommend(age=age, description=profile_text, number_items=number_items)
            # Placeholder for needs. For now, let's assume they're generated with challenges.
            needs_result = challenges_result # Assuming needs are part of challenges for this mock

            if strengths_result.get("error") or challenges_result.get("error"):
                # Handle errors from sub-recommendations
                # Gérer les erreurs des sous-recommandations
                return {
                    "error": True,
                    "data": None,
                    "message": "Error during initial strengths or challenges generation."
                }
            
            strengths = strengths_result.get("data", [])
            challenges = challenges_result.get("data", [])
            needs = needs_result.get("data", [])

            # Step 2: Generate goals using the generated strengths, challenges, and needs
            # Étape 2: Générer les objectifs en utilisant les forces, défis et besoins générés
            # Note: We'll assume the recommend method can handle optional empty lists
            # Note: Nous supposerons que la méthode recommend peut gérer des listes vides facultatives
            goals_result = self.goals_recommender.recommend(
                age=age,
                gender=gender,
                strengths=strengths,
                challenges=challenges,
                needs=needs
            )

            if goals_result.get("error"):
                return {
                    "error": True,
                    "data": None,
                    "message": "Error during goals generation."
                }
            
            goals_data = goals_result.get("data", [])
            # Extract only the description of the goals for the next step
            goals_descriptions = [goal['description'] for goal in goals_data]
            
            # Step 3: Generate means using the generated goals and the full profile
            # Étape 3: Générer les moyens en utilisant les objectifs générés et le profil complet
            means_result = self.means_recommender.recommend(
                age=age,
                gender=gender,
                strengths=strengths,
                challenges=challenges,
                needs=needs,
                goals=goals_descriptions
            )

            if means_result.get("error"):
                return {
                    "error": True,
                    "data": None,
                    "message": "Error during means generation."
                }
                
            means_data = means_result.get("data", [])

            # Step 4: Aggregate all results into a single response
            # Étape 4: Agréger tous les résultats dans une seule réponse
            full_data = {
                "strengths": strengths,
                "challenges": challenges,
                "needs": needs,
                "goals": goals_data,
                "means": means_data
            }

            return {"error": False, "data": full_data}

        except Exception as e:
            return {"error": True, "data": None, "message": str(e)}