import time

import pymongo
from metaflow import FlowSpec, Parameter, kubernetes, step, schedule
from threads import Threads

from models.thread import ThreadModel
from models.user import UserModel
from utils.database import default_db as threadsdb
from utils.settings import MongoSettings
from utils.utils import process_user_data, process_user_threads

@schedule(hourly=True)
class ThreadsETL(FlowSpec):
    """
    A flow to pull user and threads from the Threads API
    and store them in MongoDB.

    """

    mongodb_host = Parameter(
        "mongodb_host", help="Host of the mongodb instance.", default="mongodb.threads.svc.cluster.local"
    )

    mongodb_port = Parameter(
        "mongodb_port", help="Port of the mongodb instance.", default="27017"
    )

    mongodb_database = Parameter(
        "threadsdb", help="Database name.", default="threadsdb"
    )

    mongodb_username = Parameter(
        "mongodb_username",
        help="Username to authenticate to the mongodb instance.",
        default="user",
    )

    mongodb_password = Parameter(
        "mongodb_password",
        help="Password to authenticate to the mongodb instance.",
        default="password",
    )

    seconds_to_poll_for_data = Parameter(
        "seconds_to_poll_for_data",
        help="The number of seconds you want to poll the Threads API for data.",
        default=1800,
    )

    @kubernetes(image="zacharybloss/threads-collection")
    @step
    def start(self):
        print("HelloFlow is starting.")

        mongo_settings = MongoSettings(
            username=self.mongodb_username,
            password=self.mongodb_password,
            host=self.mongodb_host,
            port=self.mongodb_port,
            database=self.mongodb_database,
        )

        self.mongo_client = pymongo.MongoClient(mongo_settings.uri)
        self.users_collection = threadsdb["users"]
        self.threads_collection = threadsdb["threads"]
        self.highest_user_id = 0
        self.threads_client = Threads()

        self.next(self.get_highest_user_id)

    @kubernetes(image="zacharybloss/threads-collection")
    @step
    def get_highest_user_id(self):
        """
        Attempts to pull the highest user id
        from the users collection.

        """
        try:
            if self.users_collection.count_documents({}) > 0:
                # get highest user id
                highest_user = (
                    self.users_collection.find()
                    .sort("pk", pymongo.DESCENDING)
                    .limit(1)[0]
                )
                self.highest_user_id = int(highest_user["pk"])
        except IndexError:
            print("user_collection does not exist.")
            pass
        self.next(self.poll_for_data)

    @kubernetes(image="zacharybloss/threads-collection")
    @step
    def poll_for_data(self):
        """
        Polls data from the Threads API for approximately
        `self.seconds_to_poll_for_data` seconds.

        """

        current_time = time.time()
        end_time = current_time + self.seconds_to_poll_for_data
        while current_time < end_time:
            current_time = time.time()

            self.highest_user_id += 1
            user = self.threads_client.public_api.get_user(id=self.highest_user_id)
            if user["data"] is not None:
                processed_user_data = process_user_data(user)
                processed_user = UserModel(**processed_user_data)
                self.users_collection.insert_one(processed_user.model_dump())
                users_added += 1

                # get users Threads
                user_threads = self.threads_client.public_api.get_user_threads(
                    id=self.highest_user_id
                )
                if user_threads is None:
                    # API probably was rate-limited, try again.
                    time.sleep(10)
                    self.threads_client = Threads()
                    user_threads = self.threads_client.public_api.get_user_threads(
                        id=self.highest_user_id
                    )

                try:
                    user_threads = process_user_threads(user_threads)
                except:
                    user_threads = []

                if len(user_threads) > 0:
                    validated_threads = []
                    for thread_ in user_threads:
                        validated_threads.append(ThreadModel(**thread_).model_dump())
                    self.threads_collection.insert_many(validated_threads)
                    threads_added += len(validated_threads)

            counter += 1
            if counter % 10:
                try:
                    total_users = self.users_collection.count_documents({})
                    total_threads = self.threads_collection.count_documents({})
                    print(
                        f"Total Users: {total_users} | Total Threads: {total_threads}"
                    )
                except:
                    pass

            time.sleep(2)
        self.next(self.end)

    @kubernetes(image="zacharybloss/threads-collection")
    @step
    def end(self):
        """
        This is the 'end' step. All flows must have an 'end' step, which is the
        last step in the flow.

        """
        print("HelloFlow is all done.")

if __name__ == '__main__':
    ThreadsETL()