from fastapi import FastAPI, HTTPException, status, Response, Request
from statistics import mean
from api.models import CompanyReviews, CompanySummary, IncomingReview
from api.api_operations import save_review, CompanyNotFound
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

companies = {'Dominos': [{'review_text': 'Expensive', 'rating': 1}]}

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def index(request : Request):
    return templates.TemplateResponse("index.html", {"request" : request, "results" : companies})

@app.get("/company/{company_name}/}", status_code=200, response_model=CompanyReviews)
def get_reviews(company_name: str):

    try:
        return {"company" : company_name, "reviews" : companies[company_name] }
    except KeyError:
        message = f"{company_name} doesn't exist."
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=message)

@app.get("/company/{company_name}/summary}", response_model=CompanySummary, status_code=200)
def summary(company_name: str):

    if company_name not in companies:
        message = f"{company_name} doesn't exist."
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=message)

    ratings = [review["rating"] for review in companies[company_name]]

    avg_rating = mean(ratings)

    return {"company" : company_name , "avg_rating" : avg_rating}

@app.post("/company/{company_name}", response_model=CompanyReviews)
def save_company(company_name,  review: IncomingReview):

    try:
        review_response = save_review(review, company_name, companies)
    except CompanyNotFound:
        companies[company_name] = []
        review_response = save_review(review, company_name, companies)

    return review_response

@app.delete("/delete/{company_name}", response_model=CompanyReviews)
def remove_company(company_name: str):
    del companies[company_name]
