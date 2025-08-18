from typing import Optional

import recommendations.init


class StrengthsRecommendation:
    """    Class to simulate the logic of generating student strengths recommendations.
    """
    
    def __init__(self, language: str = "fr"):
        """
        Initializes the StrengthsRecommendation class with the specified language.
        :param language: Language for the recommendations, default is French ("fr").
        """
        self.language = language
        if self.language == "fr":
            with open("./prompts/profile_document_template_fr.txt", "r", encoding="utf-8") as file:
                self.document_context = file.read()
            with open("./prompts/strengths_template_fr.txt", "r", encoding="utf-8") as file:
                self.strengths_prompt_template = file.read()
        else:
            with open("./prompts/profile_document_template_en.txt", "r", encoding="utf-8") as file:
                self.document_context = file.read()  
            with open("./prompts/strengths_template_en.txt", "r", encoding="utf-8") as file:
                self.strengths_prompt_template = file.read()
    
    def __send_query(self, query_text_strengths: str, profile_document_context: str, number_items: int = 10,  age:float=None) -> str:
        """
            Recommends strengths based on the provided profile information.
            
            :param query_text_strengths: The text of the query for generating strengths.
            :param profile_document_context: The context document for the profile.
            :param number_items: The number of strengths to generate.
            :param age: The age of the student, optional.
            :return: A dictionary containing the error status and the generated recommendations.
        """
        
        query_text_strengths = self.strengths_prompt_template.format(key_words = query_text_strengths, number_items=number_items)
        
        query = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query_text_strengths
                },
                {
                    "type": "document",
                    "source": {
                        "type": "file",
                        "file_id": "file_011CRiWWvDgSCYar39r8XM4t"
                    },
                    "title": "Strengths recommendations", # Optional
                    "context": profile_document_context, # Optional  
                    # "citations": {"enabled": True} # Optional, enables citations
                }
            ],
        }]
        return recommendations.init.send_query(query)
    
    def recommend(self, age: Optional[float], description: str, number_items:int=10) -> dict:
        """
        Recomamend strengths based on the provided profile information age : {age} and description : {description}
        """
        try:
            # Generate recommendations of strength for age {age} and the description : {description}
            response = self.__send_query(description, self.document_context, age=age, number_items=number_items)
            print(f"Response from Claude: {response}")
            response = response.replace("<output>", "").replace("</output>", "").strip()
            print(f"\n\nCleaned response: {response}")
            response_dict = recommendations.init.process_response(response)
 
            if not response_dict['error'] :
                return {"error": False, "data": response_dict['data']}
            else:
                return {"error": True, "data": None, "message": response_dict.get('message', 'Unknown error occurred')}
        except Exception as e:
            # Capture toutes les erreurs pour les retourner de manière structurée
            return {"error": True, "data": None, "message": str(e)}

