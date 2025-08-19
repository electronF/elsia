# Elsia: Recommendation Web API 

Elsia is a web API built with **FastAPI** that provides intelligent recommendations to assist professionals in creating intervention plans for students. This service gives client applications access to recommendation systems designed to support various stages of plan creation.

***

## Features

* **Full Profile Analysis:** Allows professionals to describe a student's full profile (strengths, challenges, needs) using a free-form text or a complete document.
* **Recommendation of Strengths and Challenges:** Identifies and recommends formulations of a student's strengths and challenges from a free-form description or keywords.
* **Learning Goal Recommendation:** Provides personalized learning objectives based on a student's profile, including age, gender, challenges, and needs.
* **Means Recommendation:** Suggests concrete strategies and means to achieve the recommended learning goals.

***

## Technology Stack 🛠️

* **Framework:** FastAPI
* **Language:** Python
* **Web Service Type:** **REST** (Representational State Transfer) 
* **Data Format:** **JSON** (JavaScript Object Notation) 
* **Transport Protocol:** **HTTPS** for production, **HTTP** for development 

***

## Installation and Local Setup 🚀

Follow these steps to get a local copy of the project up and running.

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/](https://github.com/)electronF/Elsia.git
    cd Elsia
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Start the server:**
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000` and the web version to test the API is available with **Swagger UI** at `http://127.0.0.1:8000/documentation`. 

***

## API Endpoints ⚙️

The API uses versioning in its URL, starting with `/api/v1/`. All endpoints use the `POST` method. The following endpoints are available:

* **URL:** `/api/v1/strengths/` 
* **URL:** `/api/v1/challenges/` 
* **URL:** `/api/v1/goals/` 
* **URL:** `/api/v1/means/` 
* **URL:** `/api/v1/profile/full/` 



### 1. Strengths
This endpoint recommends strength formulations from a free-form text. 
* **URL**: `/api/v1/strengths/` 
* **Method**: `POST` 
* **Request Body**: `application/json` 
    ```json
    {
      "age": 21.5, // Optional: The student's age 
      "description": "He enjoys working in a team, is a good listener and is creative." // Required: A description of the student's strengths 
    }
    ```
* **Response**: `200 OK`
    ```json
    {
      "data": [
        "Good teammor",
        "Excellent listening skills in class"
      ],
      "error": false
    }
    ```

### 2. Challenges
This endpoint recommends challenge formulations from a free-form text. 
* **URL**: `/api/v1/challenges/` 
* **Method**: `POST` 
* **Request Body**: `application/json` 
    ```json
    {
      "age": 21.5, // Optional: The student's age 
      "description": "He has trouble managing his time and feels stressed before exams." // Required: A description of the student's challenges 
    }
    ```
* **Response**: `200 OK`
    ```json
    {
      "data": [
        "Difficulty with time management",
        "Stress before exams"
      ],
      "error": false
    }
    ```

### 3. Goals
This endpoint recommends learning goals based on a student's profile. 
* **URL**: `/api/v1/goals/` 
* **Method**: `POST` 
* **Request Body**: `application/json` 
    ```json
    {
      "age": 21.5, // Required: Student's age 
      "challenges": ["Difficulty with time management", "Anxiety before exams"], // Required: List of student's challenges 
      "gender": "female", // Required: Student's gender 
      "needs": [], // Optional: Student's needs 
      "strengths": ["Strong teamwork skills", "Excellent listening skills"] // Required: List of student's strengths 
    }
    ```
* **Response**: `200 OK`
    ```json
    {
      "data": [
        {
          "id": "61b2c3d4-e5f6-7890-1234-5678900bcdef",
          "description": "Develop a weekly study schedule to improve time management."
        },
        {
          "id": "f5e4d3c2-blol-9876-5432-10fedcho9876",
          "description": "Learn and apply relaxation techniques to manage pre-exam stress."
        }
      ],
      "error": false
    }
    ```

### 4. Means
This endpoint recommends means to achieve learning goals based on the profile and objectives. 
* **URL**: `/api/v1/means/` 
* **Method**: `POST` 
* **Request Body**: `application/json` 
    ```json
    {
      "age": 21.5,
      "challenges": ["Difficulty with time management"],
      "gender": "female",
      "goals": ["Develop a weekly study schedule"],
      "needs": ["Personalized study plan"],
      "strengths": ["Strong teamwork skills"]
    }
    ```
* **Response**: `200 OK`
    ```json
    {
      "data": [ 
            {
                "goal": "Develop a weekly study schedule", 
                "means": [
                        {
                            "id": "a1b2x3c4-d5f6-7890-1234-56789@obcdef",
                            "description": "Use the Pomodoro Technique to structure study sessions."
                        },
                        {
                            "id": "f5e4d3c2-blol-9876-5432-10fedcho9876",
                            "description": "Practice deep breathing exercises before a test."
                        }
                    ],
            },
        ],
      "error": false
    }
    ```

### 5. Full Profile
This endpoint provides recommendations for strengths, challenges, needs, goals, and means based on a single free-form description or a file. 
* **URL**: `/api/v1/profile/full/` 
* **Method**: `POST` 
* **Request Body**: `form-data` 
    * `age`: Optional `float` 
    * `file`: Optional file object (`.pdf`, `.txt`, or `.docx`) 
    * `description`: Required `string` 
    * `gender`: Optional `"male"`, `"female"`, or `"other"` 
* **Response**: `200 OK`
    ```json
    {
      "data": {
        "challenges": ["Difficulty with time management"],
        "goals": [
            {
                "id": "a1b2x3c4-d5f6-7890-1234-56789@obcabb",
                "description":"Develop a weekly study schedule to improve time management.",
                "means": [
                    {
                        "id": "a1b2x3c4-d5f6-7890-1234-56789@ocfcdef",
                        "description": "Use the Pomodoro Technique to structure study sessions."
                    }
                ]
            }
        ],
        "needs": ["Personalized study plan"],
        "strengths": ["Strong teamwork skills", "Excellent Listening skills"]
      }
    }
    ```

***

## Error Handling ⚠️

The API uses standard HTTP status codes to indicate the result of a request.
* `200 OK`: The request was successful.
* `422 Unprocessable Entity`: A validation error occurred.
* `500 Internal Application Error`: An internal error occurred in the recommendation algorithm.
* `504 Timeout Error`: The request took longer than the allowed time to process.

***

## Project Status and Validation 🧪

* **Status:** This is a **private repository**.
* **Current Version:** The project is currently at version **v1.0.0**.
* **Validation:** Endpoints have been manually tested via the interactive Swagger UI. The implementation of automated tests is planned to increase robustness.

***

## Security and Authentication 🔒

The final authentication method is still being decided. The project may start with **API keys** and later adopt **OAuth 2.0** or **JWT** (JSON Web Tokens) if different roles and access levels are required.

***

## Project Structure 📂

The project is organized in a modular way for easy maintenance and collaboration.

```
mon_api_recommandation/
├── main.py                     # Le point d'entrée de l'application FastAPI
├── requirements.txt            # Liste des dépendances du projet
├── models/                     # Dossier pour tous les modèles de données Pydantic
│   ├── __init__.py             # Fichier d'initialisation du package
│   ├── strengths_models.py     # Modèles pour l'endpoint des forces
│   ├── challenges_models.py    # Modèles pour l'endpoint des défis
│   ├── goals_models.py         # Modèles pour l'endpoint des objectifs
│   ├── means_models.py         # Modèles pour l'endpoint des moyens
│   └── pi_models.py            # Modèles pour l'endpoint pour le plan d'intervention complet
├── routers/                    # Contient les différents fichiers de routes
│   ├── strengths_router.py     # Endpoint pour les forces
│   ├── challenges_router.py    # Endpoint pour les défis
│   ├── goals_router.py         # Endpoint pour les objectifs
│   ├── means_router.py         # Endpoint pour les moyens
│   ├── pi_router.py            # Endpoint pour le plan d'intervention complet
│   └── __init__.py             # Fichier pour la reconnaissance du package
├── recommendations/            # Sépare la logique métier (le code de génération des recommandations)
│   ├── generate_strengths.py   # Logique pour les recommandations de forces
│   └── ...                     # ... et d'autres modules de logique métier
├── utils/            # Contient les fonctions et variables utilisées dans le projets 
│   ├── logging_setup.py        # Contient les fonctions necessaires à la créations des logs journaliers.
│   ├── variables.py            # Contient les variables d'environnement partargées par les differentes parties du projet
│   └── __init__.py             # Fichier pour la reconnaissance du package
├── prompts/                    # Contient les differents prompts utilisées par les modèles de languages
│   ├── challenges_template_en.txt        # Contient le prompt template utilisées pour les challenges en version anglaise.
│   └── ...             #  Les autres fichiers 
└── logs/
    └── 2025-08-07/
    │    ├── strengths_logs.log
    │    ├── challenges_logs.log
    │    └── ...
    └── 2025-08-08/
        ├── strengths_logs.log
        ├── challenges_logs.log
        └── ...
```

***

## Contact 📧

For any questions or suggestions, please contact the development team.

