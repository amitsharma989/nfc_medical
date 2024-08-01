from flask import Flask, request, jsonify, render_template
from models import db, MedicalInfo
from ncf_utils import read_nfc, write_nfc

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medical_info.db?timeout=10'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30
db.init_app(app)

@app.cli.command('create-db')
def create_db():
    with app.app_context():
        db.create_all()
    print("Database tables created.")

@app.route('/update-medical-info', methods=['GET'])
def update_medical_info_page():
    return render_template('update-medical-info.html')

@app.route('/get-medical-info', methods=['GET'])
def get_medical_info_page():
    return render_template('get-medical-info.html')

def get_read_page():
    return render_template('read-nfc.html')

@app.route('/write-nfc', methods=['GET'])
def get_write_nfc():
    return render_template('write-nfc.html')

@app.route('/read-nfc', methods=['GET'])
def get_read_nfc():
    return render_template('read-nfc.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/read-nfc/<tag_id>', methods=['GET'])
def handle_read_nfc(tag_id):
    try:
        data = read_nfc(tag_id)
        print(f"handleeeeeeeeredaddd{tag_id}anddd{data}")
        if isinstance(data, dict):
            return jsonify({"status": "success", "data": data}), 200
        else:
            return jsonify({"status": "error", "message": data}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/write-nfc', methods=['POST'])
def handle_write_nfc():
    """Writes data to an NFC tag."""
    data = request.json
    medical_id = data.get('medical_id')
    tag_id = data.get('nfc_tag_id')
    if not medical_id or not tag_id:
        return jsonify({"status": "error", "message": "No data provided"}), 400
    try:
        url = write_nfc(medical_id, tag_id)
        return jsonify({"status": "success", "url": url}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/update-medical-info', methods=['POST'])
def update_medical_info():
    """Updates medical info in the database."""
    data = request.json
    medical_id = data.get('medical_id')
    if medical_id:
        medical_record = MedicalInfo.query.filter_by(medical_id=medical_id).first()
        if medical_record:
            for key, value in data.items():
                setattr(medical_record, key, value)
        else:
            medical_record = MedicalInfo(**data)
            db.session.add(medical_record)
        try:
            
            db.session.commit()
        except Exception as e:
              db.session.rollback()  
              print(f"Error: {str(e)}")
        return jsonify({"status": "success", "message": "Medical info updated"}), 200
    return jsonify({"status": "error", "message": "Medical ID not found"}), 404

@app.route('/get-medical-info/<medical_id>', methods=['GET'])
def get_medical_info(medical_id):
    """Retrieves medical info from the database."""
    print(f"medical_id {medical_id} and {type(medical_id)}")
    medical_record = MedicalInfo.query.filter_by(medical_id=medical_id).first()
    if medical_record:
        return jsonify({
            "name": medical_record.name,
            "medical_id": medical_record.medical_id,
            "allergies": medical_record.allergies,
            "blood_type": medical_record.blood_type,
            "medical_conditions": medical_record.medical_conditions,
            "medications": medical_record.medications,
            "emergency_contact": medical_record.emergency_contact,
            "primary_physician": medical_record.primary_physician,
            "insurance_info": medical_record.insurance_info,
            "organ_donor": medical_record.organ_donor,
            "other_info": medical_record.other_info
        }), 200
    return jsonify({"status": "error", "message": "Medical ID not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
