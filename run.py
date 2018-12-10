from app import create_app
import os

if __name__ == '__main__':
    app = create_app(os.getenv('APP_ENV', 'production'))
    app.run()
