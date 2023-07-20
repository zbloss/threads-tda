import time


def process_user_data(user_data: dict) -> dict:
    """Extracts important fields from the user response"""

    if "data" in user_data.keys():
        user_data = user_data["data"]

    if "userData" in user_data.keys():
        user_data = user_data["userData"]

    if "user" in user_data.keys():
        user_data = user_data["user"]

    biography_entities = []
    if "biography_with_entities" in user_data:
        if "entities" in biography_entities:
            biography_entities = biography_entities["entities"]
        else:
            biography_entities = []

    user_id = user_data["pk"] if user_data["id"] is None else user_data["id"]

    keys_to_drop = [
        "profile_pic_url",
        "hd_profile_pic_versions",
        "biography_with_entities",
        "profile_context_facepile_users",
        "id",
    ]
    for key in keys_to_drop:
        try:
            user_data.pop(key)
        except KeyError:
            pass

    user_data["user_id"] = user_id
    user_data["biography_entities"] = biography_entities
    user_data["_id"] = user_id

    return user_data


def process_user_threads(thread_data: dict) -> list:
    """Extracts important fields from each thread response"""
    if "data" in thread_data.keys():
        thread_data = thread_data["data"]

    if "mediaData" in thread_data.keys():
        thread_data = thread_data["mediaData"]

    if "threads" in thread_data.keys():
        thread_data = thread_data["threads"]

    processed_threads = []
    for item in thread_data:
        for thread_item in item["thread_items"]:
            post = thread_item["post"]
            thread_id = post["id"]

            username = post["user"]["username"]
            user_id = post["user"]["pk"]
            user_verified = post["user"]["is_verified"]

            image_height = post["original_height"]
            image_width = post["original_width"]
            has_audio = False if post["has_audio"] is None else True

            quoted = post["text_post_app_info"]["share_info"]["quoted_post"]
            reposted = post["text_post_app_info"]["share_info"]["reposted_post"]
            is_post_unavailable = post["text_post_app_info"]["is_post_unavailable"]
            was_post_taken_down = not is_post_unavailable

            text = ""
            if "caption" in post.keys():
                if post["caption"] is not None:
                    if "text" in post["caption"].keys():
                        text = post["caption"]["text"]

            posted_timestamp = post["taken_at"]
            posted_datetime = time.strftime(
                "%Y-%m-%d %H:%M:%S", time.gmtime(posted_timestamp)
            )

            likes = post["like_count"]

            processed_threads.append(
                {
                    "_id": thread_id,
                    "thread_id": thread_id,
                    "username": username,
                    "user_id": user_id,
                    "is_user_verified": user_verified,
                    "image_height": image_height,
                    "image_width": image_width,
                    "has_audio": has_audio,
                    "quoted_count": quoted,
                    "reposted_count": reposted,
                    "likes_count": likes,
                    "is_post_unavailable": is_post_unavailable,
                    "was_post_taken_down": was_post_taken_down,
                    "text": text,
                    "posted_timestamp": posted_timestamp,
                    "posted_datetime": posted_datetime,
                }
            )

    return processed_threads
