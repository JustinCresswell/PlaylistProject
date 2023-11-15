'''
most code here is modified from given code or modified from zybooks code
any code I found online has a special note below it
'''
from song import Song
import webbrowser


class PlayList:
    def __init__(self, name: str = 'Default') -> None:
        # start of the song list [head of the doubly-linked list]
        self.start: Song = None
        # end of the song list [tail of the doubly-linked list]
        self.end: Song = None
        self.cur: Song = None    # cur song of the playlist
        self.current_iter = None
        self.name = name
        self.length = 0

    def add(self, song: Song, index=None) -> None:
        """
        Add a song to the playlist.
        If an index is specified, the song is inserted at that position.
        Otherwise, it's appended to the end.
        Args:
            song (Song): song to add
            index (int, optional): index where the song is being added. Defaults to None.
        """
        if not song:
            print("\033[31mNo song provided. Cannot add to the playlist.\033[0m")
            return

        # check if the list is empty
        if self.is_empty():
            self.start = song
            self.end = song
            self.length += 1
            return
        # if not empty
        if index is None:
            current = self.start
            while current:
                if current.next is None:
                    current.next = song
                    song.prev = current
                    self.end = song
                    self.length += 1
                    return
                current = current.next

        # append or insert on the specific index
        current = self._get_song_at_index(index)
        print(current)
        if current:
            temp = current.prev
            current.prev = song
            song.next = current
            song.prev = temp
            temp.next = song
            self.length += 1
            return
        print('invalid index')

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
        while current and count < index:
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
        current = self.start
        while current:
            if current.name == name:
                if current == self.start:
                    self.start = current.next
                if current == self.end:
                    self.end = current.prev
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                self.length -= 1
                return
            current = current.next
        print('No item with name in playlist')

    def remove_by_index(self, index: int) -> None:
        """        
        Remove the song at the specified index.
        - Traverse the list to find the song at the given index.
        - Adjust the prev and next attributes of the surrounding songs accordingly.

        Args:
            index (int): index of the song to remove
        """
        current = self._get_song_at_index(index)
        if current:
            if current == self.start:
                self.start = current.next
            if current == self.end:
                self.end = current.prev
            if current.prev:
                current.prev.next = current.next
            if current.next:
                current.next.prev = current.prev
            self.length -= 1
            current = current.next
            return
        print('No item with name in playlist')

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
        current = self.start
        while current:
            temp = current.next
            current.next = current.prev
            current.prev = temp
            current = temp
        self.start, self.end = self.end, self.start
        #tuple swap from https://www.30secondsofcode.org/python/s/swap-variables/

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
        current = self.start
        count = 0.0
        while current:
            count += current.views
            current = current.next
        return count

    def total_runtime(self) -> int:
        """Return the total runtime of all songs in the playlist.

        Returns:
            int: total runtime of all songs in the playlist
        """
        current = self.start
        count = 0.0
        while current:
            count += current.run_time
            current = current.next
        return count

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
        while current and count < chunk_size:
            print(current)
            current = current.next
            count += 1

    def play_current(self):
        """
        Play the currently selected song.
        """
        if self.cur is None:
            self.cur = self.start
            
        if self.cur:
            webbrowser.open(
                f'https://www.youtube.com/watch?v={self.cur.youtube_id}')
            print(f'https://www.youtube.com/watch?v={self.cur.youtube_id}')
            print(f"Playing {self.cur.name} by {self.cur.artist}...")
        else:
            print("\033[35mNo song is currently selected!\033[0m")

    def play_next(self):
        """
        Goto or point to the next song in the playlist.
        """
        # go select the next song. No need to play here
        if self.cur == None:
            print("no song selected")
            return
        self.cur = self.cur.next

    def play_previous(self):
        """
        Goto or point to the previous song in the playlist.        
        """
        # same as next
        if self.cur == None:
            print("no song selected")
            return
        self.cur = self.cur.prev

    def is_empty(self):
        '''returns True if playlist is empty'''
        return self.start is None

    def __repr__(self):
        rep_playlist = []
        current = self.start
        while current:
            rep_playlist.append(current)
            current = current.next
        return str(rep_playlist)

    def __iter__(self):
        self.current_iter = self.start
        return self

    def __next__(self):
        if self.current_iter is None:
            raise StopIteration
        song = self.current_iter
        self.current_iter = self.current_iter.next
        return song
