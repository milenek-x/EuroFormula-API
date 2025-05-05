from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import pandas as pd
import io
import os
from datetime import datetime
import json

app = Flask(__name__, static_folder='static')
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your-secret-key-here')  # Use environment variable in production

# Initialize Firebase Admin
cred = credentials.Certificate({
    "type": os.environ.get('FIREBASE_TYPE'),
    "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
    "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.environ.get('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
    "auth_uri": os.environ.get('FIREBASE_AUTH_URI'),
    "token_uri": os.environ.get('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER_CERT_URL'),
    "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_CERT_URL')
})

# Initialize Firebase only if it hasn't been initialized
if not firebase_admin._apps:
    initialize_app(cred)
db = firestore.client()

# Collections
DRIVERS = 'drivers'
TEAMS = 'teams'
RACES = 'races'
RESULTS = 'results'

# Points allocation constants
DRIVER_POINTS = {
    '1': 25,
    '2': 18,
    '3': 15,
    '4': 12,
    '5': 10,
    '6': 8,
    '7': 6,
    '8': 4,
    '9': 2,
    '10': 1,
    'pole': 1,
    'fastest_lap': 1
}

TEAM_POINTS = {
    '1': 10,
    '2': 8,
    '3': 6,
    '4': 4,
    '5': 3
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == 'Euro4mula1':
            session['logged_in'] = True
            return redirect(url_for('admin'))
        return render_template('login.html', error='Invalid password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('admin.html')

# API endpoints for data retrieval
@app.route('/api/drivers')
def get_drivers():
    drivers = []
    docs = db.collection(DRIVERS).stream()
    for doc in docs:
        drivers.append(doc.to_dict())
    # Sort drivers by points in descending order
    drivers.sort(key=lambda x: x.get('points', 0), reverse=True)
    return jsonify(drivers)

@app.route('/api/teams')
def get_teams():
    teams = []
    docs = db.collection(TEAMS).stream()
    for doc in docs:
        team_data = doc.to_dict()
        team_data['teamId'] = doc.id
        teams.append(team_data)
    return jsonify(teams)

@app.route('/api/races')
def get_races():
    races = []
    docs = db.collection(RACES).stream()
    for doc in docs:
        races.append(doc.to_dict())
    return jsonify(races)

@app.route('/api/results')
def get_results():
    results = []
    docs = db.collection(RESULTS).stream()
    for doc in docs:
        results.append(doc.to_dict())
    return jsonify(results)

@app.route('/api/drivers/<driver_number>', methods=['GET'])
def get_driver(driver_number):
    try:
        doc = db.collection(DRIVERS).document(driver_number).get()
        if doc.exists:
            return jsonify(doc.to_dict())
        return jsonify({'error': 'Driver not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CRUD operations for drivers
@app.route('/api/drivers', methods=['POST'])
def create_driver():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    doc_ref = db.collection(DRIVERS).document(str(data['driverNumber']))
    doc_ref.set(data)
    return jsonify({'success': True})

@app.route('/api/drivers/<driver_number>', methods=['PUT'])
def update_driver(driver_number):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    doc_ref = db.collection(DRIVERS).document(driver_number)
    doc_ref.update(data)
    return jsonify({'success': True})

@app.route('/api/drivers/<driver_number>', methods=['DELETE'])
def delete_driver(driver_number):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    db.collection(DRIVERS).document(driver_number).delete()
    return jsonify({'success': True})

# CRUD operations for teams
@app.route('/api/teams', methods=['POST'])
def create_team():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    doc_ref = db.collection(TEAMS).document(data['teamId'])
    doc_ref.set(data)
    return jsonify({'success': True})

@app.route('/api/teams/<team_id>', methods=['PUT'])
def update_team(team_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    doc_ref = db.collection(TEAMS).document(team_id)
    doc_ref.update(data)
    return jsonify({'success': True})

@app.route('/api/teams/<team_id>', methods=['DELETE'])
def delete_team(team_id):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    db.collection(TEAMS).document(team_id).delete()
    return jsonify({'success': True})

@app.route('/api/teams/<team_id>', methods=['GET'])
def get_team(team_id):
    try:
        doc = db.collection(TEAMS).document(team_id).get()
        if doc.exists:
            return jsonify(doc.to_dict())
        return jsonify({'error': 'Team not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# CRUD operations for races
@app.route('/api/races', methods=['POST'])
def create_race():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    doc_ref = db.collection(RACES).document(str(data['round']))
    doc_ref.set(data)
    return jsonify({'success': True})

@app.route('/api/races/<round>', methods=['GET'])
def get_race(round):
    try:
        doc = db.collection(RACES).document(round).get()
        if doc.exists:
            return jsonify(doc.to_dict())
        return jsonify({'error': 'Race not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/races/<round>', methods=['PUT'])
def update_race(round):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    doc_ref = db.collection(RACES).document(round)
    doc_ref.update(data)
    return jsonify({'success': True})

@app.route('/api/races/<round>', methods=['DELETE'])
def delete_race(round):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    db.collection(RACES).document(round).delete()
    return jsonify({'success': True})

# CRUD operations for results
@app.route('/api/results', methods=['POST'])
def create_result():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    doc_ref = db.collection(RESULTS).document(str(data['round']))
    doc_ref.set(data)
    return jsonify({'success': True})

@app.route('/api/results/<round>', methods=['GET'])
def get_result(round):
    try:
        doc = db.collection(RESULTS).document(round).get()
        if doc.exists:
            return jsonify(doc.to_dict())
        return jsonify({'error': 'Result not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/results/<round>', methods=['PUT'])
def update_result(round):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    data = request.json
    doc_ref = db.collection(RESULTS).document(round)
    doc_ref.update(data)
    return jsonify({'success': True})

@app.route('/api/results/<round>', methods=['DELETE'])
def delete_result(round):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    db.collection(RESULTS).document(round).delete()
    return jsonify({'success': True})

# Export and Import functionality
@app.route('/api/export/<collection>')
def export_collection(collection):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    docs = db.collection(collection).stream()
    data = [doc.to_dict() for doc in docs]
    df = pd.DataFrame(data)
    
    output = io.BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    
    return send_file(
        output,
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'{collection}.csv'
    )

@app.route('/api/import/<collection>', methods=['POST'])
def import_collection(collection):
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV'}), 400
    
    df = pd.read_csv(file)
    data = df.to_dict('records')
    
    batch = db.batch()
    for record in data:
        if collection == DRIVERS:
            doc_ref = db.collection(collection).document(str(record['driverNumber']))
        elif collection == TEAMS:
            doc_ref = db.collection(collection).document(record['teamId'])
        elif collection in [RACES, RESULTS]:
            doc_ref = db.collection(collection).document(str(record['round']))
        batch.set(doc_ref, record)
    
    batch.commit()
    return jsonify({'success': True})

@app.route('/api/results/update-points', methods=['POST'])
def update_points():
    try:
        print("\n=== Points Calculation ===")
        
        # Get all results
        results_ref = db.collection('results')
        results = results_ref.get()
        
        # Dictionary to store driver and team points
        driver_points = {}
        team_points = {}  # Store total points for each team
        
        # Process each result
        for result in results:
            result_data = result.to_dict()
            round_num = result_data.get('round')
            print(f"\nRound {round_num} at {result_data.get('circuit')}:")
            
            # Process each race in the result
            races = result_data.get('races', [])
            for race in races:
                race_number = race.get('race_number', 1)
                print(f"\nRace {race_number}:")
                
                # Process pole position
                pole_position = race.get('pole_position')
                if pole_position:
                    pole_position = str(pole_position)
                    if pole_position not in driver_points:
                        driver_points[pole_position] = 0
                    driver_points[pole_position] += DRIVER_POINTS['pole']
                    print(f"Driver #{pole_position} gets {DRIVER_POINTS['pole']} points for pole position")
                
                # Process race results
                race_results = race.get('results', [])
                print("\nRace Results:")
                
                # Dictionary to store team results for this race
                race_team_results = {}
                
                for result in race_results:
                    driver_number = str(result.get('driverNumber'))
                    position = result.get('position')
                    fastest_lap = result.get('fastest_lap', False)
                    
                    # Initialize driver points if not exists
                    if driver_number not in driver_points:
                        driver_points[driver_number] = 0
                    
                    # Calculate points for position
                    position_points = 0
                    if isinstance(position, str) and position.isdigit() and 1 <= int(position) <= 10:
                        position_points = DRIVER_POINTS[position]
                        driver_points[driver_number] += position_points
                        print(f"Driver #{driver_number}: Position {position} = {position_points} points")
                    
                    # Calculate points for fastest lap
                    if fastest_lap:
                        fastest_lap_points = DRIVER_POINTS['fastest_lap']
                        driver_points[driver_number] += fastest_lap_points
                        print(f"Driver #{driver_number}: Fastest Lap = {fastest_lap_points} points")
                    
                    # Print total points for this race
                    if position_points > 0 or fastest_lap:
                        print(f"Driver #{driver_number} total points this race: {position_points + (DRIVER_POINTS['fastest_lap'] if fastest_lap else 0)}")
                    
                    # Store team result if position is 1-5
                    if isinstance(position, str) and position.isdigit() and 1 <= int(position) <= 5:
                        # Get driver's team from the drivers collection
                        driver_doc = db.collection('drivers').document(driver_number).get()
                        if driver_doc.exists:
                            driver_data = driver_doc.to_dict()
                            team_name = driver_data.get('teamName')
                            if team_name:
                                if team_name not in race_team_results:
                                    race_team_results[team_name] = []
                                race_team_results[team_name].append({
                                    'position': int(position),
                                    'points': TEAM_POINTS[position]
                                })
                                print(f"Team {team_name} gets {TEAM_POINTS[position]} points for position {position}")
                
                # Calculate team points for this race
                print("\nTeam Points for this race:")
                for team_name, results in race_team_results.items():
                    # Sort results by points in descending order
                    results.sort(key=lambda x: x['points'], reverse=True)
                    # Take the best two results
                    best_results = results[:2]
                    race_points = sum(result['points'] for result in best_results)
                    
                    # Initialize team points if not exists
                    if team_name not in team_points:
                        team_points[team_name] = 0
                    
                    # Add points from this race to total
                    team_points[team_name] += race_points
                    
                    print(f"\nTeam {team_name} in Round {round_num} Race {race_number}:")
                    print(f"All results: {results}")
                    print(f"Best two results: {best_results}")
                    print(f"Points this race: {race_points}")
                    print(f"Total points so far: {team_points[team_name]}")
        
        # Print final points summary and update Firestore
        print("\n=== Final Points Summary ===")
        batch = db.batch()
        
        # Get all drivers and teams
        drivers_ref = db.collection('drivers')
        teams_ref = db.collection('teams')
        drivers = drivers_ref.get()
        teams = teams_ref.get()
        
        # Create maps of driver and team numbers to their documents
        driver_docs = {}
        team_docs = {}
        
        for doc in drivers:
            driver_data = doc.to_dict()
            driver_number = str(driver_data.get('driverNumber'))
            driver_docs[driver_number] = doc.reference
        
        for doc in teams:
            team_data = doc.to_dict()
            team_name = team_data.get('teamName')
            team_docs[team_name] = doc.reference
        
        # Update driver points
        print("\nDriver Points:")
        for driver_number, points in sorted(driver_points.items(), key=lambda x: int(x[0])):
            print(f"Driver #{driver_number}: {points} points")
            if driver_number in driver_docs:
                batch.update(driver_docs[driver_number], {'points': points})
                print(f"Updated points for Driver #{driver_number}")
            else:
                print(f"Warning: Driver #{driver_number} not found in database")
        
        # Update team points
        print("\nTeam Points:")
        for team_name, points in team_points.items():
            print(f"Team {team_name}: {points} points")
            if team_name in team_docs:
                batch.update(team_docs[team_name], {'teamPoints': points})
                print(f"Updated points for Team {team_name}")
            else:
                print(f"Warning: Team {team_name} not found in database")
        
        # Commit all updates
        batch.commit()
        print("\nAll points updated in database")
        
        # Fetch updated data
        updated_drivers = []
        updated_teams = []
        
        # Get updated driver data
        drivers = drivers_ref.stream()
        for doc in drivers:
            driver_data = doc.to_dict()
            updated_drivers.append(driver_data)
        
        # Get updated team data
        teams = teams_ref.stream()
        for doc in teams:
            team_data = doc.to_dict()
            team_data['teamId'] = doc.id
            updated_teams.append(team_data)
        
        # Sort drivers by points
        updated_drivers.sort(key=lambda x: x.get('points', 0), reverse=True)
        
        return jsonify({
            'message': 'Points updated successfully',
            'drivers': updated_drivers,
            'teams': updated_teams
        }), 200
        
    except Exception as e:
        print(f"Error in update_points: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
else:
    # This is for Vercel
    app = app 