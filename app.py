from flask import Flask, render_template, request, redirect, url_for, flash
import os
import json
import random

app = Flask(__name__)
app.secret_key = b"#1234567#7654321"

database = {}
with open('customers.json') as fp:
    database = json.load(fp)


@app.route('/')
def home():
    return render_template('home.template.html')


@app.route('/customers')
def show_customers():
    return render_template('customers.template.html', all_customers=database)


@app.route('/customers/add')
def show_add_customers():
    return render_template('add_customer.template.html', old_values={}, errors={})


@app.route('/customers/add', methods=["POST"])
def process_add_customers():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')

    # use dictionary to store error messages
    errors = {}

    # check firstname provided
    if not first_name:
        errors["first_name"] = "Please provide a valid first name"
    if not last_name:
        errors["last_name"] = "Please provide a valid last name"
    if not email:
        errors["email"] = "Please provide a valid email"
    if '@' not in email:
        errors["email"] = "Wrong Email Format"

    if 'can_send' in request.form:
        can_send = True
    else:
        can_send = False

    if len(errors) == 0:
        new_customer = {
            "id": random.randint(1000, 9999),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "can_send": can_send
        }

        database.append(new_customer)

        with open('customers.json', 'w') as fp:
            json.dump(database, fp)

        flash(
            f"The customer with the name {new_customer['first_name']} {new_customer['last_name']}"
            f" has been created successfully")

        return redirect(url_for('show_customers'))
    else:
        for key, value in errors.items():
            flash(value, "error")

        return render_template("add_customer.template.html", old_values=request.form, errors=errors)


@app.route('/customers/<int:customer_id>/edit')
def show_edit_customer(customer_id):
    customer_to_edit = None
    for each_customer in database:
        if each_customer["id"] == customer_id:
            customer_to_edit = each_customer
            break
    if customer_to_edit:
        return render_template("edit_customer.template.html", customer=customer_to_edit)
    else:
        return f"The customer with the id of {customer_id} is not found"


@app.route('/customers/<int:customer_id>/edit', methods=["POST"])
def process_edit_customer(customer_id):
    customer_to_edit = None
    for each_customer in database:
        if each_customer["id"] == customer_id:
            customer_to_edit = each_customer
            break

    errors = {}
    if not request.form.get('first_name'):
        errors["first_name"] = "Please provide a valid first name"
    if not request.form.get('last_name'):
        errors["last_name"] = "Please provide a valid last name"
    if not request.form.get('email'):
        errors["email"] = "Please provide a valid email"
    if '@' not in request.form.get('email'):
        errors["email"] = "Wrong Email Format"

    if customer_to_edit:
        if len(errors) == 0:
            customer_to_edit["first_name"] = request.form.get("first_name")
            customer_to_edit["last_name"] = request.form.get("last_name")
            customer_to_edit["email"] = request.form.get("email")

            if 'can_send' in request.form:
                customer_to_edit["can_send"] = True
            else:
                customer_to_edit["can_send"] = False

            with open('customers.json', 'w') as fp:
                json.dump(database, fp)
            flash(
                f"The customer with the name {customer_to_edit['first_name']} {customer_to_edit['last_name']}"
                f" has been EDITED successfully")
            return redirect(url_for("show_customers"))
        else:
            return render_template('edit_customer.template.html', customer=request.form, errors=errors)
    else:
        for key, value in errors.items():
            flash(value, "error")
        return f"The customer with the id of {customer_id} is not found"


@app.route('/customers/<int:customer_id>/delete')
def show_delete_customer(customer_id):
    customer_to_delete = None
    for each_customer in database:
        if each_customer["id"] == customer_id:
            customer_to_delete = each_customer
            break
    if customer_to_delete:
        return render_template("delete_customer.template.html", customer=customer_to_delete)
    else:
        return f"The customer with the id of {customer_id} is NOT found!"


@app.route('/customers/<int:customer_id>/delete', methods=["POST"])
def process_delete_customer(customer_id):
    customer_to_delete = None
    for each_customer in database:
        if each_customer["id"] == customer_id:
            customer_to_delete = each_customer
            break
    if customer_to_delete:
        database.remove(customer_to_delete)
        with open('customer.json', 'w') as fp:
            json.dump(database, fp)

        flash(
            f"The customer with the name {customer_to_delete['first_name']} {customer_to_delete['last_name']}"
            f" has been DELETED successfully")

        return redirect(url_for("show_customers"))
    else:
        return f"The customer with the id of {customer_id} is NOT found!"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),  # or '0.0.0.0'
            port=int(os.environ.get('PORT')),  # or 8080
            debug=True)
