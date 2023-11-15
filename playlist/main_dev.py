from util import FileUtil
from song import Song
from playlist import PlayList
from manager import Manager
import os

def main():
    # Load all songs from a CSV into a song pool
    dir_path = os.path.dirname(os.path.realpath(__file__))
    csv_path = os.path.join(dir_path, "song_list.csv")
    song_pool = FileUtil.load_songs_from_csv(csv_path)

    # Try to load the previous state if it exists
    manager = Manager.load_state("manager_state.pkl")
    
    while True:
        if not manager.current_playlist:
            print("\n--- 🪩 Playlist Manager 🪩 ---")
            print("1. Create a new playlist 🟢")
            print("2. Select an existing playlist 🔢")
            print("3. Save state 📥")  
            print("0. Exit 🛑")          
        else:
            print(f"\n--- 🎧 {manager.current_playlist.name} 🎧 ---")
            print("1. Play current song ▶")
            print("2. Play next song ⏭️")
            print("3. Play previous song ⏮️")
            print("4. Add song to playlist by name or ID 🎵")
            print("5. Display songs in the playlist 🎞️")
            print("6. Go back to main menu ⬅️")
            print("7. Display available songs 🗒️")
            print("8. Save state 📥")
            print("9. Share Playlist >>>")
            print('10. Type "redo" or "undo" to revert any changes')
            print('11. Type "auto" to autoplay current playlist')
            print("0. Exit 🛑")
            
            # total amount of time for the playlist by ⌛
            # total number of song in the playlist by 🔢
            # Check the Playlist to explore other functionalities to add ***
        try:
            choice = input("\nPlease enter your choice: ")
        except ValueError:
            print("\033[31mPlease enter a valid choice number!\033[0m")
            continue
        
        if not manager.current_playlist:
            if choice == '1':
                playlist_name = input("Enter name for the new playlist: ")
                manager.create_playlist(playlist_name)
            elif choice == '2':
                manager.select_or_create_playlist()
            elif choice == '3':
                manager.save_state("manager_state.pkl")    
        if choice == '0':
            confirm_exit = input("Are you sure you want to exit? (y/n): ").lower()
            if confirm_exit == 'y':
                break
        else:
            if choice == '1':
                manager.play_current_song()
            elif choice == '2':
                manager.play_next_song()
            elif choice == '3':
                manager.play_previous_song()
            elif choice == '4':
                song_name_or_id = input("Enter the song name or ID:")
                manager.add_song_to_playlist_by_name_or_id(song_name_or_id, song_pool)
            elif choice == '5':
                manager.display_current_playlist_songs()
            elif choice == '6':
                manager.current_playlist = None
            elif choice == '7':
                manager.display_available_songs(song_pool)
            elif choice == '8':
                manager.save_state("manager_state.pkl")
            elif choice == '9':
                manager.share_playlist()
            elif choice.lower() == "redo":
                manager.redo()
            elif choice.lower() == "undo":
                manager.undo()
            elif choice.lower() == "auto":
                manager.autoplay()
        if choice == '0':
            confirm_exit = input("Are you sure you want to exit? (y/n): ").lower()
            if confirm_exit == 'y':
                break
        print("\n" + "-"*40)

if __name__ == "__main__":
    main()
