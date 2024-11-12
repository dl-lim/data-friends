from dotenv import load_dotenv
import os

load_dotenv()

# Add environmental values and set defaults if none available
HOST = os.getenv('HOST') if 'HOST' in os.environ else '0.0.0.0'
PORT = os.getenv('PORT') if 'PORT' in os.environ else '8000'