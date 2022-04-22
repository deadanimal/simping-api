# Run a test server.
from apps import app
from decouple import config

if __name__ == "__main__":
    app.run(debug=config('DEBUG'))
