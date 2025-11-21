import os
from openai import OpenAI
import yaml

class PlaybookGenerator:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key)
        else:
            self.client = None

    def generate_playbook(self, project_info, analysis_results, diagram):
        """
        Generates the full markdown playbook using OpenAI.
        """
        
        # Construct the prompt
        prompt = self._construct_prompt(project_info, analysis_results, diagram)
        
        if not self.client:
            return self._generate_mock_playbook(project_info)

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o", # Or gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are a Databricks Professional Services consultant. Generate a flawless client project delivery playbook."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating playbook: {str(e)}\n\nUsing mock playbook instead.\n\n{self._generate_mock_playbook(project_info)}"

    def _construct_prompt(self, project_info, analysis_results, diagram):
        return f"""
        PROJECT INFO:
        {yaml.dump(project_info)}

        ANALYSIS RESULTS:
        {yaml.dump(analysis_results)}

        ARCHITECTURE DIAGRAM:
        {diagram}

        OUTPUT SECTIONS:
        1. Client Summary
        2. Project Objectives
        3. Architecture Diagram (Include the Mermaid code provided)
        4. Data Flow Explanation
        5. SQL Transformation Inventory
        6. ETL Workflows
        7. Risks & Mitigations
        8. Delivery Timeline
        9. Success Criteria
        10. Communication Cadence
        11. Documentation & Hand-Off

        Format as clean Markdown.
        """

    def _generate_mock_playbook(self, project_info):
        client = project_info.get('client', 'Client')
        return f"""
# Project Delivery Playbook – {client}

> [!NOTE]
> OpenAI API Key not found or error occurred. This is a generated mock playbook.

### Project Summary
{client} is migrating data pipelines to Databricks Delta Lake.

### Architecture
(See generated diagram)

### Key Work Packages
- Configure Unity Catalog
- Build ingestion workflow
- Incremental SQL transformation

### Risks
- IAM misalignment
- Schema drift
        """
