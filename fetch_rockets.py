#!/usr/bin/env python3
"""
SpaceX Rockets Data Fetcher
Fetches rocket data from SpaceX API and stores in database
"""

import requests
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class SpaceXRocketsFetcher:
    def __init__(self):
        self.base_url = "https://api.spacexdata.com/v4"
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'spacex_db'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '')
        }
        
    def create_database_and_tables(self):
        """Create database and tables if they don't exist"""
        try:
            # Connect without database to create it
            connection = mysql.connector.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                user=self.db_config['user'],
                password=self.db_config['password']
            )
            
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.db_config['database']}")
            cursor.close()
            connection.close()
            
            # Connect to the database
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            # Create rockets table
            create_rockets_table = """
            CREATE TABLE IF NOT EXISTS rockets (
                id VARCHAR(50) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description TEXT,
                height_meters DECIMAL(10, 2),
                mass_kg INT,
                first_flight DATE,
                cost_per_launch BIGINT,
                success_rate_pct DECIMAL(5, 2),
                active BOOLEAN,
                stages INT,
                boosters INT,
                wikipedia_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            
            cursor.execute(create_rockets_table)
            connection.commit()
            print("Database and tables created successfully")
            
        except Error as e:
            print(f"Error creating database: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def fetch_rockets_data(self):
        """Fetch rockets data from SpaceX API"""
        try:
            response = requests.get(f"{self.base_url}/rockets")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching rockets data: {e}")
            return None
    
    def save_rockets_to_db(self, rockets_data):
        """Save rockets data to database"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            insert_query = """
            INSERT INTO rockets (
                id, name, description, height_meters, mass_kg, first_flight,
                cost_per_launch, success_rate_pct, active, stages, boosters, wikipedia_url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                description = VALUES(description),
                height_meters = VALUES(height_meters),
                mass_kg = VALUES(mass_kg),
                first_flight = VALUES(first_flight),
                cost_per_launch = VALUES(cost_per_launch),
                success_rate_pct = VALUES(success_rate_pct),
                active = VALUES(active),
                stages = VALUES(stages),
                boosters = VALUES(boosters),
                wikipedia_url = VALUES(wikipedia_url)
            """
            
            rockets_saved = 0
            for rocket in rockets_data:
                rocket_data = (
                    rocket['id'],
                    rocket['name'],
                    rocket['description'],
                    rocket.get('height', {}).get('meters'),
                    rocket.get('mass', {}).get('kg'),
                    rocket.get('first_flight'),
                    rocket.get('cost_per_launch'),
                    rocket.get('success_rate_pct'),
                    rocket.get('active', False),
                    rocket.get('stages'),
                    rocket.get('boosters'),
                    rocket.get('wikipedia')
                )
                
                cursor.execute(insert_query, rocket_data)
                rockets_saved += 1
            
            connection.commit()
            print(f"Successfully saved {rockets_saved} rockets to database")
            
        except Error as e:
            print(f"Error saving to database: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def run(self):
        """Main execution method"""
        print("Starting SpaceX Rockets data fetch...")
        
        # Create database and tables
        self.create_database_and_tables()
        
        # Fetch rockets data
        rockets_data = self.fetch_rockets_data()
        if rockets_data:
            print(f"Fetched {len(rockets_data)} rockets from SpaceX API")
            
            # Save to database
            self.save_rockets_to_db(rockets_data)
            
            print("Rocket data fetch completed successfully!")
        else:
            print("Failed to fetch rockets data")

if __name__ == "__main__":
    fetcher = SpaceXRocketsFetcher()
    fetcher.run()