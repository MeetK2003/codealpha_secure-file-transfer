import os 

class Config:
	SECRET_KEY = 'supersecretkey123'
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	JWT_SECRET_KEY = 'anothersecretkey456'
