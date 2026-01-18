import requests
import json

def log_and_print(logging, string):
    logging.info(string)
    print(string)

def get(logging, url, headers=None):
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json().get("data")
        elif response.status_code == 401:
            log_and_print(logging, "Error: Unauthorized. Your cookie/JWT might be expired or incorrect.")
        else:
            log_and_print(logging, f"Failed to retrieve data. Status Code: {response.status_code}")
            log_and_print(logging, f"Failed GET: {url}")
            log_and_print(logging, response.text)

    except requests.exceptions.RequestException as e:
        log_and_print(logging, f"An error occurred: {e}")

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
            log_and_print(logging, "Error: Unauthorized. Check your credentials/tokens.")
        elif response.status_code == 404:
            log_and_print(logging, "Error: Resource not found. Check the URL.")
        else:
            log_and_print(logging, f"Failed to update. Status Code: {response.status_code}")
            log_and_print(logging, response.text)

    except requests.exceptions.RequestException as e:
        log_and_print(logging, f"An error occurred: {e}")

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
            log_and_print(logging, "Error: Unauthorized. Check your credentials/tokens.")
        elif response.status_code == 404:
            log_and_print(logging, "Error: Resource not found. Check the URL.")
        else:
            log_and_print(logging, f"Failed to post. Status Code: {response.status_code}")
            log_and_print(logging, response.text)

    except requests.exceptions.RequestException as e:
        log_and_print(logging, f"An error occurred: {e}")

    return False

def delete(url, headers=None):
    try:
        response = requests.delete(url, headers=headers)

        if response.status_code in [200, 204]:
            print("Successfully deleted the resource.")
            return response.json().get("data") if response.status_code == 200 else True
            
        elif response.status_code == 401:
            print("Error: Unauthorized. Your cookie/JWT might be expired or incorrect.")
        elif response.status_code == 404:
            print("Error: Resource not found. It may have already been deleted.")
        else:
            print(f"Failed to delete. Status Code: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    return False

def get_jwt_token() -> str:

    res = requests.get("https://api.warframe.market")
    return res.cookies["JWT"]