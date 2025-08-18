from typing import Optional

import recommendations.init


class ChallengesRecommendation:
    """
    Class to recommend challenges based on the student's profile.
    """
    
    def __init__(self, language: str = "en"):
        """
        Initializes the ChallengesRecommendation class with the specified language.
        :param language: Language for the recommendations, default is English ("en").
        """
        self.language = language
        if self.language == "fr":
            with open("./prompts/profile_document_template_fr.txt", "r", encoding="utf-8") as file:
                self.document_context = file.read()
            with open("./prompts/challenges_template_fr.txt", "r", encoding="utf-8") as file:
                self.challenges_prompt_template = file.read()
        else:
            with open("./prompts/profile_document_template_en.txt", "r", encoding="utf-8") as file:
                self.document_context = file.read()  
            with open("./prompts/challenges_template_en.txt", "r", encoding="utf-8") as file:
                self.challenges_prompt_template = file.read()
        
    def __send_query(self, query_text_challenges: str, profile_document_context: str, number_items: int = 10, age:float = None ) -> str:
        """
        Sends a query to the Claude model to generate challenge recommendations.
        
        :param query_text_challenges: The text of the query for generating challenges.
        :param profile_document_context: The context document for the profile.
        :return: The response from the Claude model.
        """
        
        query_text_challenges = self.challenges_prompt_template.format(key_words = query_text_challenges, number_items=number_items)
        
        query = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query_text_challenges
                },
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": "file_011CRiWWvDgSCYar39r8XM4t"
                    },
                    "title": "Challenges recommendations", # Optional
                    "context": profile_document_context, # Optional  
                    # "citations": {"enabled": True} # Optional, enables citations
                }
            ],
        }]
        return recommendations.init.send_query(query)    
    
    # Method for the generation of recommendations for student's challenges.
    def recommend(self, age: Optional[float], description: str, number_items:Optional[int]=10) -> dict:
        """
            Generates challenge recommendations based on the student's age and description.
            :param age: The age of the student.
            :param description: A description of the student's profile.
            :return: A dictionary containing the error status and the generated recommendations.
        """
        try:
            # Generate recommendations of challenges for age {age} and the description : {description}
            response = self.__send_query(description, self.document_context, number_items=number_items, age=age)
            print(f"Response from Claude: {response}")
            response = response.replace("<output>", "").replace("</output>", "").strip()
            print(f"\n\nCleaned response: {response}")
            response_dict = recommendations.init.process_response(response)
            
            print(f"Response dict: {response_dict}")
 
            if not response_dict['error'] :
                return {"error": False, "data": response_dict['data']}
            else:
                return {"error": True, "data": None, "message": response_dict.get('message', 'Unknown error occurred')}
        
        except Exception as e:
            # Captures all errors to return them in a structured way
            # Capture toutes les erreurs pour les retourner de manière structurée
            return {"error": True, "data": None, "message": str(e)}

        