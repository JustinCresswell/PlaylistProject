from song import Song
from playlist import PlayList


def test_add_to_empty():
	my_playlist = PlayList("My Playlist")
	my_song = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	my_playlist.add(my_song)
	# Assert that the song has been added to the playlist
	assert my_playlist.start == my_song


def test_add_at_index():
	playlist = PlayList("My Playlist")
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 1200, 4.0)
	playlist.add(song1)
	playlist.add(song2)
	new_song = Song(3, "New Song", "Artist 3", "ijkl789", 800, 3.0)
	# Add the new song at index 1 (between song1 and song2)
	playlist.add(new_song, index=1)
	# Verify that the new song is at the correct position
	assert playlist.start.next == new_song
	assert new_song.prev == song1
	assert new_song.next == song2


def test_add_song_at_end():
	playlist = PlayList("My Playlist")
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 1200, 4.0)
	playlist.add(song1)
	playlist.add(song2)
	new_song = Song(3, "New Song", "Artist 3", "ijkl789", 800, 3.0)
	# Add the new song without specifying an index
	playlist.add(new_song)
	# Verify that the new song is at the end of the playlist
	assert song2.next == new_song


def test_add_with_invalid_index():
	playlist = PlayList("My Playlist")
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 1200, 4.0)
	playlist.add(song1)
	playlist.add(song2)
	new_song = Song(3, "New Song", "Artist 3", "ijkl789", 800, 3.0)
	# Attempt to add the new song at an invalid index
	playlist.add(new_song, index=5)
	# Verify that the playlist remains unchanged
	assert playlist.start == song1
	assert song1.next == song2
	assert song2.next is None


def test_remove_by_name():
	# Create a playlist with some songs
	playlist = PlayList("My Playlist")
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 800, 3.0)
	song3 = Song(3, "Song 3", "Artist 1", "ijkl789", 1200, 4.0)
	playlist.add(song1)
	playlist.add(song2)
	playlist.add(song3)

	# Test removing a song by name
	playlist.remove_by_name("Song 2")

	# Check if the first song is as expected
	assert playlist.start.name == "Song 1"
	# Check if the next song is as expected
	assert playlist.start.next.name == "Song 3"
	# Check if the next song's prev is updated
	assert playlist.start.next.prev.name == "Song 1"
	assert playlist.end.name == "Song 3"  # Check if the end is as expected

	# Test removing the first song by name
	playlist.remove_by_name("Song 1")
	assert playlist.start.name == "Song 3"  # Check if the first song is updated
	# Check if the previous of the new first song is None
	assert playlist.start.prev is None

	# Test removing a non-existent song by name
	playlist.remove_by_name("Non-Existent Song")
	# Check if the playlist remains unchanged
	assert playlist.start.name == "Song 3"

	# Test removing the last song by name
	playlist.remove_by_name("Song 3")
	assert playlist.start is None  # Check if the playlist becomes empty
	assert playlist.end is None


def test_remove_by_index():
	# Create a playlist with some songs
	playlist = PlayList("My Playlist")
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 800, 3.0)
	song3 = Song(3, "Song 3", "Artist 3", "ijkl789", 1200, 4.0)
	playlist.add(song1)
	playlist.add(song2)
	playlist.add(song3)

	# Test removing a song at a valid index
	playlist.remove_by_index(1)  # Remove the second song
	assert playlist.length == 2
	assert playlist.start == song1
	assert playlist.end == song3
	assert song1.next == song3
	assert song3.prev == song1

	# Test removing the first song
	playlist.remove_by_index(0)
	assert playlist.length == 1
	assert playlist.start == song3
	assert playlist.end == song3
	assert song3.next is None
	assert song3.prev is None

	# Test removing a song at an invalid index
	playlist.remove_by_index(1)  # Index out of range
	assert playlist.length == 1  # Playlist should remain unchanged


def test_clear():
	playlist = PlayList("My Playlist")
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 800, 4.0)

	# Add songs to the playlist
	playlist.add(song1)
	playlist.add(song2)

	# Verify that the playlist is not empty
	assert playlist.length == 2

	# Clear the playlist
	playlist.clear()

	# Verify that the playlist is now empty
	assert playlist.length == 0
	assert playlist.start is None
	assert playlist.end is None
	assert playlist.cur is None


def test_reverse_empty_playlist():
	playlist = PlayList("My Playlist")
	playlist.reverse()
	# Verify that the playlist remains empty
	assert playlist.start is None
	assert playlist.end is None


def test_reverse_one_song():
	playlist = PlayList("My Playlist")
	song = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	playlist.add(song)
	playlist.reverse()
	# Verify that the playlist still contains the same song
	assert playlist.start == song
	assert playlist.end == song


def test_reverse_multiple_songs():
	playlist = PlayList("My Playlist")
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 1500, 4.0)
	song3 = Song(3, "Song 3", "Artist 3", "ijkl789", 800, 2.0)

	playlist.add(song1)
	playlist.add(song2)
	playlist.add(song3)

	playlist.reverse()

	# Verify that the playlist is reversed
	assert playlist.start == song3
	assert playlist.end == song1
	assert song3.next == song2
	assert song2.prev == song3
	assert song2.next == song1
	assert song1.prev == song2


def test_total_count():
	# Create an empty playlist
	playlist = PlayList("My Playlist")
	assert playlist.total_count() == 0

	# Add a song to the playlist
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	playlist.add(song1)
	assert playlist.total_count() == 1  # Playlist should have 1 song

	# Add more songs
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 2000, 4.0)
	song3 = Song(3, "Song 3", "Artist 3", "ijkl789", 1500, 3.0)
	playlist.add(song2)
	playlist.add(song3)
	assert playlist.total_count() == 3  # Playlist should have 3 songs

	# Remove a song
	playlist.remove_by_name("Song 2")
	print(playlist.length)
	assert playlist.total_count() == 2  # Playlist should have 2 songs after removal

	# Clear the playlist
	playlist.clear()
	assert playlist.total_count() == 0  # Playlist should be empty again


def test_total_view_empty_playlist():
	playlist = PlayList()
	total_views = playlist.total_view()
	assert total_views == 0


def test_total_view_single_song():
	playlist = PlayList()
	song = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	playlist.add(song)
	total_views = playlist.total_view()
	assert total_views == 1000


def test_total_view_multiple_songs():
	playlist = PlayList()
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 2000, 4.0)
	song3 = Song(3, "Song 3", "Artist 3", "ijkl789", 1500, 3.0)
	playlist.add(song1)
	playlist.add(song2)
	playlist.add(song3)
	total_views = playlist.total_view()
	assert total_views == 4500


def test_total_runtime_empty_playlist():
	playlist = PlayList("My Playlist")
	assert playlist.total_runtime() == 0.0


def test_total_runtime_single_song():
	song = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	playlist = PlayList("My Playlist")
	playlist.add(song)
	assert playlist.total_runtime() == 3.5


def test_total_runtime_multiple_songs():
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 1500, 4.0)
	song3 = Song(3, "Song 3", "Artist 3", "ijkl789", 800, 2.5)
	playlist = PlayList("My Playlist")
	playlist.add(song1)
	playlist.add(song2)
	playlist.add(song3)
	assert playlist.total_runtime() == 10.0


def test_display_empty_playlist():
	playlist = PlayList("My Playlist")
	# The playlist is empty, so nothing should be displayed.
	playlist.display()


def test_display_single_song():
	song = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	playlist = PlayList("My Playlist")
	playlist.add(song)
	playlist.display()  # Since there's only one song, it should be displayed.


def test_display_multiple_songs():
	song1 = Song(1, "Song 1", "Artist 1", "abcd123", 1000, 3.5)
	song2 = Song(2, "Song 2", "Artist 2", "efgh456", 1500, 4.0)
	song3 = Song(3, "Song 3", "Artist 3", "ijkl789", 800, 2.5)
	playlist = PlayList("My Playlist")
	playlist.add(song1)
	playlist.add(song2)
	playlist.add(song3)
	playlist.display()
	playlist.display(chunk_size=2)  # Display the songs in chunks of 2.

