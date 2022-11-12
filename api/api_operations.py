class CompanyNotFound(Exception):

    pass


def save_review(review, company_name, companies):

    review_json = {"review_text" : review.review_text, "rating" : review.rating}

    try:
        companies[company_name].append(review_json)
    except KeyError:
        raise CompanyNotFound

    return {"company" : company_name , "reviews" : companies[company_name]}