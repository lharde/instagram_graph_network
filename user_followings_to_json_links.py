import json

def generate_instagram_links():
    # Read the input JSON file
    with open('input_followers.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # Extract usernames and create Instagram profile URLs with IDs
    instagram_links = []
    for index, user in enumerate(data['users'], start=1):
        username = user['username']
        profile_url = f"https://www.instagram.com/{username}/"
        instagram_links.append({
            "id": index,
            "url": profile_url
        })
    
    # Write the links to a new JSON file
    output_data = {
        "instagram_profile_links": instagram_links
    }
    
    with open('instagram_profile_links.json', 'w', encoding='utf-8') as file:
        json.dump(output_data, file, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated {len(instagram_links)} Instagram profile links with IDs.")

if __name__ == "__main__":
    generate_instagram_links()
