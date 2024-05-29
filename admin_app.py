from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette_admin.contrib.mongoengine import Admin, ModelView
from mongoengine import connect, disconnect
from dotenv import load_dotenv
from models.admin_models import (Auth, CompanyModel, CompanyTariffs, Vessel, UserModel, Ship, NewsModel,
                                 Contact, Position, RealHistory, SwimsTariffs, DescriptionTariffs, Navy)
import os


load_dotenv()

DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")

app = Starlette(
    routes=[
        Route(
            "/",
            lambda r: HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>'),
        )
    ],
    on_startup=[lambda: connect(db="aflot_backend", host="mongo", port=27017, username=DB_USERNAME,
                                password=DB_PASSWORD)],
    on_shutdown=[lambda: disconnect()],
)


# app = Starlette(
#     routes=[
#         Route(
#             "/",
#             lambda r: HTMLResponse('<a href="/admin/">Click me to get to Admin!</a>'),
#         )
#     ],
#     on_startup=[lambda: connect(db="aflot_backend", host="localhost", port=27017)],
#     on_shutdown=[lambda: disconnect()],
# )
# Create admin
admin = Admin(title="Admin: AFLOT ADMIN")


# Add views
class UserView(ModelView):
    pass


admin.add_view(UserView(Auth, icon="fa fa-users"))
admin.add_view(UserView(CompanyModel, icon="fa fa-users", label="Компании"))
admin.add_view(ModelView(UserModel, icon="fa fa-users", label="Резюме моряков"))
admin.add_view(ModelView(Ship, icon="fa fa-users", label="Вакансии"))
admin.add_view(ModelView(NewsModel, icon="fa fa-blog", label="Новости"))
admin.add_view(ModelView(Contact, icon="fa fa-users", label="Контакты"))
admin.add_view(ModelView(Vessel, icon="fa fa-users", label="Судна"))
admin.add_view(ModelView(Position, icon="fa fa-users", label='Позиции'))
admin.add_view(ModelView(RealHistory, icon="fa fa-blog", label="Истории"))
admin.add_view(ModelView(SwimsTariffs, icon="fa fa-users", label="Тарифы моряков"))
admin.add_view(ModelView(DescriptionTariffs, icon="fa fa-users", label="Описание тарифов"))
admin.add_view(ModelView(CompanyTariffs, icon="fa fa-users", label="Тарифы компании"))
admin.add_view(ModelView(Navy, icon="fa fa-users", label="Морской флот"))

admin.mount_to(app)
