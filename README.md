**Live Demo:** [https://lakeguardian.onrender.com](https://lakeguardian.onrender.com)

## 🌊 About LakeGuardian

LakeGuardian is a web platform dedicated to monitoring and restoring Dundigal Lake near our college campus. Through real-time data collection, community engagement, and educational resources, we aim to combat water pollution and preserve this vital freshwater ecosystem.

## 🔍 Problem Statement

Dundigal Lake faces severe water pollution from industrial waste, sewage, and littering. This has led to degraded water quality, decreased biodiversity, and health risks for surrounding communities. Despite its importance as a local water resource, there is limited awareness and no coordinated effort to address these issues.

## 🛠️ Solution Approach

LakeGuardian combines real-time pollution monitoring with community action. Our platform uses water quality sensors to track pollution levels, visualizes data through an intuitive dashboard, and coordinates cleanup events. Users can report pollution incidents, access educational resources, and participate in restoration activities.

## ✨ Key Features

- **Water Quality Monitoring:** Track real-time pollution levels with interactive dashboards
- **Pollution Reporting:** Allow users to report pollution incidents with location and photos
- **Community Engagement:** Coordinate cleanup drives and conservation events
- **Educational Resources:** Provide information about lake ecosystems and conservation methods
- **Progress Tracking:** Visualize improvement in water quality over time

## 🔌 Technologies Used

### Google Technologies
- **Firebase Authentication & Firestore:** User management and real-time database
- **Google Maps API:** Visualize pollution hotspots and cleanup locations
- **Google Cloud Storage:** Store water quality data and user-submitted images
- **Gemini API:** AI-powered insights on pollution patterns
- **Google Cloud Functions:** Process sensor data and send automated alerts

### Other Technologies
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap
- **Backend:** Python with Flask framework
- **Deployment:** Render for web hosting

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Firebase account
- Google Maps API key
- Google Cloud account (for Gemini API)

### Installation

1. Clone the repository
```bash
git clone https://github.com/akshtih/lakeguardian.git
cd lakeguardian
```

2. Set up a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
```bash
cp .env.example .env
# Edit .env file with your API keys and configuration
```

5. Run the development server
```bash
python run.py
```

