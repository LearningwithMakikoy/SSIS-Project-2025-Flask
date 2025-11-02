from app import create_app

# Use the application factory so blueprints and extensions are configured
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
