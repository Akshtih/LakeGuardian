from flask import render_template, redirect, url_for, request, flash, jsonify, session
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.models import User
from app.utils.firebase_utils import (
    create_user, get_lakes, get_lake, get_events, join_event,
    create_report, get_reports, seed_sample_data
)
from app.utils.gemini_utils import init_gemini, get_lake_chatbot_response
from firebase_admin import auth, firestore

@app.before_request
def before_request():
    # Initialize Gemini API
    if app.config.get('GEMINI_API_KEY'):
        init_gemini()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        display_name = request.form.get('display_name')
        
        try:
            print(f"Attempting to create user: {email}, {display_name}")  # Debug print
            user = create_user(email, password, display_name)
            if user:
                # Create User object for Flask-Login
                user_obj = User(user.uid, email, display_name)
                login_user(user_obj)
                flash('Registration successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Registration failed. Please try again.', 'danger')
                print("User creation returned None")  # Debug print
        except Exception as e:
            error_msg = f"Registration error: {str(e)}"
            flash(error_msg, 'danger')
            print(error_msg)  # Debug print
            import traceback
            traceback.print_exc()  # Print full traceback to console
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # This is a simplified login for demo purposes
            # In a real app, you should use Firebase client SDK for auth
            user = User.get_by_email(email)
            if user:
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid email or password', 'danger')
        except Exception as e:
            flash('Login failed. Please try again.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get all lakes
    lakes = get_lakes()
    
    # If no lakes found, seed sample data
    if not lakes:
        seed_sample_data()
        lakes = get_lakes()
    
    # Convert GeoPoint objects to serializable format
    serialized_lakes = []
    for lake in lakes:
        serialized_lake = dict(lake)
        if 'location' in serialized_lake and hasattr(serialized_lake['location'], 'latitude'):
            serialized_lake['location'] = {
                'latitude': serialized_lake['location'].latitude,
                'longitude': serialized_lake['location'].longitude
            }
        # Convert datetime objects to strings
        if 'last_cleanup' in serialized_lake and serialized_lake['last_cleanup']:
            serialized_lake['last_cleanup'] = serialized_lake['last_cleanup'].isoformat()
        serialized_lakes.append(serialized_lake)
    
    return render_template('dashboard.html', lakes=serialized_lakes)

@app.route('/lake/<lake_id>')
@login_required
def lake_detail(lake_id):
    lake = get_lake(lake_id)
    if not lake:
        flash('Lake not found', 'danger')
        return redirect(url_for('dashboard'))
    
    reports = get_reports(lake_id)
    events = get_events(lake_id)
    
    return render_template('lake_detail.html', lake=lake, reports=reports, events=events)

@app.route('/events')
@login_required
def events():
    all_events = get_events()
    lakes = get_lakes()
    
    # Create a dictionary of lake names by ID for easy reference
    lake_dict = {lake['id']: lake['name'] for lake in lakes}
    
    return render_template('events.html', events=all_events, lakes=lake_dict)

@app.route('/join_event/<event_id>', methods=['POST'])
@login_required
def join_cleanup_event(event_id):
    success = join_event(event_id, current_user.id)
    
    if success:
        flash('Successfully joined the cleanup event!', 'success')
    else:
        flash('Failed to join the event. Please try again.', 'danger')
    
    return redirect(url_for('events'))

@app.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    lakes = get_lakes()
    
    if request.method == 'POST':
        lake_id = request.form.get('lake_id')
        description = request.form.get('description')
        pollution_level = request.form.get('pollution_level')
        
        # Create report without image
        report_id = create_report(
            user_id=current_user.id,
            lake_id=lake_id,
            description=description,
            pollution_level=pollution_level
        )
        
        if report_id:
            flash('Report submitted successfully!', 'success')
            return redirect(url_for('lake_detail', lake_id=lake_id))
        else:
            flash('Failed to submit report. Please try again.', 'danger')
    
    return render_template('report.html', lakes=lakes)

@app.route('/education')
@login_required
def education():
    return render_template('education.html')

@app.route('/ask', methods=['POST'])
def ask():
    """Handle questions to the lake conservation AI assistant."""
    try:
        # Get the question from the request
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Missing question parameter'}), 400
            
        question = data['question']
        
        # Get response from Gemini AI
        response = get_lake_chatbot_response(question)
        
        # Return the response
        return jsonify({'answer': response})
    except Exception as e:
        app.logger.error(f"Error in /ask endpoint: {str(e)}")
        return jsonify({'error': 'Failed to get response', 'details': str(e)}), 500