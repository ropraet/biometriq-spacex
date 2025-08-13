# 🚀 SpaceX Explorer

A Python web application that fetches SpaceX data and provides an interactive interface to explore launches, rockets, and crew members.

## Features

### Core Functionality
- 📊 **Rocket Data Fetcher**: Standalone Python script that fetches all SpaceX rockets and saves detailed information to a MySQL database
- 🚀 **Launch Browser**: Web interface displaying SpaceX launches with pagination (5 per page)
- 👨‍🚀 **Crew Information**: Detailed crew member profiles for each launch
- ⭐ **Star Feature**: Allow users to "star" favorite crew members with custom nicknames

### Technical Details
- **Backend**: Flask (Python)
- **Frontend**: HTML/CSS with responsive design
- **Database**: MySQL (with PostgreSQL compatibility)
- **API**: SpaceX REST API v4
- **Styling**: Custom CSS with space-themed design

## Quick Start

### Prerequisites
- Python 3.7+
- MySQL server running
- Internet connection (for SpaceX API)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd biometriq-spacex
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up database configuration**
   
   Edit `.env` file with your database credentials:
   ```env
   DB_HOST=localhost
   DB_NAME=spacex_db
   DB_USER=root
   DB_PASSWORD=your_password
   ```

4. **Initialize the database**
   ```bash
   python database_setup.py
   ```

5. **Fetch rocket data (optional)**
   ```bash
   python fetch_rockets.py
   ```

6. **Run the web application**
   ```bash
   python app.py
   ```

7. **Open your browser**
   
   Navigate to: `http://localhost:5000`

## Project Structure

```
biometriq-spacex/
├── app.py                 # Main Flask web application
├── fetch_rockets.py       # Rocket data fetcher script
├── database_setup.py      # Database initialization
├── requirements.txt       # Python dependencies
├── .env                  # Database configuration
├── templates/            # HTML templates
│   ├── base.html         # Base template with styling
│   ├── index.html        # Launches listing page
│   ├── launch_detail.html # Launch details and crew
│   ├── starred_crew.html  # Starred crew members
│   └── rockets.html       # Rockets database view
└── README.md             # This file
```

## Usage Guide

### 1. Rocket Data Collection
The `fetch_rockets.py` script fetches comprehensive rocket information from the SpaceX API and stores it in your database with these details:
- Rocket specifications (height, mass, stages)
- Performance metrics (success rate, cost per launch)
- Historical data (first flight, active status)

### 2. Web Interface Navigation

**Home Page (`/`)**
- Browse all SpaceX launches with pagination
- View mission patches and basic launch info
- Click "View Details & Crew" for more information

**Launch Details (`/launch/<id>`)**
- Comprehensive launch information
- Crew member profiles with photos
- Star crew members with custom nicknames
- Links to external resources (Wikipedia, webcasts)

**Starred Crew (`/starred_crew`)**
- View all your starred crew members
- See custom nicknames you've assigned
- Access crew member resources

**Rockets Database (`/rockets`)**
- View all rockets in your database
- Technical specifications and performance data
- Active/inactive status

## Database Schema

### Rockets Table
- Stores comprehensive rocket information
- Key fields: name, description, height, mass, success rate
- Performance metrics: cost per launch, stages, boosters

### Crew Stars Table
- User-generated content for starring crew members
- Stores custom nicknames and timestamps
- Links to original crew member data

## Configuration Options

### Database Configuration (.env)
```env
DB_HOST=localhost          # Database server host
DB_NAME=spacex_db          # Database name
DB_USER=root               # Database username
DB_PASSWORD=               # Database password
SECRET_KEY=your-secret     # Flask secret key (optional)
```

## API Integration

This application uses the **SpaceX REST API v4**:
- Launches: `https://api.spacexdata.com/v4/launches`
- Rockets: `https://api.spacexdata.com/v4/rockets`
- Crew: `https://api.spacexdata.com/v4/crew/{id}`

## Troubleshooting

### Common Issues

**Database Connection Error**
- Ensure MySQL server is running
- Check credentials in `.env` file
- Run `database_setup.py` to create tables

**No Rockets Displayed**
- Run `python fetch_rockets.py` to populate database
- Check internet connection for API access

**Launch Data Not Loading**
- Verify internet connection
- Check SpaceX API status

**Port Already in Use**
- Change port in `app.py`: `app.run(port=5001)`
- Or kill process using port 5000

### Development Mode
The application runs in debug mode by default. For production:
1. Set `app.run(debug=False)`
2. Configure proper database credentials
3. Set a secure SECRET_KEY in `.env`

## Testing the Application

### Manual Testing Checklist
- [ ] Database setup completes without errors
- [ ] Rocket data fetcher populates database
- [ ] Home page loads with paginated launches
- [ ] Launch detail pages display crew information
- [ ] Star functionality works and saves to database
- [ ] Starred crew page displays saved crew members
- [ ] Rockets page shows database content
- [ ] All navigation links work correctly

### Sample Test Data
The application will work with live SpaceX API data. For testing:
1. Recent launches should have crew members
2. Historical launches may not have crew data
3. Rocket data should populate automatically

## Contributing

This project was built for BiometrIQ technical assessment. Key implementation decisions:
- Used MySQL as requested (PostgreSQL compatible)
- Structured commits to show development process
- Included comprehensive error handling
- Responsive design for various screen sizes

## License

This project is for demonstration purposes as part of a technical assessment.