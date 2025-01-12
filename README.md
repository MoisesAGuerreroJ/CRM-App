# CRM App - Customer and Referral Management

## Description

The **CRM App** is an application designed to manage the registration, modification, and tracking of customers and referrals. Its main functionality is to allow the addition and modification of the personal information required for specific products, as well as the efficient handling of referrals through the **4 in 14 format**, a system used to register clients and referrals with key information for their tracking and management. This tool is aimed at improving the sales process, automating referral management, and ensuring that relevant customer data remains up-to-date.

## Main Features

- **Customer and Referral Registration**: Allows the registration and storage of personal information for customers and their referrals, such as names, contact details, etc.
- **4 in 14 Format**: Integration of the standardized format to ensure consistency and order in the database.
- **Data Updates**: Customer and referral information can be modified as necessary to keep the database up to date.
- **User-friendly Interface**: Intuitive UI/UX to facilitate user interaction without complications.

### Technology and Architecture

- **Backend**: Implemented with a Flask server that handles user requests and manages the database.
- **Frontend**: A web interface implemented in ______ to allow users to interact with the system.
- **Database**: Uses MySQL to securely store customer, referral, and interaction data.
- **REST API**: Provides a RESTful API for easy integration with other applications and external services.

## Requirements

### Necessary Software

- List of required software or dependencies
  - Python 3.11
  - MySQL 8.4.2
  - Docker
  - Docker Compose
  - 

### Setup

1. **Clone the repository**: Clone this repository to your local machine using:

```bash
git clone https://github.com/MoisesAGuerreroJ/CRM-App.git
```
2. **Run Docker Compose**: Open CRM-App folder and run docker using:

```bash
cd CRM-App/
docker compose up -d
```