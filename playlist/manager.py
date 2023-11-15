import pickle
from song import Song
from playlist import PlayList
import time

class Manager:

    def __init__(self):
        self.playlists: list[PlayList] = {}
        self.current_playlist: PlayList = None
        self.history = []
        self.redo_stack = []
        self.undo_stack = []

    def autoplay(self):
        '''
        time.sleep and interrupt from: 
        https://ioflood.com/blog/python-wait/#:~:text=In%20this%20example%2C%20if%20an,the%20next%20line%20of%20code.
        '''
        print(f"Total autoplay time will be: {self.current_playlist.total_runtime()} minutes. Press ctrl + c to end early")
        self.current_playlist.cur = self.current_playlist.start
        while self.current_playlist.cur:
            try:
                delay = self.current_playlist.cur.run_time * 60
                self.current_playlist.play_current()
                time.sleep(delay)
                self.current_playlist.cur = self.current_playlist.cur.next
            except KeyboardInterrupt:
                print("Returning to main menu")
                self.current_playlist.cur = None
        
    def select_or_create_playlist(self):
        """
		Lets the user select an existing playlist or create a new one.

		Returns:
				_type_: _description_
		"""
        if self.playlists:
            print("Available Playlists:")
            for i, playlist_name in enumerate(self.playlists.keys()):
                print(f"{i + 1}. {playlist_name}")
            print(f"{len(self.playlists) + 1}. Create New Playlist")

            choice = int(input("Enter your choice: "))
            if 1 <= choice <= len(self.playlists):
                self.current_playlist = list(self.playlists.values())[choice -
                                                                      1]
                print(choice, "choice is one")
            elif choice == len(self.playlists) + 1:
                playlist_name = input("Enter name for the new playlist: ")
                self.create_playlist(playlist_name)
                self.current_playlist = self.playlists[playlist_name]
            else:
                print("Invalid choice!")
                return None
            choice = None
            print(choice, "choice changed to none")
        else:
            print("No playlists found.")
            playlist_name = input("Enter name for a new playlist: ")
            self.create_playlist(playlist_name)
            self.current_playlist = self.playlists[playlist_name]

    def create_playlist(self, name: str):
        """
		Creates a new playlist with the given name.

		Args:
				name (str): name of the playlist
		"""
        self.playlists[name] = PlayList(name)

    def add_song_to_playlist_by_name_or_id(self, names_or_ids: str,
                                           song_pool: list) -> None:
        """        
		Allows the user to add one or multiple songs to their selected/current playlist by providing 
		either the song's name or ID. Multiple songs can be separated by commas.
		- Searches the song pool to find the song.
		- Adds the song to the selected playlist at a specified index (or at the end if no index provided).

		Args:
				names_or_ids (str): names or IDs of the songs to add
				song_pool (list): list of songs available to add to your playlist
		"""

        for name_or_id in names_or_ids.split(','):
            name_or_id = name_or_id.strip(
            )  # Remove any leading/trailing whitespaces

            song_to_add = None

            # Check if the input is an ID (integer)
            if name_or_id.isdigit():
                song_id = int(name_or_id)
                for song in song_pool:
                    if song.idx == song_id:
                        song_to_add = song
                        break
            else:  # Search by name
                for song in song_pool:
                    if song.name.lower() == name_or_id.lower():
                        song_to_add = song
                        break

            if song_to_add:
                if not self.current_playlist:
                    print(
                        "\033[35mNo playlist is currently selected. Please select or create one.\033[0m"
                    )
                    return

                index_str = input(
                    f"Enter the index at which you want to add the song \033[1m'{song_to_add.name}'\033[0m (or leave empty to add to the end): "
                )

                try:
                    index = int(index_str) if index_str.isdigit() else None
                except ValueError:
                    print(
                        "\033[31mPlease enter a valid index number or leave it blank.\033[0m"
                    )
                    return

                self.current_playlist.add(song_to_add, index)
                self.undo_stack.append((song_to_add, index))
                print(
                    f"\033[32mSong '{song_to_add.name}' added to the playlist!\033[0m"
                )
            else:
                print(f"\033[31mSong '{name_or_id}' not found!\033[0m")

    def display_available_songs(self, song_pool: list, chunk_size: int = 10):
        """
		Display available songs from the song pool, chunk_size songs at a time.

		Args:
				song_pool (list): list of songs available to add to your playlist
				chunk_size (int, optional): number of songs to display at a time. Defaults to 10.
		"""
        song_count = len(song_pool)
        start_idx = 0

        while start_idx < song_count:
            for idx in range(start_idx, min(start_idx + chunk_size,
                                            song_count)):
                song = song_pool[idx]
                print(f"{idx + 1}. {song.name} by {song.artist}")

            start_idx += chunk_size

            # If there are more songs to display, ask the user if they want to see more.
            if start_idx < song_count:
                user_input = input("\nShow more songs? (y/n): ").lower()
                if user_input != 'y':
                    break

    def add_song_to_current_playlist(self, song: Song, index: int = None):
        """        
		Takes a song and directly adds it to the current_playlist
		If you have a direct reference to a song object in the main program or elsewhere,
		you can easily add it to the current playlist without any further input from the user.

		Args:
				song (Song): song to add to the current playlist
		"""
        if not self.current_playlist:
            print(
                "No playlist is currently selected. Please select or create one."
            )
            return

        self.current_playlist.add(song, index)
        self.undo_stack.append((song, index))
        print(f"\033[32mSong '{song.name}' added to the playlist!\033[0m")


    def share_playlist(self):
        if self.current_playlist:
            current = self.current_playlist.start
            name = f"{self.current_playlist.name}.txt"
            with open(name, 'w') as file:
                file.write("playlist name: " + self.current_playlist.name + "\n\n")
                while current is not None:
                    if current.next is None:
                        file.write(str(current))
                    else:
                        file.writelines(str(current) + "\n")
                    current = current.next
                print(f'Share successful, file generated: "{name}"')
        else:
            print("No playlist selected, create or select a playlist to share.")


    def undo(self):
        """
		Undoes the last action performed by the user.
		"""
        if self.undo_stack:
            song_popped = self.undo_stack.pop()
            if song_popped:
                print(song_popped)
                if song_popped[1] is None:
                    self.current_playlist.remove_at_end()
                else:
                    self.current_playlist.remove_by_index(song_popped[1])
                
                self.redo_stack.append(song_popped)
                print("Undone!")
        print("Nothing to undo")

    def redo(self):
        """
		Redoes the last action performed by the user.
		"""
        if self.redo_stack:
            song_popped = self.redo_stack.pop()
            if song_popped:
                self.add_song_to_current_playlist(song_popped[0], song_popped[1])
                self.undo_stack.append(song_popped)
                print("Redone!")
        print("Nothing to redo")

    def display_current_playlist_songs(self):
        """
		Displays all songs in the current playlist.
		"""
        if not self.current_playlist:
            print('No playlist is currently selected.')
            return

        print(f"Songs in the playlist: '{self.current_playlist.name}':")
        song = self.current_playlist.start
        idx = 1
        while song:
            if song == self.current_playlist.cur:
                print(f"{idx}. < {song.name} by {song.artist} >  🐢 ")
            else:
                print(f"{idx}. {song.name} by {song.artist}")
            song = song.next
            idx += 1

    def show_currently_playing(self):
        """
		Displays the currently playing song and the current playlist.
		"""
        if not self.current_playlist:
            print('No playlist is currently selected.')
        else:
            print(f"Playing from playlist: '{self.current_playlist.name}'")

            # Check if a song is currently playing
            if self.current_playlist.cur:
                print(
                    f"Currently playing song: '{self.current_playlist.cur.name}'"
                )
            else:
                print(
                    "\033[35mNo song is currently playing in the selected playlist.\033[0m"
                )

    @classmethod
    def save_to_file(self, filename: str):
        """
		Saves the current state of the program to a file.

		Args:
				filename (str): name of the file to save to in pickle format
		"""
        with open(filename, 'wb') as file:
            pickle.dump(self, file)

    @classmethod
    def load_from_file(cls, filename: str):
        """
		Loads the state of the program from a file.
		Args:
				filename (str): name of the file to load from in pickle format

		Returns:
				_type_: _description_
		"""
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def _ensure_playlist_selected(self):
        """Helper method

		Returns:
				_type_: _description_
		"""
        if not self.current_playlist:
            print(
                "\033[35mNo playlist is currently selected. Please select or create one.\033[0m"
            )
            return False
        return True

    def play_current_song(self):
        """
		Play the currently selected song.
		"""
        if not self._ensure_playlist_selected():
            return
        self.current_playlist.play_current()

    def play_next_song(self):
        """
		Play the next song in the playlist.
		"""
        if not self.current_playlist:
            print("Please select a playlist first!")
            return
        self.current_playlist.play_next()

    def play_previous_song(self):
        """
		Play the previous song in the playlist.
		"""
        if not self.current_playlist:
            print("Please select a playlist first!")
            return
        self.current_playlist.play_previous()

    def reset_current_playlist(self):
        """
		Reset the current playlist.
		"""
        self.current_playlist = None

    def save_state(self, filename: str):
        """Saves the current state, including the playlist, currently playing song and other meta info

		Args:
				filename (str): name of the file you want to save with
		"""
        with open(filename, 'wb') as file:
            pickle.dump(self, file)
        print("State saved successfully!")

    @classmethod
    def load_state(cls, filename: str):
        """Loads any saved state.
		If there is no saved state it will keep working on current session

		Args:
				filename (str): _description_

		Returns:
				_type_: _description_
		"""
        try:
            with open(filename, 'rb') as file:
                return pickle.load(file)
        except FileNotFoundError:
            return cls(
            )  # if there's no saved state, return a new Manager instance
