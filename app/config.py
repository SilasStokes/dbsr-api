from pydantic import BaseSettings
import os

# print(f'inside config {__file__} cwd: {os.path.dirname(__file__)}')
# env_path = os.path.dirname(__file__)
class Settings(BaseSettings):
    database_hostname: str 
    database_port: str 
    database_password: str 
    database_name: str 
    database_username: str
    
    class Config(BaseSettings.Config):
        env_file = os.path.join(os.path.dirname(__file__), '.env')


settings = Settings() # type: ignore