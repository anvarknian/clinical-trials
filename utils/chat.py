import dlt
from openai import OpenAI

client = OpenAI(api_key=dlt.secrets.get("credentials.openai_api_key"))


def standardize_disease_name(disease_description) -> str:
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
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error has occurred: {e}")
