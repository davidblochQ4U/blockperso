from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()

# Adjust the path to the templates directory
templates_path = os.path.join(os.path.dirname(__file__), "../../webapp_demo/templates")
templates = Jinja2Templates(directory=templates_path)

@router.get("/demo")
def demo_view(request: Request):
    context = {"request": request, "key": "value"}
    return templates.TemplateResponse("demo.html", context)
