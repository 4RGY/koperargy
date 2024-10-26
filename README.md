
# Sistem Informasi Koperasi - Koperargy

Koperargy is a simple cooperative information system developed using Flask. This application is designed to easily manage member and transaction data for cooperatives.. (not fully developed)


## Features

- Login: Provides secure access for registered users to manage or view cooperative information. Only authenticated users can access certain features.
- Register: Allows new members to register and create accounts with basic information, which grants them access to member-exclusive features.
- Home Page: Welcomes users with an overview of the cooperative, showcasing its mission, services, and contact information.
- About: Contains information on the cooperative’s mission, vision, and background.
- CRUD for Members: Enables admins to create, read, update, and delete member information.
- CRUD for Transactions: Lets admins manage cooperative transactions, including adding, viewing, editing, and deleting transaction records.


## Installation

1. Clone the Repository

```bash
git clone https://github.com/username/koperargy.git
cd koperargy
```

2. Set Up a Virtual Environment & Install Dependencies

```bash
python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate      # For Windows
pip install -r requirements.txt
```

3. Run the Application

```bash
flask run
```
Open your browser and go to http://127.0.0.1:5000 to access the application.

    
## Contributing

We encourage contributions from the community. To contribute:

1. Fork the repository.
2. Create a new branch with your feature or bug fix.
3. Submit a pull request with a description of your changes.

