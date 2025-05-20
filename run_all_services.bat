@echo off
REM Script to run all Django microservices in parallel (Windows)

REM Activate virtual environment
call ChatbotHealthcare\venv\Scripts\activate.bat

REM Start each service in a new command window
title Appointment Service
start cmd /k "cd appointment_service && python manage.py runserver 8001"

title Patient Service
start cmd /k "cd patient_service && python manage.py runserver 8002"

title Medication Service
start cmd /k "cd medication_service && python manage.py runserver 8003"

title User Service
start cmd /k "cd user_service && python manage.py runserver 8004"

echo All services are running:
echo - Appointment Service:    http://localhost:8001/
echo - Patient Service:        http://localhost:8002/
echo - Medication Service:     http://localhost:8003/
echo - User Service:           http://localhost:8004/

pause
