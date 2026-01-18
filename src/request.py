import requests
import json

def get(logging, url, headers=None):
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json().get("data")
        elif response.status_code == 401:
            logging.info("Error: Unauthorized. Your cookie/JWT might be expired or incorrect.")
        else:
            logging.info(f"Failed to retrieve orders. Status Code: {response.status_code}")
            logging.info(response.text)

    except requests.exceptions.RequestException as e:
        logging.info(f"An error occurred: {e}")

    return False

def patch(logging, url, headers, payload):
    try:

        response = requests.patch(url, headers=headers, json=payload)

        if response.status_code in [200, 204]:
            logging.info("Successfully updated resource.")
            try:
                return response.json()
            except json.JSONDecodeError:
                return True
                
        elif response.status_code == 401:
            logging.info("Error: Unauthorized. Check your credentials/tokens.")
        elif response.status_code == 404:
            logging.info("Error: Resource not found. Check the URL.")
        else:
            logging.info(f"Failed to update. Status Code: {response.status_code}")
            logging.info(response.text)

    except requests.exceptions.RequestException as e:
        logging.info(f"An error occurred: {e}")

    return False

def post(logging, url, headers, payload):
    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code in [200, 201, 204]:
            logging.info("Successfully created resource.")
            try:
                return response
            except (json.JSONDecodeError, ValueError):
                return True
                
        elif response.status_code == 401:
            logging.info("Error: Unauthorized. Check your credentials/tokens.")
        elif response.status_code == 404:
            logging.info("Error: Resource not found. Check the URL.")
        else:
            logging.info(f"Failed to post. Status Code: {response.status_code}")
            logging.info(response.text)

    except requests.exceptions.RequestException as e:
        logging.info(f"An error occurred: {e}")

    return False

def get_jwt_token() -> str:

    res = requests.get("https://api.warframe.market")
    return res.cookies["JWT"]