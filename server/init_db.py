from app import app, db, Driver, Team, Circuit, Race, RaceResult, Car, DriverTeamContract
from datetime import datetime, date

def init_db():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # Add Teams (2025 season)
        teams = [
            Team(
                name='Red Bull Racing',
                nationality='Austrian',
                engine_supplier='Honda RBPT',
                first_entry_year=2005,
                championships_won=7,  # Updated for 2024 win
                base_location='Milton Keynes, United Kingdom',
                technical_director='Pierre Waché',
                team_principal='Christian Horner'
            ),
            Team(
                name='Mercedes-AMG Petronas',
                nationality='German',
                engine_supplier='Mercedes',
                first_entry_year=2010,
                championships_won=8,
                base_location='Brackley, United Kingdom',
                technical_director='James Allison',
                team_principal='Toto Wolff'
            ),
            Team(
                name='Ferrari',
                nationality='Italian',
                engine_supplier='Ferrari',
                first_entry_year=1950,
                championships_won=16,
                base_location='Maranello, Italy',
                technical_director='Enrico Cardile',
                team_principal='Frédéric Vasseur'
            ),
            Team(
                name='McLaren',
                nationality='British',
                engine_supplier='Mercedes',
                first_entry_year=1966,
                championships_won=8,
                base_location='Woking, United Kingdom',
                technical_director='Peter Prodromou',
                team_principal='Andrea Stella'
            )
        ]
        db.session.add_all(teams)
        db.session.commit()

        # Add Drivers (2025 stats)
        drivers = [
            Driver(
                name='Max Verstappen',
                nationality='Dutch',
                date_of_birth=date(1997, 9, 30),
                number=1,
                code='VER',
                championships_won=4,  # Updated for 2024 win
                race_wins=57,
                active_status=True,
                first_race_date=date(2015, 3, 15),
                total_points=2711.5
            ),
            Driver(
                name='Liam Lawson',
                nationality='New Zealander',
                date_of_birth=date(2002, 2, 11),
                number=15,
                code='LAW',
                championships_won=0,
                race_wins=0,
                active_status=True,
                first_race_date=date(2023, 9, 3),  # First race at Zandvoort
                total_points=2.0
            ),
            Driver(
                name='George Russell',
                nationality='British',
                date_of_birth=date(1998, 2, 15),
                number=63,
                code='RUS',
                championships_won=0,
                race_wins=1,
                active_status=True,
                first_race_date=date(2019, 3, 17),
                total_points=452.0
            ),
            Driver(
                name='Kimi Antonelli',
                nationality='Italian',
                date_of_birth=date(2006, 8, 25),
                number=23,
                code='ANT',
                championships_won=0,
                race_wins=0,
                active_status=True,
                first_race_date=date(2025, 3, 22),  # First race at Australian GP
                total_points=0.0
            ),
            Driver(
                name='Lewis Hamilton',
                nationality='British',
                date_of_birth=date(1985, 1, 7),
                number=44,
                code='HAM',
                championships_won=7,
                race_wins=103,
                active_status=True,
                first_race_date=date(2007, 3, 18),
                total_points=4639.5
            ),
            Driver(
                name='Charles Leclerc',
                nationality='Monégasque',
                date_of_birth=date(1997, 10, 16),
                number=16,
                code='LEC',
                championships_won=0,
                race_wins=5,
                active_status=True,
                first_race_date=date(2018, 3, 25),
                total_points=1035.0
            ),
            Driver(
                name='Lando Norris',
                nationality='British',
                date_of_birth=date(1999, 11, 13),
                number=4,
                code='NOR',
                championships_won=0,
                race_wins=1,  # First win in 2024
                active_status=True,
                first_race_date=date(2019, 3, 17),
                total_points=674.0
            ),
            Driver(
                name='Oscar Piastri',
                nationality='Australian',
                date_of_birth=date(2001, 4, 6),
                number=81,
                code='PIA',
                championships_won=0,
                race_wins=0,
                active_status=True,
                first_race_date=date(2023, 3, 5),
                total_points=97.0
            )
        ]
        db.session.add_all(drivers)
        db.session.commit()

        # Add Cars (2025 models)
        cars = [
            Car(
                team_id=1,  # Red Bull
                season=2025,
                model_name='RB21',
                engine_specification='Honda RBPT',
                total_wins=0,
                total_poles=0
            ),
            Car(
                team_id=2,  # Mercedes
                season=2025,
                model_name='W16',
                engine_specification='Mercedes',
                total_wins=0,
                total_poles=0
            ),
            Car(
                team_id=3,  # Ferrari
                season=2025,
                model_name='SF-25',
                engine_specification='Ferrari',
                total_wins=0,
                total_poles=0
            ),
            Car(
                team_id=4,  # McLaren
                season=2025,
                model_name='MCL39',
                engine_specification='Mercedes',
                total_wins=2,
                total_poles=2
            )
        ]
        db.session.add_all(cars)
        db.session.commit()

        # Add Circuits (2025 calendar)
        circuits = [
            Circuit(
                name='Albert Park Circuit',
                location='Melbourne',
                country='Australia',
                length_km=5.278,
                number_of_laps=58,
                circuit_type='Street',
                number_of_drs_zones=4,
                first_gp_held=1996
            ),
            Circuit(
                name='Shanghai International Circuit',
                location='Shanghai',
                country='China',
                length_km=5.451,
                number_of_laps=56,
                circuit_type='Permanent',
                number_of_drs_zones=2,
                first_gp_held=2004
            ),
            Circuit(
                name='Suzuka International Racing Course',
                location='Suzuka',
                country='Japan',
                length_km=5.807,
                number_of_laps=53,
                circuit_type='Permanent',
                number_of_drs_zones=1,
                first_gp_held=1987
            )
        ]
        db.session.add_all(circuits)
        db.session.commit()

        # Add Races (2025 season start)
        races = [
            Race(
                season=2025,
                round_number=1,
                grand_prix_name='Australian Grand Prix',
                circuit_id=3,
                date=date(2025, 3, 16),
                weather_conditions='Rainy',
                safety_car_appearances=4,
                red_flags=0
            ),
            Race(
                season=2025,
                round_number=2,
                grand_prix_name='Chinese Grand Prix',
                circuit_id=4,
                date=date(2025, 3, 23),
                weather_conditions='Lightly Cloudy',
                safety_car_appearances=0,
                red_flags=0
            ),
            Race(
                season=2025,
                round_number=3,
                grand_prix_name='Japanese Grand Prix',
                circuit_id=5,
                date=date(2025, 4, 6),
                weather_conditions='Clear',
                safety_car_appearances=0,
                red_flags=0
            )
        ]
        db.session.add_all(races)
        db.session.commit()

        # Add Race Results (2025 season results)
        results = [
            # Australian GP Results
            RaceResult(
                race_id=1,
                driver_id=1,  # Verstappen
                team_id=1,  # Red Bull
                car_id=1,
                grid_position=3,
                finish_position=2,
                points_earned=18.0,
                laps_completed=58,
                status='Finished',
                gap_to_leader='+0.895'
            ),
            RaceResult(
                race_id=1,
                driver_id=2,  # Lawson
                team_id=1,  # Red Bull
                car_id=1,
                grid_position=18,
                finish_position=None,
                points_earned=0.0,
                laps_completed=58,
                status='DNF',
                gap_to_leader='DNF'
            ),
            RaceResult(
                race_id=1,
                driver_id=3,  # Russell
                team_id=2,  # Mercedes
                car_id=2,
                grid_position=4,
                finish_position=3,
                points_earned=15.0,
                laps_completed=58,
                status='Finished',
                gap_to_leader='+8.481'
            ),
            RaceResult(
                race_id=1,
                driver_id=4,  # Antonelli
                team_id=2,  # Mercedes
                car_id=2,
                grid_position=16,
                finish_position=4,
                points_earned=12.0,
                laps_completed=58,
                status='Finished',
                gap_to_leader='+10.135'
            ),
            RaceResult(
                race_id=1,
                driver_id=5,  # Hamilton
                team_id=3,  # Ferrari
                car_id=3,
                grid_position=8,
                finish_position=10,
                points_earned=1.0,
                laps_completed=58,
                status='Finished',
                gap_to_leader='+22.473'
            ),
            RaceResult(
                race_id=1,
                driver_id=6,  # Leclerc
                team_id=3,  # Ferrari
                car_id=3,
                grid_position=7,
                finish_position=8,
                points_earned=4.0,
                laps_completed=58,
                status='Finished',
                gap_to_leader='+19.826'
            ),
            RaceResult(
                race_id=1,
                driver_id=7,  # Norris
                team_id=4,  # McLaren
                car_id=4,
                grid_position=1,
                finish_position=1,
                points_earned=25.0,
                laps_completed=58,
                status='Finished',
                gap_to_leader='WINNER'
            ),
            RaceResult(
                race_id=1,
                driver_id=8,  # Piastri
                team_id=4,  # McLaren
                car_id=4,
                grid_position=2,
                finish_position=9,
                points_earned=2.0,
                laps_completed=58,
                status='Finished',
                gap_to_leader='+20.448'
            ),
            # Chinese GP Results
            RaceResult(
                race_id=2,
                driver_id=5,  # Hamilton
                team_id=3,  # Ferrari
                car_id=3,
                grid_position=5,
                finish_position=None,
                points_earned=8.0,
                laps_completed=56,
                status='DSQ',
                gap_to_leader='DSQ'
            ),
            RaceResult(
                race_id=2,
                driver_id=7,  # Norris
                team_id=4,  # McLaren
                car_id=4,
                grid_position=3,
                finish_position=2,
                points_earned=19.0,
                laps_completed=56,
                status='Finished',
                gap_to_leader='+9.748'
            ),
            RaceResult(
                race_id=2,
                driver_id=1,  # Verstappen
                team_id=1,  # Red Bull
                car_id=1,
                grid_position=4,
                finish_position=4,
                points_earned=18.0,
                laps_completed=56,
                status='Finished',
                gap_to_leader='+16.656'
            ),
            RaceResult(
                race_id=2,
                driver_id=2,  # Lawson
                team_id=1,  # Red Bull
                car_id=1,
                grid_position=20,
                finish_position=12,
                points_earned=0.0,
                laps_completed=56,
                status='Finished',
                gap_to_leader='+81.147'
            ),
            RaceResult(
                race_id=2,
                driver_id=3,  # Russell
                team_id=2,  # Mercedes
                car_id=2,
                grid_position=2,
                finish_position=3,
                points_earned=20.0,
                laps_completed=56,
                status='Finished',
                gap_to_leader='+11.097'
            ),
            RaceResult(
                race_id=2,
                driver_id=4,  # Antonelli
                team_id=2,  # Mercedes
                car_id=2,
                grid_position=8,
                finish_position=6,
                points_earned=10.0,
                laps_completed=56,
                status='Finished',
                gap_to_leader='+53.748'
            ),
            RaceResult(
                race_id=2,
                driver_id=6,  # Leclerc
                team_id=3,  # Ferrari
                car_id=3,
                grid_position=6,
                finish_position=None,
                points_earned=4.0,  # No points for DSQ
                laps_completed=56,
                status='DSQ',
                gap_to_leader='DSQ'
            ),
            RaceResult(
                race_id=2,
                driver_id=8,  # Piastri
                team_id=4,  # McLaren
                car_id=4,
                grid_position=1,
                finish_position=1,
                points_earned=32.0,
                laps_completed=56,
                status='Finished',
                gap_to_leader='WINNER'
            )
        ]
        db.session.add_all(results)
        db.session.commit()

        # Add Driver Team Contracts (2025 season)
        contracts = [
            DriverTeamContract(
                driver_id=1,  # Verstappen
                team_id=1,  # Red Bull
                start_date=date(2024, 1, 1),
                end_date=date(2028, 12, 31),
                status='Active'
            ),
            DriverTeamContract(
                driver_id=2,  # Lawson
                team_id=1,  # Red Bull
                start_date=date(2025, 1, 1),
                end_date=date(2025, 12, 31),
                status='Active'
            ),
            DriverTeamContract(
                driver_id=3,  # Russell
                team_id=2,  # Mercedes
                start_date=date(2024, 1, 1),
                end_date=date(2025, 12, 31),
                status='Active'
            ),
            DriverTeamContract(
                driver_id=4,  # Antonelli
                team_id=2,  # Mercedes
                start_date=date(2025, 1, 1),
                end_date=date(2025, 12, 31),
                status='Active'
            ),
            DriverTeamContract(
                driver_id=5,  # Hamilton
                team_id=3,  # Ferrari
                start_date=date(2025, 1, 1),
                end_date=date(2026, 12, 31),
                status='Active'
            ),
            DriverTeamContract(
                driver_id=6,  # Leclerc
                team_id=3,  # Ferrari
                start_date=date(2024, 1, 1),
                end_date=date(2026, 12, 31),
                status='Active'
            ),
            DriverTeamContract(
                driver_id=7,  # Norris
                team_id=4,  # McLaren
                start_date=date(2024, 1, 1),
                end_date=date(2026, 12, 31),
                status='Active'
            ),
            DriverTeamContract(
                driver_id=8,  # Piastri
                team_id=4,  # McLaren
                start_date=date(2024, 1, 1),
                end_date=date(2026, 12, 31),
                status='Active'
            )
        ]
        db.session.add_all(contracts)
        db.session.commit()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!") 