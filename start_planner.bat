@echo off
start /B python "D:\ai-learning-journey\planner_server.py" >nul 2>&1
timeout /t 2 >nul
start "" "http://localhost:8888/planner.html"
