GROUP = 1
if GROUP == 1:
    from avtoserv import app
if __name__ == '__main__':

    app.run(debug=True)