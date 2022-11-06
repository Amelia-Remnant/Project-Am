from fastapi import FastAPI

app = FastAPI()

companies = {}

@app.get("/{company_name}/summary}")
def summary(company_name: str):
    return companies[company_name]

@app.post("/save/{company_name}/{review}")
def save_company(company_name: str, review: str):
    companies[company_name] = review
    return companies[company_name]

@app.delete("/delete/{company_name}")
def remove_company(company_name: str):
    del companies[company_name]


