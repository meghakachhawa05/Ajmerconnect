import requests
from django.conf import settings
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class HospitalAPIService:
    def __init__(self):
        self.base_url = "https://api.lnmittalhospital.com"  # Example URL
        self.api_key = settings.HOSPITAL_API_KEY
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def get_available_beds(self, hospital_id):
        """Get real-time bed availability information"""
        try:
            response = requests.get(
                f"{self.base_url}/beds/availability",
                headers=self.headers,
                params={'hospital_id': hospital_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching bed availability: {str(e)}")
            return None

    def get_doctor_schedule(self, doctor_id):
        """Get real-time doctor schedule"""
        try:
            response = requests.get(
                f"{self.base_url}/doctors/schedule",
                headers=self.headers,
                params={'doctor_id': doctor_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching doctor schedule: {str(e)}")
            return None

    def get_emergency_status(self, hospital_id):
        """Get emergency department status"""
        try:
            response = requests.get(
                f"{self.base_url}/emergency/status",
                headers=self.headers,
                params={'hospital_id': hospital_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching emergency status: {str(e)}")
            return None

    def get_operation_theater_status(self, hospital_id):
        """Get operation theater availability"""
        try:
            response = requests.get(
                f"{self.base_url}/ot/status",
                headers=self.headers,
                params={'hospital_id': hospital_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching OT status: {str(e)}")
            return None

    def get_lab_results(self, patient_id):
        """Get patient lab results"""
        try:
            response = requests.get(
                f"{self.base_url}/lab/results",
                headers=self.headers,
                params={'patient_id': patient_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching lab results: {str(e)}")
            return None

    def get_pharmacy_inventory(self, hospital_id):
        """Get pharmacy inventory status"""
        try:
            response = requests.get(
                f"{self.base_url}/pharmacy/inventory",
                headers=self.headers,
                params={'hospital_id': hospital_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching pharmacy inventory: {str(e)}")
            return None

    def get_ambulance_status(self, hospital_id):
        """Get ambulance availability status"""
        try:
            response = requests.get(
                f"{self.base_url}/ambulance/status",
                headers=self.headers,
                params={'hospital_id': hospital_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching ambulance status: {str(e)}")
            return None

    def get_blood_bank_status(self, hospital_id):
        """Get blood bank inventory status"""
        try:
            response = requests.get(
                f"{self.base_url}/blood-bank/status",
                headers=self.headers,
                params={'hospital_id': hospital_id}
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching blood bank status: {str(e)}")
            return None 