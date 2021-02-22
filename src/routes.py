from fastapi import Depends
from src.resources import auth, users, departments, projects, claims
from src.utils.security import check_admin, get_current_user


def add_routers(app, config):
    """
    Include routes
    :param app:
    :param config:
    :return: None
    """

    app.include_router(
        auth.router,
        prefix=f"{config.API_URL}/auth",
        tags=["Authentication"]
    )

    app.include_router(
        claims.router,
        prefix=f"{config.API_URL}/claims",
        tags=["Claims"],
        dependencies=[Depends(get_current_user)]
    )

    app.include_router(
        departments.router,
        prefix=f"{config.API_URL}/departments",
        tags=["Departments"],
        dependencies=[Depends(check_admin)]
    )

    app.include_router(
        projects.router,
        prefix=f"{config.API_URL}/projects",
        tags=["Projects"],
        dependencies=[Depends(check_admin)]
    )

    app.include_router(
        users.router,
        prefix=f"{config.API_URL}/users",
        tags=["Users"],
        dependencies=[Depends(check_admin)]
    )
