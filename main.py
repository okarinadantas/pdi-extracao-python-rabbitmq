import requests
import json
import os
import logging

logger = logging.getLogger(__name__)

def main(host, user, passwd, api_endpoint, filename_json):
    
    # Get list of queues
    try:
        url = f'http://{host}/api/{api_endpoint}'
        response = requests.get(url, auth=(user, passwd))
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        logger.error(f"Error: Could not connect to RabbitMQ. {error}")
        return
    except requests.exceptions.ConnectionError as error:
        logger.error(f"Error: Could not connect to RabbitMQ. {error}")
        return

    json_list_queues = response.json()
    queue_names = []
    for queue in json_list_queues:
        queue_name = queue["name"]
        if not (queue_name.endswith(".delay") or queue_name.endswith(".master")):
            queue_names.append(queue_name)

    # Get bindings
    bind_names = []
    for queue in queue_names:
        url = f'http://{host}/api/{api_endpoint}/{queue}/bindings'
        response = requests.get(url, auth=(user, passwd))
        response.raise_for_status()
        json_list_binds = response.json()
        for bind in json_list_binds:
            bind_names.append({"destination": bind["destination"], "source": bind["source"]})

    # Write bindings to file
    with open(filename_json, "w") as file:
        json.dump(bind_names, file, indent=2)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    host = os.getenv('host')
    user = os.getenv('user')
    passwd = os.getenv('passwd') 
    api_endpoint = os.getenv('api_endpoint')
    filename_json = os.getenv('filename_json')

    main(host, user, passwd, api_endpoint, filename_json)
