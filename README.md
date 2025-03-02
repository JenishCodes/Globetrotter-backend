# Set Up
1. Clone this repo
2. Prerequisite Python and PostgreSQL should be install
3. Run `python3 -m venv venv` command to create virtual env and keep dependencies separate.
4. Run `pip3 install -r requirements.txt` command to install require packages
5. Add below code to main.py file
   ```if __name__ == "__main__":
    print("Starting app...")
    app.run()```
6. Add .env file with variable values mentioned in app/config.py file, below would be values if running on localhost
   ```
      # App Config
      FLASK_ENV=development
      DEBUG=True
      
      # Database Config
      SQLALCHEMY_DATABASE_URI=postgresql://nerdguy:nerdguy@localhost:5432/globetrotter
      SQLALCHEMY_TRACK_MODIFICATIONS=True
      
      # JWT Config
      JWT_SECRET=super-secret
      JWT_ACCESS_TOKEN_EXPIRES=86400
      
      # CORS Config
      CORS_ORIGIN=http://localhost:3000
      
      # URLs
      URL = http://localhost:5000
      FRONTEND_URL = http://localhost:3000
   ```
7. Run `flask run` command
8. Once server is started, check by calling home url (127.0.0.1:5000)
9. If it gives welcome message then call 127.0.0.1:5000/auth/loader API to load data from json to db
10. If it gives message data loaded successfully then server is ready for frontend.

# Tech choice
- For REST implementation I choose Flask because of easy to use nature.
- For database I have used PostgreSQL cause its highly available and has many supportive libraries
- For authentication I have used JWT 
