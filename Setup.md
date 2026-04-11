## Setup


## Virtual Environment Setup

### Using venv

Create a virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

Install dependencies: (Important)
```bash
pip install -r requirements.txt
```



# Creating the .env file
Create a .env file in /server
Add the env variables as written in the doc
then use env variables like: API_KEY = os.getenv("OPENROUTER_API_KEY")
