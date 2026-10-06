from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5010, host='0.0.0.0')
else:
    gunicorn_app = app