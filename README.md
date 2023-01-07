# Project-Am

## Quickstart

To run this project after cloning, run:


### Terminal 1
```
python -m venv .venv
source .venv/
pip install requirements.txt
uvicorn main:app --reload
```

### Terminal 2
```
npx tailwindcss -i static/src/style.css -o static/css/main.css --watch
uvicorn main:app --reload
```