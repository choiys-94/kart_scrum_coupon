from app import create_app


app = create_app()

def main():
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = True

    app.run(debug=DEBUG, port=PORT, host=HOST)

if __name__ == "__main__":
    main()