@echo off
set "PYTHONPATH=%cd%\BlogFastAPI;%PYTHONPATH%"
call C:\Users\kamil\PycharmProjects\FastBlogAPI\venv\Scripts\activate.bat
uvicorn main:app --reload
