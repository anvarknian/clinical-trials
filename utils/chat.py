import json

import dlt
from openai import OpenAI

client = OpenAI(api_key=dlt.secrets.get("credentials.openai_api_key"))


def query_chatgpt(disease_description):
    inclusion_criteria = []
    exclusion_criteria = []
    try:
        prompt = """
        You are a sophisticated AI embedded in a data pipeline for health clinics and the medical field. 
        I will give you an entity, and your task is to standardize it and return a concise, well-structured JSON object. 
        Summarize and rephrase each entry, keeping it strict and brief.
        The desired output must look line this: 
        {
          "inclusion_criteria": ['<included_criteria>'],
          "exclusion_criteria": ['<excluded_criteria>']
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
        inclusion_criteria = result.get('inclusion_criteria', [])
        exclusion_criteria = result.get('exclusion_criteria', [])
    except Exception as e:
        print(f"An error has occurred: {e}")
    finally:
        return inclusion_criteria, exclusion_criteria
