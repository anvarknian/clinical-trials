import json
import os

import dlt
from openai import OpenAI

# Get OPENAI_API_KEY from env or dlt secrets
api_key = os.getenv("OPENAI_API_KEY", dlt.secrets.get("credentials.openai_api_key"))

client = OpenAI(api_key=api_key)

def query_chatgpt(disease_description):
    inclusion_criteria = None
    exclusion_criteria = None
    try:
        prompt = """
        You are an AI in a data pipeline for health clinics. 
        Given an entity, standardize it into a brief, structured JSON. 
        Summarize entries in 'InclusionCriteria' in one text as <included_criteria_summary> and all entries in 'ExclusionCriteria' in one text as <excluded_criteria_summary>, keeping both strict and concise.
        
        The output should be:

        {
          'inclusion_criteria': '<included_criteria_summary>',
          'exclusion_criteria': '<excluded_criteria_summary>'
        }
        
        --
        Input:
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": disease_description}
            ],
            response_format={"type": "json_object"},
        )
        result = json.loads(response.choices[0].message.content)
        inclusion_criteria = result.get('inclusion_criteria', None)
        exclusion_criteria = result.get('exclusion_criteria', None)
    except Exception as e:
        print(f"An error has occurred: {e}")
    finally:
        return inclusion_criteria, exclusion_criteria
