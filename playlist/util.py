import csv
from song import Song

class FileUtil:

	@staticmethod
	def display_songs_by_singer(singer_name : str, song_pool: list):
		"""'''Displays all songs by a given singer from a pool of songs.'''

		Args:
			singer_name (str): name of the singer
			song_pool (list): list of songs available to add to your playlist
		"""

		songs_by_singer = [song for song in song_pool if song.artist == singer_name]
		for song in songs_by_singer:
			print(song)

	@staticmethod
	def load_songs_from_csv(filename: str) -> list:
		"""
		Loads songs from a CSV file into a list of Song objects.

		Args:
			filename (str): name of the CSV file

		Returns:
			list: list of Song objects
		"""
		songs = []
		with open(filename, mode='r', encoding='utf-8') as file:
			reader = csv.DictReader(file)
			for row in reader:
				song = Song(
					idx=int(row["id"]),
					name=row["song_name"],
					artist=row["artist"],
					youtube_id=row["youtube_id"],
					views=float(row["views"]),
					run_time=float(row["run_time"])
				)
				songs.append(song)
		return songs
