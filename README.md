AI Claim Assistant



An AI-powered FastAPI service that classifies insurance claims into structured categories.



Features



\- AI-based claim classification

\- FastAPI backend

\- Safe JSON parsing and fallback handling

\- Structured and normalized responses

\- Input validation

\- Detailed logging



Example Request



```json

{

&#x20; "text": "My car was scratched while parked"

}



Example Response

{

&#x20; "category": "vehicle",

&#x20; "reason": "Damage to vehicle while parked"

}



Supported Categories



* vehicle
* water\_damage
* fire\_damage
* unknown



How to Run



pip install -r requirements.txt

python -m uvicorn app.main:app --reload



Swagger UI:



http://127.0.0.1:8000/docs



Error Handling



* Handles invalid AI responses
* Prevents JSON parsing crashes
* Guarantees consistent API output



Tech Stack



* Python
* FastAPI
* OpenAI API
* Uvicorn



Project Status



Production-ready backend with safe AI integration.















