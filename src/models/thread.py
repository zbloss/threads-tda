from pydantic import BaseModel

class Thread(BaseModel):
    thread_id: str
    username: str
    user_id: str
    is_user_verified: bool
    image_height: int | None
    image_width: int | None
    has_audio: bool
    quoted_count: int | None
    reposted_count: int | None
    likes_count: int | None
    is_post_unavailable: bool | None
    was_post_taken_down: bool | None
    text: str | None
    posted_timestamp: int | None
    posted_datetime: str | None
        
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                'thread_id': '3140546144073699340_4',
                'username': 'mikeyk',
                'user_id': '4',
                'is_user_verified': True,
                'image_height': 1440,
                'image_width': 1920,
                'has_audio': False,
                'quoted_count': None,
                'reposted_count': None,
                'likes_count': 48,
                'is_post_unavailable': False,
                'was_post_taken_down': True,
                'text': 'To start, our design wizard gunnargray built the original cards in Cinema4D. We wanted the cards to look distinct from each other as you level up, and for the "higher level" cards to feel premium/metallic.',
                'posted_timestamp': 1688602296,
                'posted_datetime': '2023-07-06 00:11:36'
            }
        }