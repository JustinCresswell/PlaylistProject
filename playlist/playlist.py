from song import Song
import webbrowser

class PlayList:
    def __init__(self, name : str = 'Default') -> None:
        self.start : Song = None  # start of the song list [head of the doubly-linked list]
        self.end : Song = None    # end of the song list [tail of the doubly-linked list]
        self.cur : Song = None    # cur song of the playlist
        self.name = name
        self.length = 0
        self.redo_stack = []
        self.undo_stack = []

    def _get_song_at_index(self, index) -> Song:
        """
        Helper method to retrieve the song at a specific index.

        Args:
            index (int): index of the song to retrieve

        Returns:
            Song: song at the specified index
        """
        # start from the beginning and keep going forward, finally return the desired song
        current = self.start
        count = 0
        while current is not None and count < index:
            print('test error in helper')
            current = current.next
            count += 1
        return current


    def remove_by_name(self, name: str) -> None:
        """
        Remove the first occurrence of a song by its name.
        - Traverse the list to find the song.
        - Adjust the prev and next attributes of the surrounding songs accordingly.

        Args:
            name (str): name of the song to remove
        """
        if self.start is not None:
            current = self.start
            while current is not None:
                if current.name == name:
                    if current is self.start and current is self.end:
                        current.prev = None
                        current.next = None
                        self.clear()
                        return
                    elif current.next is None:
                        print(current, current.next, current.prev)
                        self.end = current.prev 
                        self.end.next = None
                        self.length -= 1
                        current.prev = None
                        current.next = None
                        return
                    else:
                        current.next.prev = current.prev
                        current.prev.next = current.next
                        current.prev = None
                        current.next = None
                        self.length -= 1
                        return
                current = current.next
            self.length -= 1
            return "Song not found"


    def remove_by_index(self, index: int, name:str = None) -> None:
        """        
        Remove the song at the specified index.
        - Traverse the list to find the song at the given index.
        - Adjust the prev and next attributes of the surrounding songs accordingly.

        Args:
            index (int): index of the song to remove
        """
        my_idx = index
        if my_idx < 0:
            my_idx += self.length
        if my_idx < self.length:
            song = self._get_song_at_index(index=my_idx)
            if song is None:
                try:
                    self.remove_by_name(name)
                except:
                    raise IndexError(f"Index out of bounds index {index} and length {self.length}")
                return                
            elif song is self.start:
                if song.next is not None:
                    self.start = self.start.next
                    self.start.prev = None
                else:
                    self.clear()
                    return
            elif song is self.end:
                song.prev.next = song.next
                song.prev = None
            else:
                song.prev.next= song.next
                song.next.prev = song.prev
            
            song.prev = None
            song.next = None
        else:
            try:
                self.remove_by_name(name)
            except:
                raise IndexError(f"Index out of bounds index {index} and length {self.length}")
            return
        self.length -= 1
        print(self.length)

    def add(self, song: Song, index=None) -> None:
        """
        Add a song to the playlist.
        If an index is specified, the song is inserted at that position.
        Otherwise, it's appended to the end.
        Args:
            song (Song): song to add
            index (int, optional): index where the song is being added. Defaults to None.
        """
        # check if the list is empty
        
        # if not empty
            # append or insert on the specific index
            #self._get_song_at_index(index) will help retrive the song
        if not song:
            print("\033[31mNo song provided. Cannot add to the playlist.\033[0m")
            return
        else:
            if self.start is None:
                self.start = song
                self.end = self.start
            elif index is None or index >= self.length:
                self.end.next = song
                song.prev = self.end
                self.end = song
            else:
                current = self._get_song_at_index(index=index)
                if current is None:
                    song.prev = self.end
                    self.end.next = song
                    self.end = song
                elif current is self.start:
                    song.next = current
                    current.prev = song
                    self.start = song
                else:
                    current.prev.next = song
                    song.prev = current.prev
                    song.next = current
                    current.prev = song

            self.length += 1
            self.cur = self.start
            print(self.length)


    def clear(self) -> None:
        """
        Clear the entire playlist.
        """
        self.start = None
        self.end = None
        self.cur = None
        self.length = 0

    # def sort(self, key: str) -> None:
    #     """   
    #     Do this if time allows. This is not mendatory     
    #     Sort the playlist based on the given key (e.g., 'name', 'views', 'run_time').
    #     - Implement a sorting algorithm suitable for doubly linked lists (e.g., insertion sort).
    #     Args:
    #         key (str): key to sort by
            
    #     # Q: Which sorting algorithms have we learned that could be applied to a doubly-linked list? Which would be the most efficient? Are you  using the builtin sort by key method?
    #     """
    #     pass

    def reverse(self) -> None:
        """
        Reverse the order of songs in the playlist.
        """
        new_start = self.end
        current = self.end
        while current.prev is not self.start:
            current.next = current.prev
            current.next.prev = current
            current = current.next
        self.start.prev = current
        current.next = self.start
        self.end = self.start
        self.start = new_start

    def total_count(self) -> int:
        """
        Return the total number of songs in the playlist.

        Returns:
            int: total number of songs in the playlist
        """
        return self.length
    
    def total_view(self) -> int:
        """
        Return the total number of views of all songs in the playlist.

        Returns:
            int: total number of views of all songs in the playlist
        """
        views = 0
        current = self.start
        while current is not None:
            views += current.views
            current = current.next
        return views
    
    def total_runtime(self) -> int:
        """Return the total runtime of all songs in the playlist.

        Returns:
            int: total runtime of all songs in the playlist
        """
        runtime = 0
        current = self.start
        while current is not None:
            runtime += current.run_time
            current = current.next
        return runtime
    
    def display(self, chunk_size=10) -> None:
        """
        Display songs in the playlist, chunk_size songs at a time.

        Args:
            chunk_size (int, optional): number of songs to display at a time. Defaults to 10.
        """
        # Check if playlist is empty, if it is empty return right away
        if not self.start:
            print("\033[35mThe playlist is empty!\033[0m")
            return

        current = self.start
        count = 0

        # incase you want to show a chunk of song at a time and progress. 
        while current and (count < chunk_size):
            print(current)
            print('test error')
            current = current.next
            count += 1

        # your logic to show that chunk
        pass
                
    def play_current(self):
        """
        Play the currently selected song.
        """
        if self.cur:
            webbrowser.open(f'https://www.youtube.com/watch?v={self.cur.youtube_id}')
            print(f'https://www.youtube.com/watch?v={self.cur.youtube_id}')
            print(f"Playing {self.cur.name} by {self.cur.artist}...")
        else:
            print("\033[35mNo song is currently selected!\033[0m")

    def play_next(self):
        """
        Goto or point to the next song in the playlist.
        """
        # go select the next song. No need to play here
        if self.cur is not None and self.cur.next is not None:
            self.cur = self.cur.next
            self.play_current()

    def play_previous(self):
        """
        Goto or point to the previous song in the playlist.        
        """
        # same as next
        if self.cur is not None and self.cur.prev is not None:
            self.cur = self.cur.prev
            self.play_current()
