
import os
import time # The time module lets  pause the code or work with timestamps. # Poll API snapshot
import requests  # HTTP requests  , Send API calls to Bright Data 
from dotenv import load_dotenv # Load .env files , Secure API key handling
from typing import List, Dict, Any, Optional # The typing module allows you to add type hints to your functions.
from snapshot_operations import download_snapshot ,poll_snapshot_status
load_dotenv()


def poll_snapshot_status(
    snapshot_id: str, max_attempts: int = 60, delay: int = 5
) -> bool:
    api_key = os.getenv("6728f4558f49945c20fa08d041c151eee4a4115e5235a5a16d5fa4556003211f") # use os.getenv() to read the API key from environment variables: 
    progress_url = f"https://api.brightdata.com/datasets/v3/progress/{snapshot_id}" # getenv  is  use to read/write files removes or create the files and even get the current directory 
    headers = {"Authorization": f"Bearer {api_key}"}

    for attempt in range(max_attempts):
        try:
            print( f"Checking snapshot progress... (attempt {attempt + 1}/{max_attempts})")

            response = requests.get(progress_url, headers=headers)
            response.raise_for_status()

            progress_data = response.json()
            status = progress_data.get("status")

            if status == "ready":
                print("Snapshot completed!")
                return True
            elif status == "failed":
                print("Snapshot failed")
                return False
            elif status == "running":
                print("Still processing...")
                time.sleep(delay)
            else:
                print(f"Unknown status: {status}")
                time.sleep(delay)

        except Exception as e:
            print(f"Error checking progress: {e}")
            time.sleep(delay)

    print("Timeout waiting for snapshot completion")
    return False


def download_snapshot( # we only call this function when the snapshot is ready 
    snapshot_id: str, format: str = "json"
) -> Optional[List[Dict[Any, Any]]]:
    api_key = os.getenv("6728f4558f49945c20fa08d041c151eee4a4115e5235a5a16d5fa4556003211f")
    download_url = (
        f"https://api.brightdata.com/datasets/v3/snapshot/{snapshot_id}?format={format}"
    )
    headers = {"Authorization": f"Bearer {api_key}"}

    try: # and simply sends the requests to download a snapshot and returns the data to us 
        print("Downloading snapshot data...")

        response = requests.get(download_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        print(
            f"Successfully downloaded {len(data) if isinstance(data, list) else 1} items"
        )

        return data

    except Exception as e:
        print(f"Error downloading snapshot: {e}")
        return None
