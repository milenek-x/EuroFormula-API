# EuroFormula API

A comprehensive API and admin dashboard for managing EuroFormula racing series data.

## Features

### Driver Management
- Add, edit, and delete drivers
- Track driver details (number, name, nationality, team)
- Points calculation based on race results
- Driver status tracking (Rookie Championship, Gentleman Class, Guest Class)
- Drivers sorted by points in descending order

### Team Management
- Add, edit, and delete teams
- Track team details (ID, name, country)
- Team points calculation based on best two results in each race
- Teams sorted by points in descending order

### Race Management
- Add, edit, and delete races
- Track race details (round, circuit, city, country)
- Manage multiple races per round (up to 3 races)
- Schedule management with dates and times

### Results Management
- Record race results for each round
- Track pole positions
- Record finishing positions
- Track fastest laps
- Automatic points calculation

## Points System

### Driver Points
- Race Positions (1-10):
  - 1st: 25 points
  - 2nd: 18 points
  - 3rd: 15 points
  - 4th: 12 points
  - 5th: 10 points
  - 6th: 8 points
  - 7th: 6 points
  - 8th: 4 points
  - 9th: 2 points
  - 10th: 1 point
- Additional Points:
  - Pole Position: 1 point
  - Fastest Lap: 1 point

### Team Points
- Based on best two results in each race:
  - 1st: 10 points
  - 2nd: 8 points
  - 3rd: 6 points
  - 4th: 4 points
  - 5th: 3 points
- Team points are calculated per race and summed across all races

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up Firebase credentials:
   - Place your Firebase service account key in the project root
   - Update the path in `app.py` if needed

4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Access the admin dashboard at `http://localhost:5000/admin`
2. Log in with the password: `Euro4mula1`
3. Use the dashboard to:
   - Manage drivers and teams
   - Schedule races
   - Record results
   - Update points automatically

## Data Structure

### Drivers
- Driver Number (unique identifier)
- First Name
- Last Name
- Nationality
- Team
- Points
- Status

### Teams
- Team ID (unique identifier)
- Team Name
- Country
- Points

### Races
- Round Number
- Circuit
- City
- Country
- Race Schedule (up to 3 races per round)

### Results
- Round Number
- Circuit
- Race Results (up to 3 races)
  - Pole Position
  - Finishing Positions
  - Fastest Laps

## Recent Updates

- Added automatic points calculation for drivers and teams
- Implemented sorting of drivers and teams by points
- Improved race table display with clear date and time formatting
- Enhanced team points calculation based on best two results per race
- Added proper number type handling for points in database 