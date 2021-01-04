# Django eshop simulation

# Project Description
- Backend: Python, Django
- Frontend: Html, CSS, Javascript, Bootstrap
- Database technologies: XAMPP, MySQL
## Users
- Users passwords get hashed and stored
- Unregister users cannot access eshop functionalities. Can only browse the store.
- User can log in and logout. User credentials are stored using django sessions
- User have a relevant profile with personal information. They can also can see ordered items,date ordered and quantity.

## Website
- Product images are stored in database as BLOB format
- User cart is made with cookies
- User can specify the quantity of a product before purchase
- Order data are sent to the backend using Fetch API