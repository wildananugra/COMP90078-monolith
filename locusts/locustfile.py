import time
from locust import HttpUser, task, between

class Monolith(HttpUser):
    wait_time = between(1, 2.5)
    token = None
    host = "http://localhost:8080"

    @task
    def get_parameter(self):
        response = self.client.get(f"{self.host}/parameter/", headers={ "Authorization" : "Bearer " + self.token })

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    def on_start(self):
        response = self.client.post("/token", data={'username': 'admin', 'password': 'password'}).json()
        self.token = response['access_token']

class Monolith2(HttpUser):
    wait_time = between(1, 2.5)
    token = None
    host = "http://localhost:8080"

    @task
    def get_parameter(self):
        response = self.client.get(f"{self.host}/parameter/", headers={ "Authorization" : "Bearer " + self.token })

    # @task(3)
    # def view_items(self):
    #     for item_id in range(10):
    #         self.client.get(f"/item?id={item_id}", name="/item")
    #         time.sleep(1)

    def on_start(self):
        response = self.client.post("/token", data={'username': 'admin', 'password': 'password'}).json()
        self.token = response['access_token']