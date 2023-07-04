from website import create_app
from website import request, render_template, redirect, url_for

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
