from decouple import config

TOKEN = config('TOKEN')
RAPID_API = config('RAPID_API')
ADMIN_ID = config('ADMIN_ID')
NGROK_TOKEN = config('NGROK_TOKEN')

# webhook settings
WEBHOOK_HOST = 'http://127.0.0.1'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"https://{NGROK_TOKEN}.ngrok.io"

# webserver settings
WEBAPP_HOST = '127.0.0.1'  # or ip
WEBAPP_PORT = 3001
