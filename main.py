from fastapi import FastAPI, HTTPException, status, Response, Request, Form
from statistics import mean
from api.models import CompanyReviews, CompanySummary, IncomingReview
from api.api_operations import save_review, CompanyNotFound
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

companies = {'Dominos': [{'review_text': "It's nice, but quite expensive", 'rating': 6.5}], 'Papa Johns': [{'review_text': 'Not as good as Dominos', 'rating': 1.3}], "My dad's pizza": [{'review_text': 'The best', 'rating': 10}]}

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
def index(request : Request):
    ordered_companies = sorted(companies.items(), key = lambda x: x[1][0]['rating'], reverse=True)
    dict(ordered_companies)

    return templates.TemplateResponse("index.html", {"request" : request, "companies" : ordered_companies})



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



@app.get("/newreview", response_class=HTMLResponse)
def index(request : Request):

    result = 'Leave a review!'

    return templates.TemplateResponse("newreview.html", context = {"request" : request, 'result' : result})


@app.get("/summaries", response_class=HTMLResponse)
def index(request : Request):

    result = 'Summaries'

    return templates.TemplateResponse("summaries.html", context = {"request" : request, 'result' : result})


@app.get("/reviews", response_class=HTMLResponse)
def index(request : Request):

    result = 'Reviews'

    return templates.TemplateResponse("reviews.html", context = {"request" : request, 'result' : result})


@app.post("/newreview", response_model=CompanyReviews)
async def leave_review(request: Request, company_name: str = Form(...), review_text: str = Form(...), rating: float = Form(...)):

    review = IncomingReview(review_text = review_text, rating = rating)

    try:
        review_response = save_review(review, company_name, companies)
    except CompanyNotFound:
        companies[company_name] = []
        review_response = save_review(review, company_name, companies)

        return templates.TemplateResponse("newreview.html", context = {"request" : request, 'result' : review_response})



@app.delete("/delete/{company_name}", response_model=CompanyReviews)
def remove_company(company_name: str):
    del companies[company_name]
