from aiogram import Router

from features.adminka.adminka import router as admin_router
from features.adminka.frb_giveaway import router as frb_give_router
from features.adminka.ids_mainling import router as ids_mailing_router
from features.adminka.mailing import router as mailing_router
from features.adminka.send_circle_video import router as circle_video_router
from features.adminka.statisticks import router as stat_router
from features.adminka.update_data import router as load_data_router
from features.adresses.adresses import router as adresses_router
from features.complaints.complaints import router as complaints_router
from features.contacts.contacts import router as contacts_router
from features.lk.lk import router as lk_router
from features.main_menu.main_menu import router as main_menu_router
from features.missclick import router as end_router
from features.questions.questions import router as questions_router
from features.stocks.stocks import router as stocks_router

router = Router()
router.include_routers(
    main_menu_router,
    questions_router,
    adresses_router,
    stocks_router,
    contacts_router,
    lk_router,
    complaints_router,
    admin_router,
    load_data_router,
    mailing_router,
    ids_mailing_router,
    stat_router,
    frb_give_router,
    circle_video_router,
    end_router
)
