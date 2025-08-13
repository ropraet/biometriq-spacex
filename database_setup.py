#!/usr/bin/env python3
"""
Database setup script for SpaceX application
Creates all necessary tables including crew stars feature
"""

import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class DatabaseSetup:
    def __init__(self):
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'spacex_db'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '')
        }
    
    def create_all_tables(self):
        """Create all necessary tables for the application"""
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
            
            # Create crew_stars table for the optional starring feature
            create_crew_stars_table = """
            CREATE TABLE IF NOT EXISTS crew_stars (
                id INT AUTO_INCREMENT PRIMARY KEY,
                crew_id VARCHAR(50) NOT NULL,
                crew_name VARCHAR(100) NOT NULL,
                nickname VARCHAR(100),
                image_url VARCHAR(255),
                wikipedia_url VARCHAR(255),
                starred_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY unique_crew (crew_id)
            )
            """
            
            cursor.execute(create_rockets_table)
            cursor.execute(create_crew_stars_table)
            
            connection.commit()
            print("All database tables created successfully!")
            
        except Error as e:
            print(f"Error creating tables: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    db_setup = DatabaseSetup()
    db_setup.create_all_tables()