import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
#import os
from pathlib import Path
from tabulate import tabulate
import pyperclip
import sys

class SpotifySearchCLI:
    def __init__(self):
        self.sp = None
        self.setup_paths()
        self.load_config()
        self.current_page = 1
        self.total_pages = 1
        self.current_results = []
        
    def setup_paths(self):
        """Set up directory paths"""
        self.config_dir = Path('API_KEYS')
        self.config_file = self.config_dir / 'spotify.json'
        self.config_dir.mkdir(exist_ok=True)
        
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                
            required_fields = ['client_id', 'client_secret']
            if not all(field in config for field in required_fields):
                raise ValueError("Configuration file must contain: client_id, client_secret")
                
            self.config = config
            
        except FileNotFoundError:
            print("Configuration file not found. Creating template...")
            self.create_config_template()
            sys.exit(1)
            
        except json.JSONDecodeError:
            print("Invalid JSON format in configuration file.")
            sys.exit(1)
            
        except ValueError as e:
            print(f"Configuration error: {str(e)}")
            sys.exit(1)

    def create_config_template(self):
        """Create a template configuration file"""
        print("\nNeed to put creds in API_KEYS/spotify.json")
        print("- client_id\n- client_secret\n- redirect_uri")
        sys.exit(1)
            
        with open(self.config_file, 'w') as f:
            json.dump(template, f, indent=4)
            
    def setup_spotify(self):
        """Set up Spotify API credentials"""
        try:
            client_credentials_manager = SpotifyClientCredentials(
                client_id=self.config['client_id'],
                client_secret=self.config['client_secret']
            )
            self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        except Exception as e:
            print(f"Error setting up Spotify: {str(e)}")
            sys.exit(1)

    def search_song(self, query):
        """Search Spotify for songs with pagination"""
        try:
            results = self.sp.search(q=query, type='track', limit=10)
            self.total_pages = -(-results['tracks']['total'] // 10)  # Ceiling division
            self.current_page = 1
            self.current_results = results['tracks']['items']
            return self.current_results
        except Exception as e:
            print(f"Error searching Spotify: {str(e)}")
            return []

    def display_results(self, tracks):
        """Display search results in a table with pagination info"""
        if not tracks:
            print("No songs found.")
            return []
            
        table_data = [[i+1, track['name'], ', '.join(artist['name'] for artist in track['artists']), 
                      track['album']['name']] for i, track in enumerate(tracks)]
        headers = ['#', 'Song', 'Artists', 'Album']
        print(f"\nPage {self.current_page}/{self.total_pages}")
        print("Search Results:")
        print(tabulate(table_data, headers=headers, tablefmt='grid'))
        return tracks

    def get_next_page(self):
        """Get the next page of results"""
        if self.current_page >= self.total_pages:
            return None
            
        try:
            results = self.sp.search(q=self.last_query, type='track', 
                                   limit=10, offset=self.current_page * 10)
            self.current_page += 1
            self.current_results = results['tracks']['items']
            return self.current_results
        except Exception as e:
            print(f"Error getting next page: {str(e)}")
            return None

    def get_track_url(self, track):
        """Get the Spotify URL for a track"""
        return f"https://open.spotify.com/track/{track['id']}"

    def run(self):
        """Main CLI loop with pagination support"""
        print("Welcome to Spotify Search CLI!")
        
        while True:
            query = input("\nEnter song name to search (or 'q' to quit): ")
            if query.lower() == 'q':
                break
                
            self.last_query = query  # Store for pagination
            tracks = self.search_song(query)
            tracks = self.display_results(tracks)
            
            if not tracks:
                continue
                
            while True:
                try:
                    choice = input("\nEnter the number of the song to copy its link, "
                                 "'n' for next page, 'p' for previous page, or 0 to search again: ")
                    
                    if choice == '0':
                        break
                    elif choice == 'n':
                        next_tracks = self.get_next_page()
                        if next_tracks:
                            tracks = self.display_results(next_tracks)
                        else:
                            print("\nNo more pages available.")
                    elif choice == 'p':
                        if self.current_page > 1:
                            self.current_page -= 1
                            tracks = self.search_song(self.last_query)
                            tracks = self.display_results(tracks)
                        else:
                            print("\nAlready on first page.")
                    elif choice.isdigit() and 1 <= int(choice) <= len(tracks):
                        url = self.get_track_url(tracks[int(choice)-1])
                        pyperclip.copy(url)
                        print(f"\nCopied to clipboard: {url}")
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")

if __name__ == "__main__":
    cli = SpotifySearchCLI()
    cli.setup_spotify()
    cli.run()
