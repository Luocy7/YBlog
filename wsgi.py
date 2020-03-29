import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from yblog import create_app

app = create_app('prd')

if __name__ == '__main__':
    app.run(port=5001)
