from app import create_app

if __name__ == '__main__':
    config_env = 'test'
    app = create_app('test')
    app.run(debug=True, use_reloader=False)