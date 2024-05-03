from beanie import SortDirection
from fastapi import APIRouter, HTTPException
from starlette import status
from models import ship, user_model, company_model, news_model
from schemas.main.vacancy import Vacancy, CompanyInfo
from schemas.main.resume import Resume
from .config import format_date


router = APIRouter()


@router.get("/main", status_code=status.HTTP_200_OK)
async def main_page():
    try:

        data = []

        document_vacancy = await ship.find().sort([("_id", SortDirection.DESCENDING)]).limit(4).to_list()

        vacancy = {
            "new_vacancy": []
        }
        for doc in document_vacancy:

            document_company = await company_model.find_one({"vacancies": doc.id})

            data_vacancy = {
                "company_info": CompanyInfo(**document_company.dict()),
                "vacancies": Vacancy(**doc.dict()),
            }
            vacancy["new_vacancy"].append(data_vacancy)

        data.append(vacancy)

        document_resume = await user_model.find().sort([("_id", SortDirection.DESCENDING)]).limit(4).to_list()

        resume = {
            "new_resume": []
        }

        for doc in document_resume:

            resume_doc = Resume(**doc.dict())
            resume["new_resume"].append(resume_doc)

        data.append(resume)

        document_news = await news_model.find().sort([("_id", SortDirection.DESCENDING)]).limit(4).to_list()

        news_list = {
            "new_news": [],
            "interesting": []
        }

        for news in document_news:

            formated_date = await format_date(news.created_at)

            news.created_at = formated_date

            news_list["new_news"].append(news)

        data.append(news_list)
        return data

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)