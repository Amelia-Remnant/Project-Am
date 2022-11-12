from fastapi import FastAPI, HTTPException, status, Response
from statistics import mean
from api.models import CompanyReviews, CompanySummary, IncomingReview
from api.api_operations import save_review, CompanyNotFound

app = FastAPI()

companies = {}

@app.get("/company/{company_name}/}", status_code=200, response_model=CompanyReviews)
def get_reviews(company_name: str):

    try:
        return companies[company_name]
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

@app.post("/company/{company_name}", response_model=CompanyReviews, status_code=200)
def save_company(company_name: str, review: IncomingReview, response : Response):

    try:
        review_response = save_review(review)
    except CompanyNotFound:
        response.status_code = status.HTTP_201_CREATED
        companies[company_name] = []

        review_response = save_review(review)

    return review_response

@app.delete("/delete/{company_name}")
def remove_company(company_name: str):
    del companies[company_name]
