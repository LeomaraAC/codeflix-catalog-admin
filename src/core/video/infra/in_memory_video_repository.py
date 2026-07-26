from src.core.video.domain.video import Video
from src.core.video.domain.video_repository import VideoRepository
from uuid import UUID

class InMemoryVideoRepository(VideoRepository):
	def __init__(self):
		self.videos: list[Video] = []

	def save(self, video: Video) -> None:
		self.videos.append(video)

	def get_by_id(self, id: UUID) -> Video | None:
		return next((video for video in self.videos if video.id == id), None)

	def delete(self, id: UUID) -> None:
		video = self.get_by_id(id)
		if video:
			self.videos.remove(video)

	def update(self, video: Video) -> None:
		if video not in self.videos:
			return
		index = self.videos.index(video)
		self.videos[index] = video

	def list(self) -> list[Video]:
		return [video for video in self.videos]