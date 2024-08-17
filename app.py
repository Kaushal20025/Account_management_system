from flask import Flask, render_template, request, redirect, url_for
from models import db, Account, Transaction, Report
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Manually create the tables when the app starts
with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    # Fetch all reports from the database
    reports = Report.query.all()
    return render_template('dashboard.html', reports=reports)

@app.route('/accounts')
def view_accounts():
    accounts = Account.query.all()
    return render_template('accounts.html', accounts=accounts)

@app.route('/accounts/add', methods=['GET', 'POST'])
def add_account():
    if request.method == 'POST':
        new_account = Account(
            name=request.form['name'],
            credit = request.form['credit'],
            debit =request.form['debit'],
            balance=float(request.form['balance'])
        )
        db.session.add(new_account)
        db.session.commit()
        return redirect(url_for('view_accounts'))
    return render_template('add_account.html')

@app.route('/transactions')
def view_transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions)

@app.route('/transactions/add', methods=['GET', 'POST'])
def add_transaction():
    if request.method == 'POST':
        account_id = int(request.form['account_id'])
        
        # Check if the account exists
        account = Account.query.get(account_id)
        
        if not account:
            return "Account does not exist. Please create the account first.", 400
        
        new_transaction = Transaction(
            account_id=account_id,
            type=request.form['type'],
            amount=float(request.form['amount'])
        )
        db.session.add(new_transaction)
        db.session.commit()
        return redirect(url_for('view_transactions'))
    
    accounts = Account.query.all()  # To display accounts in a dropdown, if needed
    return render_template('add_transaction.html', accounts=accounts)

@app.route('/reports')
def view_reports():
    reports = Report.query.all()
    return render_template('reports.html', reports=reports)

@app.route('/reports/generate', methods=['GET', 'POST'])
def generate_report():
    if request.method == 'POST':
        report_type = request.form['type']
        report_date = request.form['date']

        if not report_type or not report_date:
            return "Please fill out all fields.", 400

        new_report = Report(
            type=report_type,
            date=report_date
        )
        db.session.add(new_report)
        db.session.commit()
        return redirect(url_for('view_reports'))

    return render_template('generate_report.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True)