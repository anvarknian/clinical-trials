import json

import dlt
from openai import OpenAI

client = OpenAI(api_key=dlt.secrets.get("credentials.openai_api_key"))


def standardize_disease_name(disease_description):
    try:
        prompt = """
        You are a highly intelligent AI. 
        I will provide a title related to diseases, and I need you to return a well-structured JSON object in the format:
        {"name": "<disease>"}
        Ensure the name is accurate, properly formatted, and corresponds directly to the title provided.
        If the input is invalid or you can't guess the disease, then return {"name": "Unknown"}
        """
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": disease_description}
            ],
            response_format={"type": "json_object"},
        )
        return json.loads(response.choices[0].message.content).get("name", "Unknown")
    except Exception as e:
        print(f"An error has occurred: {e}")
