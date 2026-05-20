# python

## Setup

1. Create a virtual environment:

   ```
   python3 -m venv venv
   ```

2. Activate the virtual environment:
   - On macOS/Linux: `source venv/bin/activate`
   - On Windows: `venv\Scripts\activate`

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Script

To run the YAML configuration loader:

```
python 2/2.py --config 2/config.yaml
```

This will load the configuration from the specified YAML file and print it as a dictionary.
