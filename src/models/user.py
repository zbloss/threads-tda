from pydantic import BaseModel

class UserModel(BaseModel):
    pk: str
    user_id: str | None
    username: str
    
    full_name: str | None
    biography: str | None
    is_verified: bool
    follower_count: int
    biography_entities: list | None
    bio_links: list[dict[str, str]]
    is_private: bool
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                'is_private': False,
                'username': 'mikeyk',
                'is_verified': True,
                'biography': 'Co-founder of Instagram and former CTO. Working on Artifact.',
                'follower_count': 56792,
                'bio_links': [{'url': 'https://artifact.news'}],
                'pk': '4',
                'full_name': 'Mike Krieger',
                'id': None,
                'biography_entities': []
            }
        }