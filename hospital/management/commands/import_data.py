from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from hospital.models import Doctor, Hospital
from amenity.models import Amenity
import csv
import os
from django.conf import settings

User = get_user_model()

class Command(BaseCommand):
    help = 'Import doctor and amenity data from CSV files'

    def handle(self, *args, **options):
        self.stdout.write('Starting data import...')
        
        # Import doctors
        self.import_doctors()
        
        # Import amenities
        self.import_amenities()
        
        self.stdout.write(self.style.SUCCESS('Data import completed successfully!'))

    def import_doctors(self):
        csv_file_path = os.path.join(settings.BASE_DIR, 'csv', 'doctor.csv')
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.WARNING(f'Doctor CSV file not found at {csv_file_path}'))
            return
        
        self.stdout.write('Importing doctors...')
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            
            for row in reader:
                try:
                    # Clean and process the data
                    name = row.get('Name', '').strip()
                    if not name or name == '':
                        continue
                    
                    specialization = row.get('Specialization', '').strip()
                    qualifications = row.get('Qualifications', '').strip()
                    experience = row.get('Experience', '').strip()
                    clinic_hospital = row.get('Clinic/Hospital', '').strip()
                    fee = row.get('Fee', '').strip()
                    is_available = row.get('is_available', 'TRUE').strip().upper() == 'TRUE'
                    
                    # Create or get hospital
                    hospital, created = Hospital.objects.get_or_create(
                        name=clinic_hospital if clinic_hospital else 'General Hospital',
                        defaults={
                            'address': 'Ajmer, Rajasthan',
                            'phone': '0145-123456',
                            'email': 'info@hospital.com',
                            'admin': User.objects.first() or User.objects.create_user(
                                username='hospital_admin',
                                email='admin@hospital.com',
                                password='admin123'
                            )
                        }
                    )
                    
                    # Create doctor
                    doctor, created = Doctor.objects.get_or_create(
                        name=name,
                        defaults={
                            'specialization': specialization,
                            'qualification': qualifications,
                            'experience': self.parse_experience(experience),
                            'hospital': hospital,
                            'consultation_fee': self.parse_fee(fee),
                            'is_available': is_available
                        }
                    )
                    
                    if created:
                        count += 1
                        self.stdout.write(f'Created doctor: {name}')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing doctor {row.get("Name", "Unknown")}: {str(e)}'))
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} doctors'))

    def import_amenities(self):
        csv_file_path = os.path.join(settings.BASE_DIR, 'csv', 'amenity.csv')
        
        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.WARNING(f'Amenity CSV file not found at {csv_file_path}'))
            return
        
        self.stdout.write('Importing amenities...')
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            count = 0
            
            for row in reader:
                try:
                    # Clean and process the data
                    name = row.get('name', '').strip()
                    if not name or name == '':
                        continue
                    
                    amenity_type = row.get('type', '').strip()
                    address = row.get('address', '').strip()
                    contact = row.get('contact', '').strip()
                    website = row.get('website', '').strip()
                    description = row.get('description', '').strip()
                    latitude = row.get('latitude', '').strip()
                    longitude = row.get('lontitude', '').strip()  # Note: typo in CSV
                    is_featured = row.get('is_featured', '').strip().lower() == 'yes'
                    
                    # Parse coordinates
                    try:
                        lat = float(latitude) if latitude and latitude != '(not listed)' else None
                        lng = float(longitude) if longitude and longitude != '(not listed)' else None
                    except (ValueError, TypeError):
                        lat = None
                        lng = None
                    
                    # Create amenity
                    amenity, created = Amenity.objects.get_or_create(
                        name=name,
                        defaults={
                            'type': amenity_type,
                            'address': address,
                            'contact': contact,
                            'website': website,
                            'description': description,
                            'latitude': lat,
                            'longitude': lng,
                            'is_featured': is_featured
                        }
                    )
                    
                    if created:
                        count += 1
                        self.stdout.write(f'Created amenity: {name}')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error importing amenity {row.get("name", "Unknown")}: {str(e)}'))
            
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} amenities'))

    def parse_fee(self, fee_str):
        """Parse fee string and return numeric value"""
        if not fee_str:
            return 0
        
        # Remove currency symbols and extra characters
        fee_str = fee_str.replace('₹', '').replace(',', '').replace(' ', '')
        
        # Extract first number found
        import re
        numbers = re.findall(r'\d+', fee_str)
        if numbers:
            return int(numbers[0])
        
        return 0

    def parse_experience(self, exp_str):
        """Parse experience string and return numeric value"""
        if not exp_str:
            return 0
        
        # Extract first number found
        import re
        numbers = re.findall(r'\d+', exp_str)
        if numbers:
            return int(numbers[0])
        
        return 0
