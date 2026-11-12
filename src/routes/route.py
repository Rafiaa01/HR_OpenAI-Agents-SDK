from fastapi import APIRouter

from src.routes import emp_routes, leave_route, manager_route

router = APIRouter()

router.include_router(emp_routes.router)
router.include_router(leave_route.router)
router.include_router(manager_route.router)
