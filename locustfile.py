import random, string
from locust import HttpLocust, TaskSet, task

def generate_str(length=1):
    return "".join(random.choice(string.ascii_lowercase) for i in range(length))

class UserBehavior(TaskSet):
    @task(2)
    def submit_url_1(self):
        self.client.post("/", {"longUrl":"https://www.youtube.com/results?search_query=2015+songs+playlist"})
    @task(1)
    def index(self):
        self.client.get("/")

    @task(3)
    def submit_url_2(self):
        self.client.post("/",{"longUrl":"https://screen.yahoo.com/live/event/edc-3", "shortUrl":"a"})

    @task(2)
    def get_url(self):
        for i in range(2000):
            result = generate_str(1)
            self.client.get("/"+result)


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait=5000
    max_wait=9000