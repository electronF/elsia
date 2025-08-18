from typing import Optional

import recommendations.init  # Importing the init module to access the send_query function


class NeedRecommendation:
    """
    Class to generate needs recommendations based on the student's profile and goals.
    """
    
    def __init__(self, language: str = "en"):
        """
        Initializes the NeedRecommendation class with the specified language.
        :param language: Language for the recommendations, default is English ("en").
        """
        self.language = language
        if self.language == "fr":
            with open("./prompts/profile_document_template_fr.txt", "r", encoding="utf-8") as file:
                self.document_context = file.read()
            with open("./prompts/needs_template_fr.txt", "r", encoding="utf-8") as file:
                self.needs_prompt_template = file.read()
        else:
            with open("./prompts/profile_document_template_en.txt", "r", encoding="utf-8") as file:
                self.document_context = file.read()  
            with open("./prompts/needs_template_en.txt", "r", encoding="utf-8") as file:
                self.needs_prompt_template = file.read()
    
    def __send_query(self, query_text_needs: str, needs_document_context: str, age:Optional[float], number_items:Optional[int]=10) -> str:       
        """
            Sends a query to the Claude model to generate recommendations.
            
            :param query_text_needs: The text of the query for generating needs.
            :param needs_document_context: The context document for the profile.    
            :return: The response from the Claude model.
        """
        query_text_needs = self.needs_prompt_template.format(key_words=query_text_needs)
        
        query = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": query_text_needs
                },
                # {
                #     "type": "document",
                #     "source": {
                #         "type": "file",
                #         "file_id": "file_011CRskJiRMBcCwWsJAFjCm3"
                #     },
                #     "title": "Needs recommendations",  # Optional
                #     "context": needs_document_context,  # Optional  
                #     # "citations": {"enabled": True} # Optional, enables citations
                # }
            ],
        }]
        return recommendations.init.send_query(query)
    
    
    def recommend(self, age: Optional[float], description: str, number_items: int = 10) -> dict:
        """
            Generates needs recommendations based on the student's age and description.
            :param age: The age of the student.
            :param description: The description of the student's profile.
            :param number_items: The number of items to recommend.
            :return: A dictionary containing the recommended needs.
        """
        try:
            # Generate recommendations of strength for age {age} and the description : {description}
            response = self.__send_query(description, self.document_context, age=age, number_items=number_items)
            # Process the response to extract the data
            response_dict = recommendations.init.process_response(response)
 
            if not response_dict['error'] :
                return {"error": False, "data": response_dict['data']}
            else:
                return {"error": True, "data": None, "message": response_dict.get('message', 'Unknown error occurred')}
        except Exception as e:
            # Capture toutes les erreurs pour les retourner de manière structurée
            return {"error": True, "data": None, "message": str(e)}