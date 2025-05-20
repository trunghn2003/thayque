#!/bin/bash
# Script to run all Django microservices in parallel

# Tạo venv cho từng service nếu chưa có
for service in appointment_service patient_service medication_service user_service; do
  if [ ! -d "$service/venv" ]; then
    echo "Creating venv for $service..."
    python3 -m venv $service/venv
    source $service/venv/bin/activate
    pip install -r requirements.txt || pip install -r ../requirements.txt
    deactivate
  fi
done

# Activate venv của ChatbotHealthcare (nếu cần)
source ChatbotHealthcare/venv/bin/activate

# Start each service in the background
cd appointment_service && source venv/bin/activate && python manage.py runserver 8001 &
cd ../patient_service && source venv/bin/activate && python manage.py runserver 8002 &
cd ../medication_service && source venv/bin/activate && python manage.py runserver 8003 &
cd ../user_service && source venv/bin/activate && python manage.py runserver 8004 &

# Optional: Print info
cd ..
echo "All services are running:"
echo "- Appointment Service:    http://localhost:8001/"
echo "- Patient Service:        http://localhost:8002/"
echo "- Medication Service:     http://localhost:8003/"
echo "- User Service:           http://localhost:8004/"

# Wait for all background jobs
wait
