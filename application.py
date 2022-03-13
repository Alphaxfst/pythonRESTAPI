from flask import Flask, request
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    address = db.Column(db.String(200))

    def __repr__(self):
        return f"{self.name} - {self.address}"


@app.route('/')
def index():
    return 'Hello!'

@app.route('/customers')
def get_customers():
    customers = Customers.query.all()

    output = []
    for customer in customers:
        customer_data = {'name': customer.name, 'address': customer.address}
        output.append(customer_data)    
    return {"customers": output}

@app.route('/customers/<id>')
def get_customer(id):
    customer = Customers.query.get_or_404(id)
    return {'name': customer.name, 'address': customer.address}

@app.route('/customers', methods=['POST'])
def add_customer():
    customer = Customers(name=request.json['name'],
                         address=request.json['address'])
    db.session.add(customer)
    db.session.commit()
    return {'id': customer.id}

@app.route('/customers/<id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customers.query.get(id)
    if customer is None:
        return {"error": "not found"}
    db.session.delete(customer)
    db.session.commit()
    return {"message": "successfully deleted"}

if __name__ == '__main__':
    app.run(debug=True)