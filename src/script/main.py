import os
import json

from dotenv import find_dotenv
from dotenv import load_dotenv

from .quip.client import QuipClient

def main():
    load_dotenv(find_dotenv(raise_error_if_not_found=True, usecwd=True))
    client = QuipClient(
        access_token=os.environ["QUIP_ACCESS_TOKEN"]
    )
    user = client.get_authenticated_user()

    #starred = client.get_folder(user["starred_folder_id"])
    #print(f"There are {len(starred['children'])} items in your starred folder")

    query = "SOP: RDS"
    threads = client.get_matching_threads(query, count=None, only_match_titles=False)
    print(f"There are {len(threads)} threads matching '{query}'")
    for thread in threads:
        #print(thread["thread"]["title"])
        print(json.dumps(thread, indent=2))
