# Web Scraping using Selenium
# Import the Important Libraries

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os
import zipfile
import requests
import pandas as pd
import json


# Set up headless browser
options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

# Open downloads page
driver.get("https://cricsheet.org/downloads/")
time.sleep(3)
html = driver.page_source
driver.quit()

# Parse with BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Match types we want
desired_keywords = {
    "Test matches": "tests_json.zip",
    "One-day internationals": "odis_json.zip",
    "T20 internationals": "t20s_json.zip",
    "Indian Premier League": "ipl_json.zip"
}

# Create download folder
download_folder = "cricsheet_data"
os.makedirs(download_folder, exist_ok=True)

# Extract all <a> tags that contain zip files
all_links = soup.find_all("a", href=True)

# Download matching files
for label, file_name in desired_keywords.items():
    found = False
    for tag in all_links:
        href = tag['href']
        if file_name in href:
            full_url = "https://cricsheet.org" + href if href.startswith("/downloads") else href
            save_path = os.path.join(download_folder, file_name)

            print(f"Downloading {label} → {file_name}")
            r = requests.get(full_url, stream=True)
            with open(save_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Saved: {file_name}")
            found = True
            break
    if not found:
        print(f" Could not find link for {label}")

print("\nAll done. Check the 'cricsheet_data' folder!")

# Creating Dataframe from JSON

# Import importanat Libraries
import os
import json
import pandas as pd

folder = r"C:\Users\pc\Desktop\Project_2 Cricsheet Analysis\cricsheet_data"
match_list = []

for match_type in ["ipl", "odi", "t20", "test"]:
    match_type_folder = os.path.join(folder, match_type)

    if not os.path.exists(match_type_folder):
        print(f"{match_type_folder} not found.")
        continue

    for file_name in os.listdir(match_type_folder):
        if file_name.endswith(".json"):
            file_path = os.path.join(match_type_folder, file_name)

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    venue = data.get("info", {}).get("venue", "")
                    teams = data.get("info", {}).get("teams", [])
                    date = data.get("info", {}).get("dates", [""])[0]

                    match_list.append({
                        "match_type": match_type,
                        "venue": venue,
                        "teams": teams,
                        "date": date
                    })

            except Exception as e:
                print(f"Error reading {file_name}: {e}")

# Creating DataFrame
df = pd.DataFrame(match_list)

print("Total Matches Read:", len(df))
print("Match type distribution:\n", df['match_type'].value_counts())
print(df.head(20))

# Save DataFrame into MySQL

# Import importanat Libraries

import os
import json
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
from urllib.parse import quote_plus

# Connect to MySQL
username = "root"
password = "Rajan@6319"
host = "localhost"
database = "cricsheet_analysis"

# Encode password for URL-safe string
password_encoded = quote_plus(password)

# Path to Unzipped Match Folders 

root_folder = r"C:\Users\pc\Desktop\Project_2 Cricsheet Analysis\cricsheet_data"

# Create Database if not exists
conn = mysql.connector.connect(host=host, user=username, password=password)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
cursor.close()
conn.close()

# Create SQLAlchemy Engine
engine = create_engine(f"mysql+mysqlconnector://{username}:{password_encoded}@{host}/{database}")

# Loop through Each Match Format Folder
for match_format in ["t20", "odi", "ipl", "test"]:
    folder_path = os.path.join(root_folder, match_format)

    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue

    match_data = []

    for file in os.listdir(folder_path):
        if file.endswith(".json"):
            full_path = os.path.join(folder_path, file)
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    match_info = data.get("info", {})

                    match_entry = {
                        "match_format": match_format,
                        "date": match_info.get("dates", [""])[0],
                        "venue": match_info.get("venue", ""),
                        "teams": json.dumps(match_info.get("teams", [])), 
                        "city": match_info.get("city", ""),
                        "gender": match_info.get("gender", ""),
                        "match_type": match_info.get("match_type", ""),
                        "winner": match_info.get("outcome", {}).get("winner", "No Result")
                    }

                    match_data.append(match_entry)

            except Exception as e:
                print(f"Error in {file}: {e}")

    # Save DataFrame to SQL
    if match_data:
        df = pd.DataFrame(match_data)
        table_name = f"{match_format}_matches"
        df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)
        print(f"{match_format.upper()}: {len(df)} matches saved to `{table_name}`")
    else:
        print(f"{match_format.upper()}: No valid JSON files found")

print("\nAll match data saved successfully to MySQL!")