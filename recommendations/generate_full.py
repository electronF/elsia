from typing import Dict, List, Optional
import uuid

import recommendations.init  # Importing the init module to access the send_query function


class FullRecommendation:
    """
    Class to orchestrate the generation of a full student profile.
    """
    # Classe pour orchestrer la génération d'un profil étudiant complet.
    def __init__(self, language: str = "en"):
        # Initialise les classes de recommandation pour chaque domaine
        
        self.language = language
        if self.language == "fr":
            with open("./prompts/profile_goals_means_template_fr.txt", "r", encoding="utf-8") as file:
                self.full_recommend_prompt_template = file.read()
        else:
            with open("./prompts/profile_goals_means_template_en.txt", "r", encoding="utf-8") as file:
                self.full_recommend_prompt_template = file.read() 
        
        
        if self.language == "fr":
            with open("./prompts/goals_document_template_fr.txt", "r", encoding="utf-8") as file:
                self.goals_document_context = file.read()
        else:
            with open("./prompts/goals_document_template_en.txt", "r", encoding="utf-8") as file:
                self.goals_document_context = file.read()  
        
        if self.language == "fr":
            with open("./prompts/profile_document_template_fr.txt", "r", encoding="utf-8") as file:
                self.profile_document_context = file.read()
        else:
            with open("./prompts/profile_document_template_en.txt", "r", encoding="utf-8") as file:
                self.profile_document_context = file.read()  
        
        if self.language == "fr":
            with open("./prompts/means_document_template_fr.txt", "r", encoding="utf-8") as file:
                self.means_document_context = file.read()
        else:
            with open("./prompts/means_document_template_en.txt", "r", encoding="utf-8") as file:
                self.means_document_context = file.read()  
            
    
        
            

    def __send_query(self, query_text_full_profile:str, profile_document_context: str, goals_document_context:str, means_document_context:str) -> str:
        """
        Sends a query to the Claude model to generate challenge recommendations.
        
        :param query_text_challenges: The text of the query for generating challenges.
        :param profile_document_context: The context document for the profile.
        :return: The response from the Claude model.
        """
        
        
        
        query = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query_text_full_profile
                },
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": "file_011CRiWWvDgSCYar39r8XM4t"
                    },
                    "title": "Instruction creation profile", # Optional
                    "context": profile_document_context, # Optional  
                    # "citations": {"enabled": True} # Optional, enables citations
                },
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": "file_011CRskFjFdCHud4pXMs6oWr"
                    },
                    "title": "Instruction creation d'objectifs", # Optional
                    "context": goals_document_context, # Optional  
                    # "citations": {"enabled": True} # Optional, enables citations
                },
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": "file_011CRskJiRMBcCwWsJAFjCm3"
                    },
                    "title": "Instruction creation moyens", # Optional
                    "context": means_document_context, # Optional  
                    # "citations": {"enabled": True} # Optional, enables citations
                }
            ],
        }]
        return recommendations.init.send_query(query) 
    
    async def recommend(self, age: Optional[float], gender: str, description: str, file: Optional[object], number_items:int=10) -> dict:
        """
        Generates a full profile including strengths, challenges, needs, goals, and means.
        This function orchestrates the calls to all other recommendation modules.
        """
        try:
            query_full = self.full_recommend_prompt_template.format(age = age, gender=gender,  description=description, number_items=number_items)
            
            response:str = self.__send_query(query_full, self.profile_document_context, self.goals_document_context, self.means_document_context)

            response_dict = recommendations.init.process_response(response)
            
            full_data = {
                "strengths": [],
                "challenges": [],
                "needs": [],
                "goals": [],
                "means": []
            }
            
            if not response_dict['error'] :
                for key, value in response_dict['data'].items():
                    for c_value in value:
                        if key == "strengths":
                            full_data["strengths"].append(c_value)
                        elif key == "challenges":
                            full_data["challenges"].append(c_value)
                        elif key == "needs":
                            full_data["needs"].append(c_value)
                        elif key in ["goals", "objectives"]:
                            full_data["goals"].append({
                                "id": str(uuid.uuid4()),
                                "description": c_value
                            })
                        elif key == "means":
                            full_data["means"].append({
                                "id": str(uuid.uuid4()),
                                "description": c_value
                            })
                return {"error": False, "data": full_data}
            else:
                return {"error": True, "data": None, "message": response_dict.get('message', 'Unknown error occurred')}
        except Exception as e:
            return {"error": True, "data": None, "message": str(e)}
