#!/usr/bin/env python3
"""
SpaceX Web Application
A Flask web app to display SpaceX launches, crew members, and rocket data
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import mysql.connector
from mysql.connector import Error
import os
import math
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'spacex-secret-key-change-in-production')

class SpaceXAPI:
    def __init__(self):
        self.base_url = "https://api.spacexdata.com/v4"
        self.db_config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', 3306)),
            'database': os.getenv('DB_NAME', 'spacex_db'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', '')
        }
    
    def get_launches(self, page=1, per_page=5):
        """Fetch launches with pagination"""
        try:
            response = requests.get(f"{self.base_url}/launches")
            response.raise_for_status()
            all_launches = response.json()
            
            # Calculate pagination
            total = len(all_launches)
            total_pages = math.ceil(total / per_page)
            start = (page - 1) * per_page
            end = start + per_page
            
            launches = all_launches[start:end]
            
            return {
                'launches': launches,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': total_pages,
                'has_prev': page > 1,
                'has_next': page < total_pages
            }
        except requests.RequestException as e:
            print(f"Error fetching launches: {e}")
            return None
    
    def get_launch_by_id(self, launch_id):
        """Fetch specific launch details"""
        try:
            response = requests.get(f"{self.base_url}/launches/{launch_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching launch {launch_id}: {e}")
            return None
    
    def get_crew_by_ids(self, crew_ids):
        """Fetch crew members by their IDs"""
        crew_members = []
        try:
            for crew_id in crew_ids:
                response = requests.get(f"{self.base_url}/crew/{crew_id}")
                response.raise_for_status()
                crew_members.append(response.json())
        except requests.RequestException as e:
            print(f"Error fetching crew: {e}")
        
        return crew_members
    
    def get_starred_crew(self):
        """Get starred crew members from database"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM crew_stars ORDER BY starred_at DESC")
            starred_crew = cursor.fetchall()
            
            return starred_crew
            
        except Error as e:
            print(f"Error fetching starred crew: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def star_crew_member(self, crew_id, crew_name, nickname, image_url=None, wikipedia_url=None):
        """Add crew member to starred list"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor()
            
            insert_query = """
            INSERT INTO crew_stars (crew_id, crew_name, nickname, image_url, wikipedia_url)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                nickname = VALUES(nickname),
                image_url = VALUES(image_url),
                wikipedia_url = VALUES(wikipedia_url),
                starred_at = CURRENT_TIMESTAMP
            """
            
            cursor.execute(insert_query, (crew_id, crew_name, nickname, image_url, wikipedia_url))
            connection.commit()
            
            return True
            
        except Error as e:
            print(f"Error starring crew member: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    
    def get_rockets(self):
        """Get rockets from database"""
        try:
            connection = mysql.connector.connect(**self.db_config)
            cursor = connection.cursor(dictionary=True)
            
            cursor.execute("SELECT * FROM rockets ORDER BY name")
            rockets = cursor.fetchall()
            
            return rockets
            
        except Error as e:
            print(f"Error fetching rockets: {e}")
            return []
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

spacex_api = SpaceXAPI()

@app.route('/')
def index():
    """Home page with launches pagination"""
    page = request.args.get('page', 1, type=int)
    
    launches_data = spacex_api.get_launches(page=page)
    if not launches_data:
        flash('Error fetching launches data', 'error')
        launches_data = {'launches': [], 'total': 0, 'page': 1, 'total_pages': 0, 'has_prev': False, 'has_next': False}
    
    return render_template('index.html', **launches_data)

@app.route('/launch/<launch_id>')
def launch_detail(launch_id):
    """Launch detail page with crew members"""
    launch = spacex_api.get_launch_by_id(launch_id)
    if not launch:
        flash('Launch not found', 'error')
        return redirect(url_for('index'))
    
    crew_members = []
    print(launch)
    if launch.get('crew'):
        crew_ids = launch['crew']
        crew_members = spacex_api.get_crew_by_ids(crew_ids)
    
    return render_template('launch_detail.html', launch=launch, crew_members=crew_members)

@app.route('/star_crew', methods=['POST'])
def star_crew():
    """Star a crew member with nickname"""
    crew_id = request.form.get('crew_id')
    crew_name = request.form.get('crew_name')
    nickname = request.form.get('nickname')
    image_url = request.form.get('image_url')
    wikipedia_url = request.form.get('wikipedia_url')
    
    if not crew_id or not crew_name or not nickname:
        flash('Missing required fields', 'error')
        return redirect(request.referrer or url_for('index'))
    
    if spacex_api.star_crew_member(crew_id, crew_name, nickname, image_url, wikipedia_url):
        flash(f'Successfully starred {crew_name} with nickname "{nickname}"!', 'success')
    else:
        flash('Error starring crew member', 'error')
    
    return redirect(request.referrer or url_for('index'))

@app.route('/starred_crew')
def starred_crew():
    """View all starred crew members"""
    starred = spacex_api.get_starred_crew()
    return render_template('starred_crew.html', starred_crew=starred)

@app.route('/rockets')
def rockets():
    """View all rockets from database"""
    rockets_data = spacex_api.get_rockets()
    return render_template('rockets.html', rockets=rockets_data)

if __name__ == '__main__':
    port = int(os.getenv('FLASK_PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)