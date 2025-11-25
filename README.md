# Databricks AI Playbook Generator

An AI tool that takes Databricks project artifacts (SQL notebooks, Python notebooks, config files, project description) and automatically generates a consulting “Project Delivery Playbook”.

## Project Overview
This tool automates the creation of "Project Delivery Playbooks" for Databricks consulting engagements. By analyzing project artifacts (SQL, Python, Configs), it generates a comprehensive guide, saving hours of manual work for consultants and ensuring consistency across projects.

> [!NOTE]
> **For Recruiters / Hiring Managers**: This project is a demonstration of AI Engineering, Streamlit UI development, and Databricks integration. It is designed to be easily analyzed by reviewing the code and the screenshots below, without the need to run the full environment.

## Model Usage & Real-World Considerations
The current implementation uses standard public models (e.g., OpenAI GPT-4) for demonstration purposes. In a real-world enterprise deployment, this architecture would be adapted to use:
- **Private/Fine-tuned Models**: To ensure data privacy and domain specificity.
- **RAG (Retrieval-Augmented Generation)**: To leverage internal knowledge bases.
- **Governance & Security**: Adhering to strict enterprise data handling policies.

## Setup

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Usage

Run the Streamlit app:
```bash
streamlit run app/ui/streamlit_app.py
```

## Screenshots

### Home Page
![Home](docs/images/home.png)

### Generated Playbook
![Playbook](docs/images/playbook.png)

### Architecture Diagram
![Architecture](docs/images/architecture.png)

