from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
from services.api_client import APIClient
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

api = APIClient(
    base_url=os.getenv('API_BASE_URL', "https://<api-key-identifier>.execute-api.eu-central-1.amazonaws.com/dev"),
    api_key=os.getenv('API_KEY', 'dev-local-key-CHANGE-ME')
)

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin' not in session:
            flash('Please log in first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            flash('Logged in successfully', 'success')
            return redirect(url_for('list_vpcs'))
        else:
            flash('Invalid credentials', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('admin', None)
    flash('Logged out', 'success')
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'admin' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('list_vpcs'))


@app.route('/vpcs')
@login_required
def list_vpcs():
    try:
        result = api.list_vpcs()
        vpcs = result.get('items', [])
        return render_template('vpcs/list.html', vpcs=vpcs)
    except Exception as e:
        flash(f'Error loading VPCs: {str(e)}', 'error')
        return render_template('vpcs/list.html', vpcs=[])


@app.route('/vpcs/create', methods=['GET', 'POST'])
@login_required
def create_vpc():
    if request.method == 'POST':
        try:
            vpc = api.create_vpc(
                vpc_name=request.form['vpc_name'],
                cidr_block=request.form['cidr_block'],
                region=request.form['region']
            )
            flash(f'VPC created: {vpc["vpc_id"]}', 'success')
            return redirect(url_for('list_vpcs'))
        except Exception as e:
            flash(f'Error creating VPC: {str(e)}', 'error')
    return render_template('vpcs/create.html')


@app.route('/vpcs/<vpc_id>')
@login_required
def get_vpc(vpc_id):
    try:
        vpc = api.get_vpc(vpc_id)
        subnets = api.list_subnets_by_vpc(vpc_id).get('items', [])
        return render_template('vpcs/detail.html', vpc=vpc, subnets=subnets)
    except Exception as e:
        flash(f'Error loading VPC: {str(e)}', 'error')
        return redirect(url_for('list_vpcs'))


@app.route('/vpcs/<vpc_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_vpc(vpc_id):
    if request.method == 'POST':
        try:
            data = {}
            if request.form.get('vpc_name'):
                data['vpc_name'] = request.form['vpc_name']
            if request.form.get('region'):
                data['region'] = request.form['region']
            if request.form.get('status'):
                data['status'] = request.form['status']

            api.update_vpc(vpc_id, **data)
            flash('VPC updated', 'success')
            return redirect(url_for('get_vpc', vpc_id=vpc_id))
        except Exception as e:
            flash(f'Error updating VPC: {str(e)}', 'error')

    try:
        vpc = api.get_vpc(vpc_id)
        return render_template('vpcs/edit.html', vpc=vpc)
    except Exception as e:
        flash(f'Error loading VPC: {str(e)}', 'error')
        return redirect(url_for('list_vpcs'))


@app.route('/vpcs/<vpc_id>/delete', methods=['POST'])
@login_required
def delete_vpc(vpc_id):
    try:
        api.delete_vpc(vpc_id)
        flash('VPC deleted', 'success')
    except Exception as e:
        flash(f'Error deleting VPC: {str(e)}', 'error')
    return redirect(url_for('list_vpcs'))


@app.route('/subnets')
@login_required
def list_subnets():
    try:
        result = api.list_subnets()
        subnets = result.get('items', [])
        return render_template('subnets/list.html', subnets=subnets)
    except Exception as e:
        flash(f'Error loading subnets: {str(e)}', 'error')
        return render_template('subnets/list.html', subnets=[])


@app.route('/vpcs/<vpc_id>/subnets/create', methods=['GET', 'POST'])
@login_required
def create_subnet(vpc_id):
    if request.method == 'POST':
        try:
            subnet = api.create_subnet(
                vpc_id=vpc_id,
                subnet_name=request.form['subnet_name'],
                cidr_block=request.form['cidr_block'],
                availability_zone=request.form.get('availability_zone') or None
            )
            flash(f'Subnet created: {subnet["subnet_id"]}', 'success')
            return redirect(url_for('get_vpc', vpc_id=vpc_id))
        except Exception as e:
            flash(f'Error creating subnet: {str(e)}', 'error')

    try:
        vpc = api.get_vpc(vpc_id)
        return render_template('subnets/create.html', vpc=vpc)
    except Exception as e:
        flash(f'Error loading VPC: {str(e)}', 'error')
        return redirect(url_for('list_vpcs'))


@app.route('/subnets/<subnet_id>')
@login_required
def get_subnet(subnet_id):
    try:
        subnet = api.get_subnet(subnet_id)
        return render_template('subnets/detail.html', subnet=subnet)
    except Exception as e:
        flash(f'Error loading subnet: {str(e)}', 'error')
        return redirect(url_for('list_subnets'))


@app.route('/subnets/<subnet_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_subnet(subnet_id):
    if request.method == 'POST':
        try:
            data = {}
            if request.form.get('subnet_name'):
                data['subnet_name'] = request.form['subnet_name']
            if request.form.get('status'):
                data['status'] = request.form['status']

            api.update_subnet(subnet_id, **data)
            flash('Subnet updated', 'success')
            return redirect(url_for('get_subnet', subnet_id=subnet_id))
        except Exception as e:
            flash(f'Error updating subnet: {str(e)}', 'error')

    try:
        subnet = api.get_subnet(subnet_id)
        return render_template('subnets/edit.html', subnet=subnet)
    except Exception as e:
        flash(f'Error loading subnet: {str(e)}', 'error')
        return redirect(url_for('list_subnets'))


@app.route('/subnets/<subnet_id>/delete', methods=['POST'])
@login_required
def delete_subnet(subnet_id):
    try:
        subnet = api.get_subnet(subnet_id)
        vpc_id = subnet['vpc_id']
        api.delete_subnet(subnet_id)
        flash('Subnet deleted', 'success')
        return redirect(url_for('get_vpc', vpc_id=vpc_id))
    except Exception as e:
        flash(f'Error deleting subnet: {str(e)}', 'error')
        return redirect(url_for('list_subnets'))


if __name__ == '__main__':
    app.run(debug=True)
