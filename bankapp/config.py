from pydantic import BaseSettings

class Settings(BaseSettings):
    simulator_host: str = "http://localhost:8090/sim"
