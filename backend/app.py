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



    
    cv_data = {
        'name': 'Ali Alqeisi',
        'linkedin': 'https://www.linkedin.com/in/aq02/',
        'experiences': [
            {
                'title': 'R&D Software Development Intern',
                'company': 'Brainlab’s Langer Medical',
                'duration': 'September 2024 - Februar 2025, Waldkirch, Deutschland',
                'details': [
                    'Reduzierung der Produktionszeit pro Gerät um 15 Minuten durch die Entwicklung eines automatisierten Windows-Installationssystems und eines Python-Programms, was einer Kosteneinsparung von etwa 7 USD pro Gerät entspricht.',
                    'Dokumentation gemäß IEC 62304-Medizinprodukte-Software-Lebenszyklusprozess, von der Stakeholder-Ebene bis zu den Testfällen.',
                    'Entwicklung einer unterstützenden Softwarelösung, die die Inbetriebnahme und kundenspezifische Konfiguration der Geräte durch das Produktionsteam erleichtert.',
                    'Beitrag zur Software- und Systemverifikationstests von Neuromonitoring-Geräten.'
                ]
            }
        ],
        'skills': [
            'Python', 'Powershell', 'Bash', 'Linux', 'Matlab', 'MDT', 'Docker', 'Kubernetes', 'Jenkins (CI/CD)', 'Terraform', 'Ansible', 'Azure', 'TensorFlow', 'Agile Methodik', 'Windows Server', 'Konfigurationsmanagement',
            'Arabisch (Muttersprache)', 'Englisch (Fließend)', 'Deutsch (C1)'
        ],
        'projects': [
            {
                'title': 'Containerisierte Flask-App mit CI/CD (Laufend)',
                'details': [
                    'Entwicklung einer Flask-Webanwendung, die mit Docker containerisiert wurde.',
                    'Erstellung einer CI/CD-Pipeline mit Jenkins für automatisierte Deployments.',
                    'Bereitstellung der Anwendung in einem Kubernetes-Cluster mithilfe von Deployments und NodePort-Service.'
                ]
            },
            {
                'title': 'Terraform-basierte AKS-Cluster-Deployment',
                'details': [
                    'Bereitstellung von AKS-Clustern in Azure mithilfe von Terraform.',
                    'Integration von Azure Key Vault für die sichere Verwaltung von secrets.',
                    'Automatisierung der AKS-Bereitstellung mit Terraform und Service Principals.'
                ]
            },
            {
                'title': 'Deep Learning zur Klassifizierung von Herztönen',
                'details': [
                    'Anwendung von Signalverarbeitung (Fourier-Transformation, Wavelets, Cepstrum) zur Extraktion von Merkmalen aus Herztonaufnahmen.',
                    'Erstellung eines TensorFlow-basierten CNN-Modells zur Klassifizierung von 5 Arten von Herzkrankheiten mit 97% Genauigkeit.'
                ]
            }
        ],
        'Studium': [
            {
                'degree': 'Medizintechnik',
                'institution': 'Hochschule Rheinmain, Wiesbaden, Deutschland',
                'duration': 'März 2024 - März 2025',
                'details': '2 Auslandssemester als Erasmus-Stipendiat'
            },
            {
                'degree': 'Biomedizinische Technik (Schwerpunkt Elektrotechnik)',
                'institution': 'German Jordanian University, Madaba, Jordanien',
                'duration': 'September 2020 - März 2025',
                'details': 'Rang 5 im Studiengang Biomedizinische Technik'
            }
        ],
        'total_views': total_views
    }
   
    return render_template('index.html', **cv_data)

if __name__ == '__main__':
    
    start_http_server(8000)
    subprocess.Popen(["python", "consumer.py"])
    app.run(host='0.0.0.0', port=5000, debug=False)

