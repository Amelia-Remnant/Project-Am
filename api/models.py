from typing import List
from pydantic import BaseModel, validator

class IncomingReview(BaseModel):

    review_text : str
    rating : int

    @validator("rating")
    def rating_in_range(cls, rating):
        if rating in range(0,10):
            return rating
        else:
            raise ValueError("Rating must be between 1 and 10")

class CompanyReviews(BaseModel):

    company : str
    reviews : List[IncomingReview]

class CompanySummary(BaseModel):
    
    company : str
    avg_rating : float