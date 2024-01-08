@echo off
set "set PYTHONPATH=%PYTHONPATH%;C:\path\to\directory\containing\BlogFastAPI"
call C:\Users\kamil\PycharmProjects\FastBlogAPI\venv\Scripts\activate.bat
uvicorn main:app --reload
