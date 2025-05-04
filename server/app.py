from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from sqlalchemy import text

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS with credentials support

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///f1_database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ASCPAKEN@#$^@32435da'  # Change this to a secure secret key
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Allow cookies in cross-origin requests
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Driver(db.Model):
    driver_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    number = db.Column(db.Integer, unique=True)
    code = db.Column(db.String(3), unique=True)  # Driver's 3-letter code (e.g., 'HAM')
    championships_won = db.Column(db.Integer, default=0)
    race_wins = db.Column(db.Integer, default=0)  # Total career race wins
    active_status = db.Column(db.Boolean, default=True)
    first_race_date = db.Column(db.Date)
    total_points = db.Column(db.Float, default=0)
    # Relationships
    race_results = db.relationship('RaceResult', back_populates='driver')
    qualifying_results = db.relationship('Qualifying', back_populates='driver')
    team_contracts = db.relationship('DriverTeamContract', back_populates='driver')

class Team(db.Model):
    team_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    nationality = db.Column(db.String(50), nullable=False)
    engine_supplier = db.Column(db.String(50))
    first_entry_year = db.Column(db.Integer)
    championships_won = db.Column(db.Integer, default=0)
    base_location = db.Column(db.String(100))
    technical_director = db.Column(db.String(100))
    team_principal = db.Column(db.String(100))
    # Relationships
    race_results = db.relationship('RaceResult', back_populates='team')
    cars = db.relationship('Car', back_populates='team')
    driver_contracts = db.relationship('DriverTeamContract', back_populates='team')

class Circuit(db.Model):
    circuit_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    length_km = db.Column(db.Float, nullable=False)
    lap_record = db.Column(db.Float)  # in seconds
    lap_record_holder_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'))
    number_of_laps = db.Column(db.Integer)
    circuit_type = db.Column(db.String(50))  # Street, Permanent, Hybrid
    number_of_drs_zones = db.Column(db.Integer, default=2)
    first_gp_held = db.Column(db.Integer)  # Year
    # Relationships
    races = db.relationship('Race', back_populates='circuit')

class Race(db.Model):
    race_id = db.Column(db.Integer, primary_key=True)
    season = db.Column(db.Integer, nullable=False)
    round_number = db.Column(db.Integer, nullable=False)
    grand_prix_name = db.Column(db.String(100), nullable=False)
    circuit_id = db.Column(db.Integer, db.ForeignKey('circuit.circuit_id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    weather_conditions = db.Column(db.String(50))
    safety_car_appearances = db.Column(db.Integer, default=0)
    red_flags = db.Column(db.Integer, default=0)
    # Relationships
    circuit = db.relationship('Circuit', back_populates='races')
    race_results = db.relationship('RaceResult', back_populates='race')
    qualifying = db.relationship('Qualifying', back_populates='race')
    pit_stops = db.relationship('PitStop', back_populates='race')

class RaceResult(db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.race_id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.car_id'), nullable=False)
    grid_position = db.Column(db.Integer)
    finish_position = db.Column(db.Integer)
    points_earned = db.Column(db.Float, default=0)
    laps_completed = db.Column(db.Integer)
    status = db.Column(db.String(50))  # Finished, DNF, DSQ, DNS
    gap_to_leader = db.Column(db.String(20))  # Time or number of laps
    # Relationships
    race = db.relationship('Race', back_populates='race_results')
    driver = db.relationship('Driver', back_populates='race_results')
    team = db.relationship('Team', back_populates='race_results')
    car = db.relationship('Car', back_populates='race_results')

    def update_driver_wins(self):
        """Update the driver's total race wins after a result is added or modified"""
        if self.finish_position == 1 and self.status == 'Finished' and self.driver is not None:
            self.driver.race_wins = db.session.query(RaceResult).filter(
                RaceResult.driver_id == self.driver_id,
                RaceResult.finish_position == 1,
                RaceResult.status == 'Finished'
            ).count()
            db.session.commit()

# SQLAlchemy event listeners to automatically update race wins
@db.event.listens_for(RaceResult, 'after_insert')
def update_wins_after_insert(mapper, connection, target):
    target.update_driver_wins()

@db.event.listens_for(RaceResult, 'after_update')
def update_wins_after_update(mapper, connection, target):
    target.update_driver_wins()

class Qualifying(db.Model):
    qualifying_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.race_id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'), nullable=False)
    q1_time = db.Column(db.Float)  # in seconds
    q2_time = db.Column(db.Float)
    q3_time = db.Column(db.Float)
    final_position = db.Column(db.Integer)
    weather_conditions = db.Column(db.String(50))
    tire_compound_used = db.Column(db.String(20))
    # Relationships
    race = db.relationship('Race', back_populates='qualifying')
    driver = db.relationship('Driver', back_populates='qualifying_results')

class Car(db.Model):
    car_id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    season = db.Column(db.Integer, nullable=False)
    model_name = db.Column(db.String(100))
    engine_specification = db.Column(db.String(100))
    total_wins = db.Column(db.Integer, default=0)
    total_poles = db.Column(db.Integer, default=0)
    # Relationships
    team = db.relationship('Team', back_populates='cars')
    race_results = db.relationship('RaceResult', back_populates='car')

class PitStop(db.Model):
    pitstop_id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('race.race_id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'), nullable=False)
    stop_number = db.Column(db.Integer, nullable=False)
    lap_number = db.Column(db.Integer, nullable=False)
    stop_time = db.Column(db.Float, nullable=False)  # in seconds
    tire_compound = db.Column(db.String(20))
    # Relationships
    race = db.relationship('Race', back_populates='pit_stops')

class DriverTeamContract(db.Model):
    contract_id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.driver_id'), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.team_id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20))  # Active, Terminated, Completed
    # Relationships
    driver = db.relationship('Driver', back_populates='team_contracts')
    team = db.relationship('Team', back_populates='driver_contracts')

# Create all database tables
with app.app_context():
    db.create_all()

@app.route('/hello')
def hello_world():
    return {'hello': "Welcome to F1 Race Management System!"}

@app.route('/api/drivers/standings')
def get_driver_standings():
    try:
        # Using prepared statement for complex standings calculation
        query = text("""
            SELECT 
                d.driver_id,
                d.name,
                d.nationality,
                d.number,
                d.code,
                COALESCE(SUM(r.points_earned), 0) as total_points,
                COUNT(CASE WHEN r.finish_position = 1 THEN 1 END) as total_wins,
                COUNT(CASE WHEN r.grid_position = 1 THEN 1 END) as pole_positions,
                COUNT(CASE WHEN r.finish_position <= 3 THEN 1 END) as podiums
            FROM driver d
            LEFT JOIN race_result r ON d.driver_id = r.driver_id
            GROUP BY d.driver_id, d.name, d.nationality, d.number, d.code
            ORDER BY total_points DESC
        """)
        
        results = db.session.execute(query)
        standings = [
            {
                'driver_id': r.driver_id,
                'name': r.name,
                'nationality': r.nationality,
                'number': r.number,
                'code': r.code,
                'total_points': float(r.total_points),
                'total_wins': r.total_wins,
                'pole_positions': r.pole_positions,
                'podiums': r.podiums
            } for r in results
        ]
        
        return jsonify(standings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams/standings')
def get_team_standings():
    try:
        # Using prepared statement for complex standings calculation
        query = text("""
            SELECT 
                t.team_id,
                t.name,
                t.nationality,
                COALESCE(SUM(r.points_earned), 0) as total_points,
                COUNT(CASE WHEN r.finish_position = 1 THEN 1 END) as total_wins,
                COUNT(CASE WHEN r.grid_position = 1 THEN 1 END) as pole_positions,
                COUNT(CASE WHEN r.finish_position <= 3 THEN 1 END) as podiums
            FROM team t
            LEFT JOIN race_result r ON t.team_id = r.team_id
            GROUP BY t.team_id, t.name, t.nationality
            ORDER BY total_points DESC
        """)
        
        results = db.session.execute(query)
        standings = [
            {
                'team_id': r.team_id,
                'name': r.name,
                'nationality': r.nationality,
                'total_points': float(r.total_points),
                'total_wins': r.total_wins,
                'pole_positions': r.pole_positions,
                'podiums': r.podiums
            } for r in results
        ]
        
        return jsonify(standings)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/season/statistics')
def get_season_statistics():
    try:
        # Get total races
        total_races = db.session.query(Race).count()

        # Get pole positions per driver
        pole_positions = db.session.query(
            Driver.name,
            db.func.count(RaceResult.result_id).label('count')
        ).join(RaceResult).filter(
            RaceResult.grid_position == 1
        ).group_by(Driver.name).all()

        # Get podium finishes per driver
        podium_finishes = db.session.query(
            Driver.name,
            db.func.count(RaceResult.result_id).label('count')
        ).join(RaceResult).filter(
            RaceResult.finish_position <= 3,
            RaceResult.status == 'Finished'
        ).group_by(Driver.name).all()

        # Format the response
        stats = {
            'totalRaces': total_races,
            'polePositions': {name: count for name, count in pole_positions},
            'podiumFinishes': {name: count for name, count in podium_finishes}
        }
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Helper function to convert RaceResult to dictionary
def race_result_to_dict(result):
    return {
        'result_id': result.result_id,
        'race_id': result.race_id,
        'driver_id': result.driver_id,
        'team_id': result.team_id,
        'car_id': result.car_id,
        'grid_position': result.grid_position,
        'finish_position': result.finish_position,
        'points_earned': float(result.points_earned) if result.points_earned else 0.0,
        'laps_completed': result.laps_completed,
        'status': result.status,
        'gap_to_leader': result.gap_to_leader
    }

# Get a single race result by ID
@app.route('/api/race-results/<int:result_id>', methods=['GET'])
def get_race_result(result_id):
    try:
        result = RaceResult.query.get_or_404(result_id)
        return jsonify(race_result_to_dict(result))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Create a new race result
@app.route('/api/race-results', methods=['POST'])
@login_required
def create_race_result():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['race_id', 'driver_id', 'team_id', 'car_id']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        new_result = RaceResult(
            race_id=data['race_id'],
            driver_id=data['driver_id'],
            team_id=data['team_id'],
            car_id=data['car_id'],
            grid_position=data.get('grid_position'),
            finish_position=data.get('finish_position'),
            points_earned=data.get('points_earned', 0.0),
            laps_completed=data.get('laps_completed'),
            status=data.get('status', 'Finished'),
            gap_to_leader=data.get('gap_to_leader')
        )
        
        db.session.add(new_result)
        db.session.commit()
        
        return jsonify(race_result_to_dict(new_result)), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid foreign key or constraint violation'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update an existing race result
@app.route('/api/race-results/<int:result_id>', methods=['PUT'])
@login_required
def update_race_result(result_id):
    try:
        result = RaceResult.query.get_or_404(result_id)
        data = request.get_json()
        
        # Update fields if they exist in the request
        if 'grid_position' in data:
            result.grid_position = data['grid_position']
        if 'finish_position' in data:
            result.finish_position = data['finish_position']
        if 'points_earned' in data:
            result.points_earned = data['points_earned']
        if 'laps_completed' in data:
            result.laps_completed = data['laps_completed']
        if 'status' in data:
            result.status = data['status']
        if 'gap_to_leader' in data:
            result.gap_to_leader = data['gap_to_leader']
        
        # Update driver wins
        result.update_driver_wins()
        
        db.session.commit()
        return jsonify(race_result_to_dict(result))
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Invalid foreign key or constraint violation'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete a race result
@app.route('/api/race-results/<int:result_id>', methods=['DELETE'])
@login_required
def delete_race_result(result_id):
    try:
        result = RaceResult.query.get_or_404(result_id)
        db.session.delete(result)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Get all race results
@app.route('/api/race-results', methods=['GET'])
def get_race_results():
    try:
        results = db.session.query(
            RaceResult,
            Race.grand_prix_name,
            Driver.name.label('driver_name'),
            Team.name.label('team_name')
        ).join(
            Race, RaceResult.race_id == Race.race_id
        ).join(
            Driver, RaceResult.driver_id == Driver.driver_id
        ).join(
            Team, RaceResult.team_id == Team.team_id
        ).order_by(
            Race.date.desc(),
            RaceResult.finish_position
        ).all()

        # Convert to list of dictionaries with additional information
        results_list = [{
            'result_id': result.RaceResult.result_id,
            'race_id': result.RaceResult.race_id,
            'race_name': result.grand_prix_name,
            'driver_id': result.RaceResult.driver_id,
            'driver_name': result.driver_name,
            'team_id': result.RaceResult.team_id,
            'team_name': result.team_name,
            'car_id': result.RaceResult.car_id,
            'grid_position': result.RaceResult.grid_position,
            'finish_position': result.RaceResult.finish_position,
            'points_earned': float(result.RaceResult.points_earned) if result.RaceResult.points_earned else 0.0,
            'laps_completed': result.RaceResult.laps_completed,
            'status': result.RaceResult.status,
            'gap_to_leader': result.RaceResult.gap_to_leader
        } for result in results]
        
        return jsonify(results_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get list of all races
@app.route('/api/races', methods=['GET'])
def get_races():
    try:
        races = db.session.query(
            Race.race_id,
            Race.grand_prix_name,
            Race.season
        ).order_by(Race.date.desc()).all()
        
        races_list = [{
            'race_id': race.race_id,
            'name': f"{race.grand_prix_name} {race.season}"
        } for race in races]
        
        return jsonify(races_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get list of all drivers
@app.route('/api/drivers', methods=['GET'])
def get_drivers():
    try:
        drivers = db.session.query(
            Driver.driver_id,
            Driver.name,
            Driver.code
        ).order_by(Driver.name).all()
        
        drivers_list = [{
            'driver_id': driver.driver_id,
            'name': f"{driver.name} ({driver.code})"
        } for driver in drivers]
        
        return jsonify(drivers_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get list of all teams
@app.route('/api/teams', methods=['GET'])
def get_teams():
    try:
        teams = db.session.query(
            Team.team_id,
            Team.name
        ).order_by(Team.name).all()
        
        teams_list = [{
            'team_id': team.team_id,
            'name': team.name
        } for team in teams]
        
        return jsonify(teams_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get driver's current team and car
@app.route('/api/drivers/<int:driver_id>/current-team', methods=['GET'])
def get_driver_current_team(driver_id):
    try:
        # Get the driver's most recent team contract
        current_contract = db.session.query(DriverTeamContract).filter(
            DriverTeamContract.driver_id == driver_id,
            DriverTeamContract.status == 'Active'
        ).first()

        if not current_contract:
            return jsonify({'error': 'No active team contract found for driver'}), 404

        # Get the team's current car
        current_car = db.session.query(Car).filter(
            Car.team_id == current_contract.team_id,
            Car.season == datetime.now().year
        ).first()

        if not current_car:
            return jsonify({'error': 'No current car found for team'}), 404

        return jsonify({
            'team_id': current_contract.team_id,
            'car_id': current_car.car_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400

        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 400

        user = User(username=data['username'])
        user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Missing username or password'}), 400

        user = User.query.filter_by(username=data['username']).first()
        if user and user.check_password(data['password']):
            login_user(user)
            return jsonify({'message': 'Logged in successfully', 'is_admin': user.is_admin}), 200
        return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/auth/logout', methods=['GET', 'POST'])
def logout():
    if current_user.is_authenticated:
        logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/auth/status')
def auth_status():
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'username': current_user.username,
            'is_admin': current_user.is_admin
        })
    return jsonify({'authenticated': False})

@app.cli.command("create-admin")
def create_admin():
    """Create an admin user."""
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    
    try:
        admin = User(username=username, is_admin=True)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin user '{username}' created successfully!")
    except Exception as e:
        db.session.rollback()
        print(f"Error creating admin user: {str(e)}")

@app.route('/api/races/<int:race_id>/report', methods=['GET'])
def get_race_report(race_id):
    try:
        # Using prepared statement for race report
        query = text("""
            SELECT 
                r.race_id,
                r.grand_prix_name,
                r.season,
                r.date,
                r.weather_conditions,
                r.safety_car_appearances,
                r.red_flags,
                rr.result_id,
                rr.grid_position,
                rr.finish_position,
                rr.points_earned,
                rr.laps_completed,
                rr.status,
                rr.gap_to_leader,
                d.driver_id,
                d.name as driver_name,
                d.code as driver_code,
                d.nationality as driver_nationality,
                d.number as driver_number,
                t.team_id,
                t.name as team_name,
                t.nationality as team_nationality
            FROM race r
            LEFT JOIN race_result rr ON r.race_id = rr.race_id
            LEFT JOIN driver d ON rr.driver_id = d.driver_id
            LEFT JOIN team t ON rr.team_id = t.team_id
            WHERE r.race_id = :race_id
            ORDER BY rr.finish_position
        """)
        
        results = db.session.execute(query, {'race_id': race_id})
        
        # Process results
        race_report = {
            'race_details': None,
            'results': []
        }
        
        for row in results:
            if not race_report['race_details']:
                race_report['race_details'] = {
                    'name': row.grand_prix_name,
                    'season': row.season,
                    'date': row.date,
                    'weather_conditions': row.weather_conditions,
                    'safety_car_appearances': row.safety_car_appearances,
                    'red_flags': row.red_flags
                }
            
            if row.result_id:  # Only add if there are results
                race_report['results'].append({
                    'driver': {
                        'name': row.driver_name,
                        'code': row.driver_code,
                        'nationality': row.driver_nationality,
                        'number': row.driver_number
                    },
                    'team': {
                        'name': row.team_name,
                        'nationality': row.team_nationality
                    },
                    'performance': {
                        'grid_position': row.grid_position,
                        'finish_position': row.finish_position,
                        'points_earned': float(row.points_earned) if row.points_earned else 0.0,
                        'laps_completed': row.laps_completed,
                        'status': row.status,
                        'gap_to_leader': row.gap_to_leader
                    }
                })
        
        if not race_report['race_details']:
            return jsonify({'error': 'Race not found'}), 404
            
        return jsonify(race_report)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

application = app

if __name__ == '__main__':
    app.run()