# Mall Navigator

A Flask-based web application that helps users navigate through various malls in Chennai, India. The app provides detailed directions to specific shops within each mall.

## Features

- Browse through 5 major malls in Chennai
- View all shops in each mall
- Get detailed directions to reach specific shops
- Information about shop categories and floor numbers

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd mallnav
   ```

2. **Create and activate virtual environment**

   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the Flask server**

   ```bash
   python app.py
   ```

2. **Access the application**
   - Open your web browser
   - Navigate to `http://127.0.0.1:5000`

## Using the Application

1. **Home Page**

   - View all available malls
   - Click on any mall to see its shops

2. **Mall Page**

   - See all shops in the selected mall
   - View shop categories and floor numbers
   - Click on any shop for detailed directions

3. **Shop Details Page**
   - Get specific directions to reach the shop
   - View shop category and floor information
   - Navigate back to mall or home page

## Available Malls

1. Vivira Mall
2. BSR Mall
3. Express Avenue Mall
4. Marina Mall
5. Phoenix Mall

## Troubleshooting

If you encounter any issues:

1. **Database not initializing**

   - Delete the `instance/malls.db` file
   - Restart the application

2. **Package installation issues**

   - Make sure your virtual environment is activated
   - Try running `pip install --upgrade pip` first
   - Then run `pip install -r requirements.txt`

3. **Application not starting**
   - Check if port 5000 is available
   - Ensure all required packages are installed
   - Verify Python version (should be 3.8 or higher)

## Development

- The application uses Flask for the backend
- SQLite database for data storage
- Bootstrap for frontend styling
- Jinja2 templating engine

## Credits

Developed by Beny Dishon K
