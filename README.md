# API Monitor (api-up-test)

This Python script measures the latency of API calls and generates a CSV report. 

## Classes

- `APIMonitor`: This class takes a list of API data and provides a method to measure the latency of the API calls.

## Functions

- `read_api_data_from_json(file_path)`: Reads API data from a JSON file.
- `generate_csv_report(latency_results, output_file)`: Generates a CSV report from the latency results.
- `main()`: The main function that ties everything together.

## How to Run

1. Ensure you have Python 3 installed.
2. Install the required packages with `pip install -r requirements.txt`.
3. Run the script with `python main.py`.

## Input

The script expects a JSON file named `apis.json` in the same directory. The JSON file should contain an array of objects, each representing an API to monitor. Each object should have a `url` property and may optionally have a `method` and `data` property.

Example:

```json
{
    "apis": [
        {
            "url": "https://api.example.com",
            "method": "GET"
        },
        {
            "url": "https://api.example.com",
            "method": "POST",
            "data": {
                "key": "value"
            }
        }
    ]
}
```

## Output

The script generates a CSV file named api_report.csv in the same directory. The CSV file contains the following columns: API Name, Status, Latency (seconds), Response/Error.

## Future Goals

- To add custom auth support to the APIs

- To write the report to a db and add a function to compare the current result and previous result and generate that report too
