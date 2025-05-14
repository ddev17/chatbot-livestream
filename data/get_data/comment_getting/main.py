import json
import time

import requests

comment_link = input("Enter your comment link: ")

while True:
    try:
        response = requests.get(comment_link)
        if response.status_code not in [200, 201]:
            print(f"Lỗi {response.status_code}")
            continue

        data = response.json()
        # Trích xuất tất cả content
        contents = [
            json.loads(msg["content"])["content"]
            for message in data["data"]["message"]
            for msg in message["msgs"]
        ]

        with open("output.txt", "a", buffering=1, encoding="utf-8") as output_file:
            for content in contents:
                output_file.write(f"{content}\n")
                print(f"{content}")

    except Exception as e:
        print(f"Lỗi {e}")

    time.sleep(5)