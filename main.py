import json
import requests
import csv
import time


class APIMonitor:
    def __init__(self, api_data):
        self.api_data = api_data

    def measure_latency(self, num_measurements=5):
        latency_results = []
        for api_info in self.api_data:
            latencies = []
            for _ in range(num_measurements):
                start_time = time.time()
                response = self._make_request(api_info)
                end_time = time.time()
                latency = end_time - start_time
                latencies.append(latency)
            avg_latency = sum(latencies) / len(latencies)
            latency_results.append((api_info["url"], response, avg_latency))
        return latency_results

    def _make_request(self, api_info):
        method = api_info.get("method", "GET")
        url = api_info["url"]
        data = api_info.get("data")

        if method == "GET":
            return requests.get(url)
        elif method == "POST":
            return requests.post(url, json=data)
        # Add support for other methods as needed (PUT, DELETE, etc.)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")


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


def main():
    # Read API data from JSON file
    api_data = read_api_data_from_json("apis.json")

    # Initialize APIMonitor instance
    api_monitor = APIMonitor(api_data)

    # Measure latency of API calls
    latency_results = api_monitor.measure_latency()

    # Generate and write CSV report
    generate_csv_report(latency_results, "api_report.csv")


if __name__ == "__main__":
    main()
