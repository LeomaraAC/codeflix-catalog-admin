from src.core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType


class TestAudioVideoMedia:
    def test_complete_returns_new_completed_instance(self) -> None:
        media = AudioVideoMedia(
            name='video.mp4',
            media_type=MediaType.VIDEO,
            raw_location='videos/video.mp4',
            encoded_location='',
            status=MediaStatus.PENDING,
        )

        completed_media = media.complete('videos/video-encoded.mp4')

        assert completed_media is not media
        assert completed_media == AudioVideoMedia(
            name='video.mp4',
            media_type=MediaType.VIDEO,
            raw_location='videos/video.mp4',
            encoded_location='videos/video-encoded.mp4',
            status=MediaStatus.COMPLETED,
        )

    def test_fail_returns_new_error_instance_with_empty_encoded_location(self) -> None:
        media = AudioVideoMedia(
            name='video.mp4',
            media_type=MediaType.VIDEO,
            raw_location='videos/video.mp4',
            encoded_location='videos/video-encoded.mp4',
            status=MediaStatus.PROCESSING,
        )

        failed_media = media.fail()

        assert failed_media is not media
        assert failed_media == AudioVideoMedia(
            name='video.mp4',
            media_type=MediaType.VIDEO,
            raw_location='videos/video.mp4',
            encoded_location='',
            status=MediaStatus.ERROR,
        )