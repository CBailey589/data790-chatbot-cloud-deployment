# data790-chatbot-cloud-deployment

A small llm chatbot deployed in an Azure Container Apps with MLFlow support for model analaysis.
This specific chatbot is meant to handle general user queries but is instructed to respond only in poems.
The chatbot prefers short standard poem formats, but will occasionally produce longer formats such as Sonnets and Villanelles.

## Deployment:

Two container images have been stored in Azure Container Registry:
1) The lightweight chatbot application
2) An MLFlow image

Two Azure container apps pull their respective image and exist independent of one another
The lightweight chatbot is able to send LLM call traces to MLFlow via HTTPS requests using Azure's internal network.
The lightweight chatbot forwards user prompts to the UNC AI Gateway for response generation

## Application

The chatbot (built with FastAPI) contains the following api endpoints:
- /chat [POST] accpets {"message": "user_prompt_here"} and returns a {"response": "generated_response_here"}
- /health [GET] Returns {"status": "running"} when the application is running.
- /docs [GET] Provided by default by FastAPI

The UNC AI Gateway is configured to use gpt-4.1-mini by default, but will use whatever is configured in the .env DEFAULT_MODEL variable.
Current security measures within the app include:
  - Rejecting prompts over 1,000 tokens, estimated using tiktoken. Rejections return a 413 response.
  - max_completion_tokens for the request is set to 500 tokens.

## Repository:
app/
  - __init__.py
  - llm_client.py   # System prompt, security, connection UNC API Gateway
  - main.py         # MLFlow integration, API endpoints, prompt validation 
mlflow/
  - Dockerfile      # Dockerfile for MLFlow image
Dockerfile          # Dockerfile for chatbot image
requirements.txt
.env.example
.dockerignore

## Local Operation:
- Create and activate a python virtual environment
  - ```python -m pip install -r requirements.txt```
- Configure .env with endpoints and API key
- Start MLFlow
  - ```mlflow server --host 127.0.0.1 --port 5000 --backend-store-uri sqlite:///mlflow.db```
- Start API
  - ```uvicorn app.main:app --reload```
- Open http://127.0.0.1:8000/docs and test the POST /chat method in the browser interface
- Open MLFlow at http://127.0.0.1:5000

## Cloud Deployment:
- Open an Azure Cloud Shell from the Azure Portal
- Upload the appropriate files to the Azure shell
- ```az acr build --registry acrdata790fall26 --image poetry-chatbot-connorb:v1 .```
- ```az acr build --registry acrdata790fall26 --image mlflow-connorb:v1 ./mlflow```
- Deploy the chatbot container app:
  - Container App: poetry-chatbot-connorb
  - Resource Group: rg-primary-unc-sdss-pilot-data-790-fall-26
  - Container App Environment: cae-data790-fall26
  - Port: 8000
  - CPU / Memory: 0.5 CPU / 1 GiB
  - Scaling: 0-2 replicas
- Deploy the MLFlow container app:
  - Container App: mlflow-connorb
  - Resource Group: rg-primary-unc-sdss-pilot-data-790-fall-26
  - Container App Environment: cae-data790-fall26
  - Port: 5000
  - CPU / Memory: 1 CPU / 2 GiB
  - Scaling: 1 replica
- The chatbot deployment needs external HTTPS. Configure the following variables:
  - LLM_API_KEY=<Container Apps secret reference>
  - LLM_BASE_URL=https://azureaiapi.cloud.unc.edu/openai/v1
  - DEFAULT_MODEL=gpt-4.1-mini
  - MLFLOW_TRACKING_URI=https://<internal-mlflow-hostname>
- You may need to whitelist your IP address to access the MLFlow container app if you can not access the app directly

## Scaling
- The chatbot reduces to zero instances in periods of downtime, and starts up upon receiving a user prompt.
- Initial startup for the chatbot will be slower due to the requirement for the container to start.

## Monitoring
- MLFlow monitoring can be observed within the MLFlow container app (prompts, latency, responses, tokens, etc).
- Because the SQLite is running within the MLFlow container app deployment, there is no persistent storage of traces. Restarting the app will delete all data.

<img width="1785" height="957" alt="image" src="https://github.com/user-attachments/assets/dad495cf-5e3d-4bd2-b048-593facd33915" />



