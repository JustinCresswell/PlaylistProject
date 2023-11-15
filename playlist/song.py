class Song:
	def __init__(self, idx: int = -1, name: str = None, artist: str = None, youtube_id: str = None, views: float = 0.0, run_time: float = 0.0) -> None:
		self.idx : int = idx
		self.name : str = name
		self.artist : str = artist
		self.youtube_id: str = youtube_id
		self.views : float = views
		self.run_time: float = run_time
		self.next : Song = None
		self.prev : Song = None


	def __repr__(self) -> str:
		"""
		Returns a string representation of the song.

		Returns:
			str: string representation of the song
		"""
		return str(str(self.idx) + '.' + str(self.name))