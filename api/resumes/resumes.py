import math
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Annotated
from datetime import date
from api.auth.config import get_current_user
from models import user_model, auth, company_model, ship
from starlette import status
from beanie import PydanticObjectId
from schemas.resumes.user_resume import UserResumeResponse, PostAJobsRequest, UserResume

router = APIRouter()


@router.get("/resumes", response_model=UserResumeResponse)
async def get_all_vacancies_user(page: int = 1, page_size: int = 6):
    try:

        skip = (page - 1) * page_size
        limit = page_size

        total_count = await user_model.find().count()
        total_pages = math.ceil(total_count / page_size)

        resumes = await user_model.find().skip(skip).limit(limit).to_list()

        resume_list = []
        for vacancy in resumes:
            resume_list.append(UserResume(**vacancy.dict()))

        data = UserResumeResponse(
            current_page=page,
            vacancies=resume_list,
            total_page=total_pages
        )

        return data

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/resumes/search")
async def search_resumes(
        salary: str = Query(None),
        ship_type: str = Query(None),
        position: str = Query(None),
        date_of_departure: date = Query(None),
        contract_duration: str = Query(None),
        page: int = 1, page_size: int = 7):

    try:

        filter_query = {}
        if salary:
            filter_query["salary"] = salary
        if ship_type:
            filter_query["ship_type"] = ship_type
        if position:
            filter_query["position"] = {"$regex": position, "$options": "i"}
        if date_of_departure:
            filter_query["date_of_departure"] = date_of_departure
        if contract_duration:
            filter_query["contract_duration"] = contract_duration

        total_resume = await user_model.find(filter_query).count()
        total_pages = math.ceil(total_resume / page_size)
        resumes_db = await user_model.find(filter_query).skip((page - 1) * page_size).limit(page_size).to_list()

        resumes_list = []
        for resume in resumes_db:
            resumes_list.append(UserResume(**resume.dict()))

        return UserResumeResponse(current_page=page, vacancies=resumes_list, total_page=total_pages)

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/resumes/{sailor_id}", response_model=user_model)
async def get_user_vacancy(sailor_id: PydanticObjectId):
    try:

        user_vacancy = await user_model.get(sailor_id)

        if not user_vacancy:
            raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)

        return user_vacancy

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.get("/resumes/{sailor_id}/post-a-job", status_code=status.HTTP_200_OK)
async def post_a_job_get(sailor_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_id = current_user.get('id')
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(detail="Company not found", status_code=status.HTTP_404_NOT_FOUND)

        company = await company_model.get(company_info.resumeID)

        vacancy_list = company.vacancies

        response_list = []

        for vacancy in vacancy_list:
            jobs = await ship.get(vacancy.id)

            response_list.append(jobs)

        return response_list

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/resumes/{sailor_id}/post-a-job")
async def post_a_job_post(sailor_id: PydanticObjectId, request: PostAJobsRequest,
                          current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_id = current_user.get('id')
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(detail="Company not found", status_code=status.HTTP_404_NOT_FOUND)

        jobs = await ship.get(request.id)

        if not jobs.job_offers:
            jobs.job_offers = []

        jobs.job_offers.append(request.id)

        await jobs.save()

        return jobs

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/resumes/{sailor_id}/add_favorite", status_code=status.HTTP_201_CREATED)
async def add_user_to_favorite(sailor_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_id = current_user.get('id')
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(detail="Company not found", status_code=status.HTTP_404_NOT_FOUND)

        company = await company_model.get(company_info.resumeID)

        if not company.favorites_resume:
            company.favorites_resume = []

        company.favorites_resume.append(sailor_id)
        await company.save()

        return company

    except HTTPException as e:
        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.post("/resumes/search")
async def search_resume(current_user: Annotated[dict, Depends(get_current_user)],
                        title: str = Query(None), salary: int = Query(None)):
    try:

        query = {}

        if title:
            query["title"] = {"$regex": title, "$options": "i"}

        if salary:
            query["salary"] = {"$gte": salary}

        resume = user_model.find(query).to_list()

        return resume

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)


@router.post('/resumes/{sailor_id}/add-blacklist', status_code=status.HTTP_201_CREATED)
async def add_blacklist(sailor_id: PydanticObjectId, current_user: Annotated[dict, Depends(get_current_user)]):
    try:

        company_id = current_user.get('id')
        company_info = await auth.get(company_id)

        if not company_info:
            raise HTTPException(detail="Company not found", status_code=status.HTTP_404_NOT_FOUND)

        company = await company_model.get(company_info.resumeID)

        if not company.black_list_resume:
            company.black_list_resume = []

        company.black_list_resume.append(sailor_id)
        await company.save()

        return company

    except HTTPException as e:

        return HTTPException(detail=e, status_code=status.HTTP_400_BAD_REQUEST)