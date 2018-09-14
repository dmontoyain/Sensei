#YAY

if __name__ == '__main__':
	from rq42.api42 import Api42
	from api.app import app
	Api42.runActiveUserUpdater(300)
	app.run(host="0.0.0.0",port=1025)