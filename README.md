# Instagram Graph View

A tool for processing Instagram network logs and generating Gephi visualization files.

## Project Structure

```
.
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── network_logs_to_json.py  # Converts network logs to JSON files
│   ├── json_reader.py          # Reads JSON files and creates data structures
│   ├── file_writer.py          # Writes data to Gephi CSV files
│   └── main.py                 # Main script
├── network_logs/               # Input HAR files
├── json_followings/           # Intermediate JSON files
└── output/                    # Generated files
    ├── nodes.csv             # Generated nodes file
    ├── edges.csv             # Generated edges file
    ├── instagram_graph.log   # Main log file
    └── network_processing.log # Network processing log file
```

## Features

- Processes Instagram network logs (HAR files) to extract following data
- Converts network logs to structured JSON files
- Creates unique nodes for each user
- Generates directed edges for following relationships
- Produces Gephi-compatible CSV files
- Includes comprehensive error handling and logging
- Type hints for better code understanding

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your HAR files in the `network_logs` directory
2. Run the main script:
   ```bash
   python src/main.py
   ```

## Output

The script generates two CSV files in the `output` directory:
- `nodes.csv`: Contains user information (ID, full name, username)
- `edges.csv`: Contains relationships between users

## Logging

Log files are stored in the `output` directory:
- `instagram_graph.log`: Main application logs
- `network_processing.log`: Network logs processing details

## Error Handling

The script includes comprehensive error handling:
- Validates input files
- Handles missing or malformed data
- Provides detailed error messages in logs

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 