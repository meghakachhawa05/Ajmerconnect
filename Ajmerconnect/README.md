# Ajmerconnect - City Guide Platform

A comprehensive Django-based city guide platform for Ajmer, Rajasthan, India. This platform connects citizens with essential services, amenities, and healthcare facilities.

## Features

### 🏥 Hospital Management
- Find hospitals and doctors
- Book appointments online
- View doctor profiles and specializations
- Manage patient appointments

### 🎫 Amenity Booking System
- Book tickets for government amenities (parks, museums)
- Real-time availability checking
- QR code-based ticket verification
- Admin panel for facility management

### 🗺️ Interactive Map (Coming Soon)
- View all amenities and hospitals on an interactive map
- Get directions and location information
- Filter by category and distance

### 📱 Modern Landing Page
- **Hero Section**: Eye-catching introduction with search functionality
- **Stats Dashboard**: Real-time statistics of hospitals, amenities, doctors, and bookings
- **Category Filters**: Easy navigation to different types of services
- **Featured Places**: Highlighted amenities and popular destinations
- **Quick Actions**: Fast access to common tasks
- **Responsive Design**: Works perfectly on all devices

## Technology Stack

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Icons**: Font Awesome 6
- **Styling**: Custom CSS with modern gradients and animations

## Project Structure

```
resumeproject2/
├── Ajmerconnect/          # Main project settings
├── core/                  # Core app (authentication, home, about, contact)
├── hospital/              # Hospital management app
├── amenity/               # Amenities and booking app
├── booking/               # Ticketing system app
├── dashboard/             # Admin dashboard app
├── templates/             # HTML templates
│   ├── core/             # Core templates (home, about, contact, map)
│   ├── hospital/         # Hospital templates
│   ├── amenity/          # Amenity templates
│   ├── booking/          # Booking templates
│   └── dashboard/        # Dashboard templates
└── static/               # Static files (CSS, JS, images)
```

## Landing Page Features

### 🎨 Modern Design
- **Gradient Backgrounds**: Beautiful color gradients throughout
- **Card-based Layout**: Clean, organized information display
- **Hover Effects**: Interactive elements with smooth animations
- **Typography**: Modern font (Poppins) with proper hierarchy

### 🔍 Search Functionality
- **Global Search**: Search across all amenities and hospitals
- **Smart Suggestions**: Auto-complete with popular searches
- **Category Filtering**: Filter results by type

### 📊 Statistics Dashboard
- **Real-time Counts**: Dynamic statistics from database
- **Visual Icons**: Font Awesome icons for better UX
- **Animated Cards**: Hover effects and smooth transitions

### 🚀 Quick Actions
- **Book Hospital Appointment**: Direct link to appointment booking
- **My Bookings**: Access to user's booking history
- **View Map**: Link to interactive map
- **Create Account**: Registration for new users

### 📱 Responsive Design
- **Mobile-First**: Optimized for mobile devices
- **Tablet Support**: Responsive layout for tablets
- **Desktop Experience**: Full-featured desktop interface

## Getting Started

### Prerequisites
- Python 3.8+
- Django 4.2+
- pip

### Installation

1. **Install Django Framework**

   This project is built with the Django web framework.  
   If you don't have Django installed globally, you can install it with:

   ```bash
   pip install django
   ```

   Or, to install the specific version used in this project (recommended):

   ```bash
   pip install "django>=4.2"
   ```

   > Django is the main framework powering the backend of this project.

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Optional: PDF Generation Support**

   If you want to enable PDF generation features (such as exporting receipts or reports), install the `xhtml2pdf` package:

   ```bash
   pip install xhtml2pdf
   ```

   > This package is used for rendering HTML templates as PDF files in Django views.

4. **Optional: Razorpay Payment Gateway Integration**

   To enable online payments using Razorpay, install the official Razorpay Python SDK:

   ```bash
   pip install razorpay
   ```

   > This package is used to integrate Razorpay payment gateway for secure online transactions.

   **Note:**
   You will need to add your Razorpay API keys in your Django settings or environment variables.
   Refer to the [Razorpay documentation](https://razorpay.com/docs/payment-gateway/server-integration/python/) for setup instructions.

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Visit the application**
   - Home page: http://localhost:8000/
   - Admin panel: http://localhost:8000/admin/

## Key Pages

### 🏠 Home Page (`/`)
- Landing page with hero section
- Category filters for different services
- Statistics dashboard
- Featured places
- Quick action buttons

### 🗺️ Map Page (`/map/`)
- Interactive map placeholder
- Feature preview
- Navigation to other services

### ℹ️ About Page (`/about/`)
- Mission and vision
- Features overview
- Team information
- Statistics

### 📞 Contact Page (`/contact/`)
- Contact form
- Contact information
- FAQ section
- Business hours

## Customization

### Styling
- Modify `static/style.css` for custom styling
- Update color schemes in CSS variables
- Add new animations and effects

### Content
- Update featured amenities in the home view
- Modify statistics in the views
- Customize contact information

### Features
- Add new amenity types
- Implement real map integration
- Add more booking features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- **Email**: [Your Email Address] (replace with actual email)
- **Phone**: [Your Phone Number] (replace with actual number)
- **GitHub Issues**: Report bugs and feature requests on GitHub

---

**Built with ❤️ for the city of Ajmer**

> **Note**: This is a development project. Contact information and domain details should be updated when deploying to production. 