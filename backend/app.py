from flask import Flask, render_template, request
from producer import log_cv_view
import os
from kafka import KafkaProducer
from prometheus_client import start_http_server, Counter
import sqlite3
from consumer import start_consumer
import subprocess



app = Flask(__name__)

app.config['TEMPLATES_AUTO_RELOAD'] = True

cv_views_counter = Counter('cv_views_total', 'Total number of CV views')

def initialize_database():
    conn = sqlite3.connect('/WORKDIR/data/cv_views.db')
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cv_views (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_views INTEGER DEFAULT 0
        )
    ''')
    
    # Insert initial data if the table is empty
    cursor.execute('INSERT OR IGNORE INTO cv_views (id, total_views) VALUES (1, 0)')
    conn.commit()
    conn.close()

# Initialize the Prometheus Counter with the current total_views from the database
def initialize_counter():
    conn = sqlite3.connect('/WORKDIR/data/cv_views.db')
    cursor = conn.cursor()
    cursor.execute('SELECT total_views FROM cv_views WHERE id = 1')
    total_views = cursor.fetchone()[0]
    conn.close()
    
    # Set the initial value of the Prometheus Counter
    cv_views_counter.inc(total_views)
    
    return total_views

# Increment the total_views in the database and the Prometheus Counter
def increment_counter():
    conn = sqlite3.connect('/WORKDIR/data/cv_views.db')
    cursor = conn.cursor()
    
    # Increment the total_views by 1
    cursor.execute('UPDATE cv_views SET total_views = total_views + 1 WHERE id = 1')
    conn.commit()
    conn.close()
    
    # Increment the Prometheus Counter
    cv_views_counter.inc()

# Initialize the database and counter when the app starts
initialize_database()
total_views = initialize_counter()



@app.route('/')
def home():

     # Capture user agent from the request headers
    user_agent = request.headers.get('User-Agent',"Unknown")

    increment_counter()
    
    # Call the Kafka producer function to log the view
    log_cv_view(user_agent)

    conn = sqlite3.connect('/WORKDIR/data/cv_views.db')
    cursor = conn.cursor()
    cursor.execute('SELECT total_views FROM cv_views WHERE id = 1')
    current_total_views = cursor.fetchone()[0]
    conn.close()



    cv_data = {
    'name': 'Ali Alqeisi',
    'profession': 'Devops Engineer',
    'linkedin': 'https://www.linkedin.com/in/aq02/',
    'email': 'ali@alqima.eu',  # Add your email here
    'github': 'https://github.com/AliAlqeisi2',  # Add your GitHub link here
    'experiences': [
        {
            'title': 'R&D Software Development Intern',
            'company': 'Brainlab’s Langer Medical',
            'duration': 'September 2024 - February 2025, Waldkirch, Germany',
            'details': [
                'Reduced production time per device by 15 minutes by developing an automated Windows installation system and a Python program, resulting in a cost saving of approximately 70USD per device.',
                'Documented according to the IEC 62304 medical device software lifecycle process, from stakeholder level to test cases.',
                'Developed a supporting software solution to facilitate the commissioning and customer-specific configuration of devices by the production team.',
                'Contributed to software and system verification tests for neuromonitoring devices.',
                'Testimonials: "Mr. Alqeisi stood out through his excellent willingness to learn. His very dependable work ethic could be relied on at all times and even in difficult situations. His conduct towards his line managers, mentors, colleagues or towards clients was always impeccable" - Reinhold Zimmermann, R&D Director at Langer Medical, Brainlab '
            ]
        }
    ],
    'skills': [
      'Agile','Ansible','Azure','Bash','Config Mgmt.','Docker','Jenkins (CI/CD)','Kubernetes','Linux','Matlab','MDT','Powershell','Python','Terraform (IaC)','TensorFlow','Windows Server','Arabic (Native)','English (Fluent)','German (C1)'
    ],
    'projects': [
        {
            'title': 'Smart CV with DevOps-Driven Deployment and Real-Time View Tracking (This Website)',
            'details': [
                'Developed a Flask-based web application to showcase my CV with real-time view tracking.',
                'Implemented Apache Kafka for user agent tracking and email notifications when the CV is viewed.',
                'Used SQLite as the database to store view data and user information.',
                'Containerized the application using Docker and deployed it on Azure App Service.',
                'Set up a CI/CD pipeline with Jenkins to automatically deploy updates.',
                'Managed infrastructure-as-code using Terraform for automated provisioning and scaling.',
                'Hosted the application on Azure App Service for reliable and scalable deployment.',
                'Integrated Prometheus and cAdvisor for monitoring container metrics and performance.'
            ]
        },
        {
            'title': 'Terraform-based AKS Cluster Deployment',
            'details': [
                'Deployed AKS clusters in Azure using Terraform.',
                'Integrated Azure Key Vault for secure secret management.',
                'Automated AKS deployment using Terraform and Service Principals.'
            ]
        },
        {
            'title': 'Deep Learning for Heart Sound Classification',
            'details': [
                'Applied signal processing (Fourier Transform, Wavelets, Cepstrum) to extract features from heart sound recordings.',
                'Developed a TensorFlow-based CNN model to classify 5 types of heart diseases with 97% accuracy.'
            ]
        }
    ],
    'certificates': [
        {'name': 'Jenkins: CI/CD Pipeline for Scalable Web Applications', 'link': 'https://learn.kodekloud.com/certificate/8cb35cd8-a46a-44e9-97ac-9b177bffa29e'},
        {'name': 'Apache Kafka - Foundations and Development', 'link': 'https://learn.kodekloud.com/certificate/00735ead-6268-4d6f-aa23-f997ac59c3e5'},
        {'name': 'Learn Ansible Basics - Beginners Course', 'link': 'https://learn.kodekloud.com/certificate/6da6ef57-5606-4fca-9ba7-a7d2f7624020'},
        {'name': 'Prometheus Certified Associate (PCA)', 'link': 'https://learn.kodekloud.com/certificate/1d77669b-8285-4d39-8387-a8de60814d34'},
        {'name': 'AZ900: Microsoft Azure Fundamentals', 'link': 'https://learn.kodekloud.com/certificate/6e7c3c01-3243-4711-a064-51eee01a1056'},
        {'name': 'Terraform Basics Training Course', 'link': 'https://learn.kodekloud.com/certificate/d47ed776-574c-460a-96f6-4cd462f84fd6'},
        {'name': 'Kubernetes - Hands-on Tutorial', 'link': 'https://learn.kodekloud.com/certificate/a7840298-1239-416b-9b54-fcf71453ac7d'},
        {'name': 'Docker Training Course', 'link': 'https://learn.kodekloud.com/certificate/9a8c9f34-cf7b-4b7c-8f75-4a2f0306f8e1'},
        
        
        
        
        
       
    ],
    'education': [
        {
            'degree': 'Medical Engineering',
            'institution': 'Hochschule RheinMain, Wiesbaden, Germany',
            'duration': 'March 2024 - March 2025',
            'details': '2 semesters as an Erasmus scholarship holder'
        },
        {
            'degree': 'Biomedical Engineering (Focus on Electrical Engineering)',
            'institution': 'German Jordanian University, Madaba, Jordan',
            'duration': 'September 2020 - March 2025',
            'details': 'Ranked 5th in the Biomedical Engineering program'
        }
    ],
    'total_views': current_total_views
    }
   
    return render_template('index.html', **cv_data)

if __name__ == '__main__':
    
    start_http_server(8000)
    subprocess.Popen(["python", "consumer.py"])
    app.run(host='0.0.0.0', port=5000, debug=False)

