from app import app
import os


@app.cli.command("clear-cache")
def clear_cache():
    """ Delete expired cache directory """
    pass


if __name__ == "__main__":
    ####################
    # FOR DEVELOPMENT
    ####################
    app.run(host='0.0.0.0', port=os.environ.get(
        "FLASK_SERVER_PORT", 5000), debug=True, use_reloader=True)
