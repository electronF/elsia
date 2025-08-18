from typing import Optional, List, Dict
import uuid

import recommendations.init  # Importing the init module to access the send_query function


class MeansRecommendation:
    """
        Class to generate means recommendations based on the student's profile and goals.
    """
    def __init__(self, language: str = "en"):
        """
        Initializes the MeansRecommandation class with the specified language.
        :param language: Language for the recommendations, default is English ("en").
        """
        self.language = language
        if self.language == "fr":
            with open("./prompts/means_document_template_fr.txt", "r", encoding="utf-8") as file:
                self.document_context = file.read()
            with open("./prompts/means_template_fr.txt", "r", encoding="utf-8") as file:
                self.means_prompt_template = file.read()
        else:
            with open("./prompts/means_document_template_en.txt", "r", encoding="utf-8") as file:
                self.document_context = file.read()  
            with open("./prompts/means_template_en.txt", "r", encoding="utf-8") as file:
                self.means_prompt_template = file.read()
    
    def __send_query(self, query_text_means: str, means_document_context: str) -> str:
        """
        Sends a query to the Claude model to generate means recommendations.
        
        :param query_text_means: The text of the query for generating means.
        :param means_document_context: The context document for the profile.
        :return: The response from the Claude model.
        """
        
        query_means = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query_text_means
                },
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": "file_011CRskJiRMBcCwWsJAFjCm3"
                    },
                    "title": "Means recommendations", # Optional
                    "context": means_document_context, # Optional  
                    # "citations": {"enabled": True} # Optional, enables citations
                }
            ],
        }]
        
        return recommendations.init.send_query(query_means)  
    
    def recommend(self, age: Optional[float], gender: str, strengths: Optional[List[str]], challenges: Optional[List[str]], needs: Optional[List[str]], goals: List[str], number_items:int=10) -> dict:
        """
            Generate means based on the provided profile information age : {age}, gender:{gender}, strengths : {strengths}, challenges : {challenges}, needs : {needs} and goals : {goals}.
            
            :param age: The age of the student.
            :param gender: The gender of the student.
            :param strengths: List of strengths of the student.
            :param challenges: List of challenges faced by the student.
            :param needs: List of needs of the student.
            :param goals: List of goals set by the student.
            :param number_items: Number of means to generate.
            :return: A dictionary containing the error status and the generated recommendations.
        """

        try:
            print(f"Generating means for age: {age}")
            strengths = ',\n '.join(strengths)
            challenges = ',\n '.join(challenges)
            needs = ',\n '.join(needs)
            goals = ',\n '.join(goals)
            
            query_text_means = self.means_prompt_template.format(age=age, sex=gender, strengths = strengths, challenges = challenges, needs=needs, goals = goals, number_items=number_items)
            
            print(f"Query text for means: {query_text_means}")
            
            response = self.__send_query(query_text_means, self.document_context)
            
            print(f"Response from Claude: {response}aaa")
            
            response_dict = recommendations.init.process_response(response)
            
            means:List[Dict] = []
            if not response_dict['error'] :
                for item in response_dict['data']:
                    means.append({
                        "id": str(uuid.uuid4()),
                        "description": item
                    })
                return {"error": False, "data": means}
            else:
                return {"error": True, "data": None, "message": response_dict.get('message', 'Unknown error occurred')}
        
        except Exception as e:
            # Captures all errors to return them in a structured way
            # Capture toutes les erreurs pour les retourner de manière structurée
            return {"error": True, "data": None, "message": str(e)}