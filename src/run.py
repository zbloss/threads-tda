import time

import pymongo
from threads import Threads

from models.thread import ThreadModel
from models.user import UserModel
from utils.database import default_db as threadsdb
from utils.utils import process_user_data, process_user_threads


def main():
    threads_client = Threads()
    users_collection = threadsdb["users"]
    threads_collection = threadsdb["threads"]

    highest_user_id = 0
    try:
        if users_collection.count_documents({}) > 0:
            # get highest user id
            highest_user = (
                users_collection.find().sort("pk", pymongo.DESCENDING).limit(1)[0]
            )
            highest_user_id = int(highest_user["pk"])
    except IndexError:
        print("user_collection does not exist.")
        pass

    counter = 0
    users_added = 0
    threads_added = 0
    while True:
        # get next user from Threads
        highest_user_id += 1
        user = threads_client.public_api.get_user(id=highest_user_id)
        if user["data"] is not None:
            processed_user_data = process_user_data(user)
            processed_user = UserModel(**processed_user_data)
            users_collection.insert_one(processed_user.model_dump())
            users_added += 1

            # get users Threads
            user_threads = threads_client.public_api.get_user_threads(
                id=highest_user_id
            )
            if user_threads is None:
                # API probably was rate-limited, try again.
                time.sleep(10)
                threads_client = Threads()
                user_threads = threads_client.public_api.get_user_threads(
                    id=highest_user_id
                )

            try:
                user_threads = process_user_threads(user_threads)
            except:
                user_threads = []

            if len(user_threads) > 0:
                validated_threads = []
                for thread_ in user_threads:
                    validated_threads.append(ThreadModel(**thread_).model_dump())
                threads_collection.insert_many(validated_threads)
                threads_added += len(validated_threads)

        counter += 1
        if counter % 10:
            try:
                total_users = users_collection.count_documents({})
                total_threads = threads_collection.count_documents({})
                print(f"Total Users: {total_users} | Total Threads: {total_threads}")
            except:
                pass

        time.sleep(2)


if __name__ == "__main__":
    print("Starting threads calls...")
    main()
    print("Finished")
