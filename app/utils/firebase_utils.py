from firebase_admin import auth, firestore
import datetime

db = firestore.client()

def create_user(email, password, display_name):
    """Create a new user with Firebase Authentication"""
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        
        # Create user profile in Firestore
        db.collection('users').document(user.uid).set({
            'email': email,
            'displayName': display_name,
            'createdAt': datetime.datetime.now(),
            'reports': 0,
            'cleanups': 0
        })
        
        return user
    except Exception as e:
        print(f"Error creating user: {e}")
        return None

def get_lakes():
    """Get all lakes from Firestore"""
    lakes = []
    lakes_ref = db.collection('lakes')
    
    try:
        docs = lakes_ref.stream()
        for doc in docs:
            lake_data = doc.to_dict()
            lake_data['id'] = doc.id
            lakes.append(lake_data)
    except Exception as e:
        print(f"Error getting lakes: {e}")
    
    return lakes

def get_lake(lake_id):
    """Get a specific lake by ID"""
    try:
        doc = db.collection('lakes').document(lake_id).get()
        if doc.exists:
            lake_data = doc.to_dict()
            lake_data['id'] = doc.id
            return lake_data
    except Exception as e:
        print(f"Error getting lake: {e}")
    
    return None

def get_events(lake_id=None):
    """Get cleanup events, optionally filtered by lake"""
    events = []
    events_ref = db.collection('events')
    
    if lake_id:
        query = events_ref.where('lake_id', '==', lake_id)
    else:
        query = events_ref
    
    try:
        docs = query.order_by('date').stream()
        for doc in docs:
            event_data = doc.to_dict()
            event_data['id'] = doc.id
            events.append(event_data)
    except Exception as e:
        print(f"Error getting events: {e}")
    
    return events

def join_event(event_id, user_id):
    """Add a user to an event's participants"""
    try:
        event_ref = db.collection('events').document(event_id)
        event_ref.update({
            'participants': firestore.ArrayUnion([user_id])
        })
        
        # Update user's cleanup count
        user_ref = db.collection('users').document(user_id)
        user_ref.update({
            'cleanups': firestore.Increment(1)
        })
        
        return True
    except Exception as e:
        print(f"Error joining event: {e}")
        return False

def create_report(user_id, lake_id, description, pollution_level, location=None):
    """Create a pollution report for a lake (no image)"""
    try:
        report_ref = db.collection('reports').document()
        report_data = {
            'user_id': user_id,
            'lake_id': lake_id,
            'description': description,
            'pollution_level': pollution_level,
            'location': location,  # GeoPoint if provided
            'timestamp': datetime.datetime.now(),
            'status': 'reported'  # reported, in_progress, cleaned
        }
        
        report_ref.set(report_data)
        
        # Update user's report count
        user_ref = db.collection('users').document(user_id)
        user_ref.update({
            'reports': firestore.Increment(1)
        })
        
        return report_ref.id
    except Exception as e:
        print(f"Error creating report: {e}")
        return None

def get_reports(lake_id=None):
    """Get pollution reports, optionally filtered by lake"""
    reports = []
    reports_ref = db.collection('reports')
    
    if lake_id:
        query = reports_ref.where('lake_id', '==', lake_id)
    else:
        query = reports_ref
    
    try:
        docs = query.order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            report_data = doc.to_dict()
            report_data['id'] = doc.id
            reports.append(report_data)
    except Exception as e:
        print(f"Error getting reports: {e}")
    
    return reports

def seed_sample_data():
    """Seed the database with sample lakes and events"""
    # Sample lakes near a location (replace with coordinates near your college)
    lakes = [
        {
            'name': 'College Lake',
            'location': firestore.GeoPoint(12.9716, 77.5946),
            'area': 3.5,  # in square kilometers
            'health_index': 65,  # 0-100 scale
            'description': 'Lake adjacent to the college campus. Faces moderate pollution from nearby residential areas.',
            'common_pollutants': ['plastic bottles', 'food wrappers', 'plastic bags'],
            'last_cleanup': datetime.datetime.now() - datetime.timedelta(days=30)
        },
        {
            'name': 'City Park Lake',
            'location': firestore.GeoPoint(12.9846, 77.6046),
            'area': 2.8,
            'health_index': 72,
            'description': 'Popular recreational lake in the city park. Visited by many tourists and locals.',
            'common_pollutants': ['plastic cups', 'cigarette butts', 'food packaging'],
            'last_cleanup': datetime.datetime.now() - datetime.timedelta(days=15)
        },
        {
            'name': 'Eco Reserve Pond',
            'location': firestore.GeoPoint(12.9656, 77.5746),
            'area': 1.2,
            'health_index': 88,
            'description': 'Protected pond in the ecological reserve. Home to several bird species.',
            'common_pollutants': ['occasional litter'],
            'last_cleanup': datetime.datetime.now() - datetime.timedelta(days=7)
        },
        {
            'name': 'Industrial Zone Lake',
            'location': firestore.GeoPoint(12.9916, 77.6146),
            'area': 5.1,
            'health_index': 42,
            'description': 'Lake near the industrial zone. Faces significant pollution challenges.',
            'common_pollutants': ['industrial waste', 'plastic debris', 'chemical containers'],
            'last_cleanup': datetime.datetime.now() - datetime.timedelta(days=60)
        },
        {
            'name': 'Community Reservoir',
            'location': firestore.GeoPoint(13.0046, 77.5896),
            'area': 4.3,
            'health_index': 58,
            'description': 'Reservoir serving the local community. Moderate pollution from agricultural runoff.',
            'common_pollutants': ['fertilizer containers', 'plastic sheets', 'bags'],
            'last_cleanup': datetime.datetime.now() - datetime.timedelta(days=45)
        }
    ]
    
    # Add lakes to Firestore
    lake_ids = []
    for lake in lakes:
        doc_ref = db.collection('lakes').document()
        doc_ref.set(lake)
        lake_ids.append(doc_ref.id)
    
    # Sample cleanup events
    events = [
        {
            'lake_id': lake_ids[0],  # College Lake
            'title': 'College Lake Cleanup Day',
            'description': 'Join fellow students for our monthly lake cleanup event!',
            'date': datetime.datetime.now() + datetime.timedelta(days=3),
            'start_time': '09:00 AM',
            'duration': 3,  # hours
            'meeting_point': 'North Shore of College Lake',
            'organizer': 'Student Environmental Club',
            'participants': [],
            'max_participants': 30,
            'equipment_provided': ['gloves', 'trash bags', 'pickers'],
            'equipment_to_bring': ['water bottle', 'sunscreen', 'hat']
        },
        {
            'lake_id': lake_ids[1],  # City Park Lake
            'title': 'Weekend Warriors: Lake Cleanup',
            'description': 'Community cleanup initiative at City Park Lake. All are welcome!',
            'date': datetime.datetime.now() + datetime.timedelta(days=5),
            'start_time': '10:00 AM',
            'duration': 4,  # hours
            'meeting_point': 'City Park Main Entrance',
            'organizer': 'City Environmental Department',
            'participants': [],
            'max_participants': 50,
            'equipment_provided': ['gloves', 'trash bags', 'refreshments'],
            'equipment_to_bring': ['comfortable shoes', 'water bottle']
        },
        {
            'lake_id': lake_ids[3],  # Industrial Zone Lake
            'title': 'Industrial Lake Restoration Project',
            'description': 'Major cleanup effort for our most polluted lake. Volunteers needed!',
            'date': datetime.datetime.now() + datetime.timedelta(days=7),
            'start_time': '08:30 AM',
            'duration': 6,  # hours
            'meeting_point': 'Eastern Shore Parking Lot',
            'organizer': 'Clean Water Initiative',
            'participants': [],
            'max_participants': 100,
            'equipment_provided': ['protective gear', 'trash bags', 'tools', 'lunch'],
            'equipment_to_bring': ['sturdy boots', 'water bottle', 'work gloves']
        },
        {
            'lake_id': lake_ids[4],  # Community Reservoir
            'title': 'Reservoir Cleanup & Education Day',
            'description': 'Combine cleanup with learning about water conservation.',
            'date': datetime.datetime.now() + datetime.timedelta(days=14),
            'start_time': '09:00 AM',
            'duration': 5,  # hours
            'meeting_point': 'Community Center Parking',
            'organizer': 'Water Conservation Society',
            'participants': [],
            'max_participants': 40,
            'equipment_provided': ['educational materials', 'cleanup tools', 'snacks'],
            'equipment_to_bring': ['notebook', 'pen', 'water bottle', 'hat']
        }
    ]
    
    # Add events to Firestore
    for event in events:
        db.collection('events').document().set(event)
    
    return True