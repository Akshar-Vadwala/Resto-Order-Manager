# Resto Order Manager

[![License: Creative Commons](https://img.shields.io/badge/License-CC_BY--NC_4.0-blue.svg)](https://creativecommons.org/licenses/by-nc/4.0/deed.en)

## Description

Resto-Order-Manager is a comprehensive Django web application designed to streamline restaurant operations and facilitate online food ordering and delivery. It provides a user-friendly platform for customers to browse menus, add items to their cart, and place orders seamlessly through the Stripe payment gateway. On the restaurant side, it offers robust tools for managing orders, updating menu items, generating reports, and ensuring efficient operations.

## Features

### Customer Experience:
- Browse menus
- Add items to cart
- Seamless Stripe payment integration
- Download Bill pdfs

### Restaurant Management:
- Order management
- Menu updates
- Reporting tools

## Tech Stack

- **Backend:** Python Django
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript
- **IDE:** Spyder
- **Python:** 3.11.4
- **Django:** 5.0.6
- **Payment Gateway:** Stripe (test mode)

## Demo Video

![](/demo.gif)

## Usage

1. Clone this repository:

    ```bash
    git clone https://github.com/Akshar-Vadwala/resto-order-manager.git
    ```

2. Install the required dependencies as mentioned in techstack.


3. Set up the MySQL database by creating a database named `resto_order_manager` and applying the migrations:

    ```bash
    python manage.py migrate
    ```

4. Run the Django development server:

    ```bash
    python manage.py runserver
    ```

5. Access the application in your web browser at `http://localhost:8000`.

## Contribution

Contributions to this project are welcome! Here's how you can help:

- Use the project for testing and provide feedback on its functionality and user experience.
- Suggest enhancements to improve the user interface and overall experience.
- Report any bugs or issues you encounter while using the application.
- Enhance the codebase by fixing bugs, optimizing performance, or adding new features.

Please note that commercial use of the code or any derived work is not allowed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/deed.en). Contributions should align with the non-commercial nature of the project.

Feel free to fork the repository, make your changes, and submit a pull request. Your contributions are appreciated!

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/deed.en). See the [LICENSE](LICENSE) file for details.
