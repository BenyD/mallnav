# Mall Navigator

A web application that helps users navigate through shopping malls, find stores, and get detailed directions to their desired destinations.

## Features

### Mall Navigation

- Browse through different malls in the city
- View detailed mall information including:
  - Address and parking details
  - Food court location and hours
  - Contact information
  - Website links

### Store Search and Navigation

- Search for stores by name, category, or floor
- Get detailed store information including:
  - Opening hours
  - Special offers
  - Contact details
  - Website links

### Enhanced Navigation Features

- Interactive "Start from" selection for personalized directions
- Step-by-step navigation instructions
- Estimated walking times
- Accessibility information
- Nearby amenities with walking distances
- Visual floor map representation
- Multiple starting point options:
  - Main Entrance
  - Parking Area
  - Food Court
  - Elevators
  - Escalators
  - Restrooms
  - Information Desk

## Technology Stack

- **Backend**: Python with Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, Bootstrap 5
- **Icons**: Bootstrap Icons

## Project Structure

```
mallnav/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── instance/
│   └── malls.db       # SQLite database
├── templates/
│   ├── base.html      # Base template
│   ├── index.html     # Home page
│   ├── mall.html      # Mall details page
│   ├── shop.html      # Shop details and navigation
│   └── search_results.html  # Search results page
└── README.md          # Project documentation
```

## Setup and Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/mallnav.git
   cd mallnav
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open your browser and navigate to `http://127.0.0.1:5000`

## Database Schema

### Mall

- id (Primary Key)
- name
- address
- parking_info
- food_court_location
- food_court_hours
- contact_number
- email
- website

### Shop

- id (Primary Key)
- name
- floor
- category
- directions
- opening_hours
- contact_number
- special_offers
- email
- website
- mall_id (Foreign Key)

## Features in Development

- [ ] Interactive floor maps
- [ ] Real-time store occupancy
- [ ] User reviews and ratings
- [ ] Mobile application
- [ ] AR navigation support

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Developed by Beny Dishon K
This project is licensed under the MIT License - see the LICENSE file for details.
