from web_app import sentiment_app

app = sentiment_app()

if __name__ == '__main__':
    app.run(debug=True)