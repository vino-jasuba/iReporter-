from app import create_app
import os
import settings

if __name__ == '__main__':
    app = create_app(os.getenv('APP_ENV'))
    app.run()
