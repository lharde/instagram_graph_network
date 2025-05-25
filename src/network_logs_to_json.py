"""
Module for converting Instagram network logs to JSON files.
"""
import os
import re
import json
import logging
from pathlib import Path

# Setup logging
logger = logging.getLogger(__name__)

# Constants
INPUT_FOLDER = "network_logs"
OUTPUT_FOLDER = "json_followings"
FOLLOWERS_FILE = "input_followers.json"

def setup_directories():
    """Create necessary directories if they don't exist."""
    Path(OUTPUT_FOLDER).mkdir(exist_ok=True)
    Path(INPUT_FOLDER).mkdir(exist_ok=True)

def extract_username_from_pages(har_data):
    """Extract username from the title field in the pages section."""
    try:
        # Search in pages section for title
        for page in har_data.get("log", {}).get("pages", []):
            if "title" in page:
                title = page["title"]
                # Extract username from URL
                match = re.search(r'instagram\.com/([^/]+)/?', title)
                if match:
                    username = match.group(1)
                    logger.info(f"Found username: {username}")
                    return username
        logger.warning("No username found in pages")
        return None
    except Exception as e:
        logger.error(f"Error extracting username: {e}")
        return None

def find_user_by_username(username, json_file=FOLLOWERS_FILE):
    """Find a user by their username in a JSON file."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        logger.debug(f"Searching for user: {username}")
        
        # Try exact match
        for user in data['users']:
            if user['username'].lower() == username.lower():
                logger.info(f"Found user: {user['username']} (ID: {user['id']})")
                return user
        
        logger.warning(f"User not found: {username}")
        return None
    except Exception as e:
        logger.error(f"Error reading file: {e}")
        return None

def extract_followings(response_data):
    """Extract following data from various JSON structures."""
    followings = []
    
    if isinstance(response_data, dict):
        # Direct user data
        if "user" in response_data:
            user = response_data["user"]
            if all(k in user for k in ["full_name", "username", "id"]):
                followings.append({
                    "full_name": user["full_name"],
                    "username": user["username"],
                    "id": user["id"]
                })
        
        # Data in users array
        if "users" in response_data:
            for user in response_data["users"]:
                if all(k in user for k in ["full_name", "username", "id"]):
                    followings.append({
                        "full_name": user["full_name"],
                        "username": user["username"],
                        "id": user["id"]
                    })
        
        # Data in data.users
        if "data" in response_data and "users" in response_data["data"]:
            for user in response_data["data"]["users"]:
                if all(k in user for k in ["full_name", "username", "id"]):
                    followings.append({
                        "full_name": user["full_name"],
                        "username": user["username"],
                        "id": user["id"]
                    })
    
    return followings

def process_har_file(filepath):
    """Process a single HAR file and extract user data."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            har_data = json.load(f)
        
        # Extract username from pages section
        username = extract_username_from_pages(har_data)
        if not username:
            logger.error(f"❌ No username found in {filepath}")
            return None, None, []
            
        # Find user in input_followers.json
        user = find_user_by_username(username)
        if not user:
            logger.error(f"❌ User {username} not found in {FOLLOWERS_FILE}")
            return None, None, []
            
        followings = []
        
        # Search all entries in HAR file
        for entry in har_data.get("log", {}).get("entries", []):
            try:
                # Extract response content
                content = entry.get("response", {}).get("content", {}).get("text", "")
                if not content:
                    continue
                
                # Try to parse content as JSON
                try:
                    response_data = json.loads(content)
                except json.JSONDecodeError:
                    continue
                
                # Extract following data
                followings.extend(extract_followings(response_data))
            
            except Exception as e:
                logger.error(f"Error processing entry: {str(e)}")
                continue
        
        return username, user["id"], followings
        
    except Exception as e:
        logger.error(f"❌ Error processing {filepath}: {str(e)}")
        return None, None, []

def main():
    """Main function to process all HAR files."""
    setup_directories()
    
    # Check if there are any HAR files to process
    har_files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith('.har')]
    if not har_files:
        logger.warning(f"No HAR files found in {INPUT_FOLDER}")
        return
    
    for filename in har_files:
        filepath = os.path.join(INPUT_FOLDER, filename)
        logger.info(f"Processing {filename}...")
        
        # Process HAR file
        username, user_id, followings = process_har_file(filepath)
        
        if not username or not user_id or not followings:
            logger.error(f"❌ Could not fully extract data from {filename}")
            continue
        
        # Remove duplicates based on ID
        unique_followings = {user["id"]: user for user in followings}.values()
        
        # Create JSON structure
        data = {
            "username": username,
            "id": user_id,
            "followings": list(unique_followings)
        }
        
        # Save as JSON
        output_filename = f"{username}.json"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Created {output_filename} ({len(unique_followings)} followings found)")

if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('output/network_processing.log')
        ]
    )
    main()

    