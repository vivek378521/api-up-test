import json
import requests
import csv
import time
import asyncio


class APIMonitor:
    def __init__(self, api_data):
        self.api_data = api_data

    async def measure_latency(self):
        tasks = []
        for api_info in self.api_data:
            task = asyncio.create_task(self._make_request(api_info))
            tasks.append(task)
        return await asyncio.gather(*tasks)

    async def _make_request(self, api_info):
        start_time = time.time()
        method = api_info.get("method", "GET")
        url = api_info["url"]
        data = api_info.get("data")
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        end_time = time.time()
        latency = end_time - start_time
        return (api_info["url"], response, latency)


def read_api_data_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
        return data["apis"]


def generate_csv_report(latency_results, output_file):
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["API Name", "Status", "Latency (seconds)", "Response/Error"])
        for url, response, latency in latency_results:
            if response.status_code // 100 == 2:
                writer.writerow([url, response.status_code, f"{latency:.6f}"])
            else:
                writer.writerow(
                    [
                        url,
                        response.status_code,
                        f"{latency:.6f}",
                        f"Error: {response.text}",
                    ]
                )


async def main():
    # Read API data from JSON file
    api_data = read_api_data_from_json("apis.json")

    # Initialize APIMonitor instance
    api_monitor = APIMonitor(api_data)

    # Measure latency of API calls concurrently
    latency_results = await api_monitor.measure_latency()

    # Generate and write CSV report
    generate_csv_report(latency_results, "api_report.csv")


if __name__ == "__main__":
    asyncio.run(main())
