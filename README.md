# Privacy-Focused AI Chatbot: A Local RAG Implementation with Django and Ollama

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Ollama](https://img.shields.io/badge/ollama-%23000000.svg?style=for-the-badge&logo=ollama&logoColor=white)

## About the Project

This project features an AI-powered chatbot designed to provide specialized support by extracting insights directly from user-provided documents. Developed as the proposed system for a Undergraduate Thesis (TCC), this platform aims to deliver a versatile and secure conversational AI tool capable of assisting users across various professional and academic domains.

### Technical Stack & Core Features:
* **Core Framework:** Built with **Django**, providing a robust, scalable, and secure web interface.
* **Environment & Database:** Developed using **Python 3.13.13** and backed by **PostgreSQL 17.10** for reliable data persistence and relational management.
* **Local Processing:** Powered by **Ollama** to run open-source Large Language Models (LLMs) entirely locally, eliminating reliance on third-party cloud APIs.
* **Contextual Intelligence:** Implements **Retrieval-Augmented Generation (RAG)** to ensure the chatbot answers queries based strictly on the specialized context of uploaded documents.
* **Data Sovereignty:** By keeping all data processing and model execution local, the system guarantees strict data privacy and security.
* **Dynamic Configuration:** Features an intuitive interface that allows users to adjust and fine-tune model parameters on the fly, directly through the web UI.

### Why It Was Built
The system was conceived to address the growing need for secure, domain-specific AI assistants. Traditional cloud-based solutions often pose data privacy risks and offer limited customization. This project demonstrates how open-source technologies can be orchestrated locally to maintain absolute control over sensitive data, while providing an adaptable tool to optimize workflows and information retrieval in multiple fields.

## Getting Started

Follow these instructions to set up and run the project locally for development and testing purposes.

### Prerequisites

Before installation, ensure you have the following components installed on your system:

* **Python 3.13.13** or higher
* **PostgreSQL 17.10** or higher
* **Ollama** (installed and running locally)
* A tool to manage virtual environments (such as `venv` or `virtualenv`)

---

### Installation & Setup

#### 1. Clone the Repository
First, clone this repository to your local machine:
```bash
git clone https://github.com/MarcosBraga1/local-rag-privacy-chatbot.git
cd local-rag-privacy-chatbot
```

#### 2. Set Up the Virtual Environment
Create and activate a Python virtual environment to isolate the project dependencies:
```bash
# Create the environment
python -m venv .venv

# Activate it (Linux/macOS)
source .venv/bin/activate
```

#### 3. Install Dependencies
Install all required Python packages listed in the `requirements.txt` file:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 4. Configure the PostgreSQL Database
Create a new database and user in your local PostgreSQL instance. You can do this via psql or a graphical tool like pgAdmin:
```bash
CREATE DATABASE db_name;
```

#### 5. Environment Variables
The repository includes a `.env.example` file with the required configuration variables. Copy this file to create your own `.env` configuration:
```bash
# Linux/macOS
cp .env.example .env
```
Open the newly created `.env` file and update the values with your local settings (database credentials, Django secret key, and Google keys for Oauth).

#### 6. Run Database Migrations
Apply the initial Django migrations to set up your PostgreSQL database schema:
```bash
python3 manage.py migrate
```

#### 7. Configure Ollama & Download a Model
Ensure the Ollama service is running locally on your machine. The system natively supports four different open-source models. You must pull at least one (or all) of them via the Ollama CLI before running the application:
```bash
# Pull the specific models supported by the application
ollama pull qwen2.5:3b
ollama pull llama3
ollama pull llama3.2
ollama pull phi3
```
_Note: You only need to download the models you intend to test or use through the web UI interface._

### Running the Application
Once everything is configured, you can start the development server.

1. Start the Django local server:
```bash
python3 manage.py runserver
```

2. Open your web browser and navigate to `http://127.0.0.1:8000/accounts/login/`.

3. Access the interface, create an account or sign in with Google, configure your model parameters, upload your documents, and start interacting with the local RAG chatbot.

## Usage Guide

Once the application is up and running, follow these steps to use and test the local RAG chatbot capabilities:

1. **Authentication:** * When you first access the application, you will be prompted to either **Register** a new account or **Log In**.
   * You can sign in instantly using the **Sign in with Google** integration.
2. **Access the Dashboard:** After a successful login, you will be redirected to the main dashboard interface.
3. **Select an AI Model:** Use the interface dropdown to choose between the pre-installed models (`qwen2.5:3b`, `llama3`, `llama3.2`, or `phi3`).
4. **Adjust Hyperparameters:** If needed, fine-tune model parameters (such as *Temperature* or *Top-K*) directly via the UI settings panel.
5. **Start Chatting:** Submit queries in the chat interface. The system will retrieve context from your uploaded files and generate accurate, private, and localized answers.

## Project Structure

A brief overview of the main directory structure and where the core components reside:

```text
├── dashboard/             # Django app for the dashboard
│   ├── templates/         # Web UI frontend templates
│   ├── views.py           # Chatbot and model parameters control logic
│   └── models.py          # Database schemas for chat history
├── setup/                 # Django project configuration (settings, urls, wsgi)           
├── templates/             # Web UI frontend templates
│   ├── account/           # Web UI frontend for django-allauth routes
│   └── base_auth.html     # Base HTML template for auth pages
├── .env.example           # Template for environment variables
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies list
```

## License

This project is developed as an academic work for an Undergraduate Thesis (TCC). Distributed under the **MIT License**. See `LICENSE` for more information.