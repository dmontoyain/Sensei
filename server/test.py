#YAY

if __name__ == '__main__':
	from rq42.api42 import Api42
	from api.app import app
	app.run(host="0.0.0.0",port=1025)