from flask import  jsonify, render_template_string
from flask import url_for

def write_nfc(medical_id, tag_id):
 
    from models import NfcTag, MedicalInfo, db
    try:
      
        medical_details = MedicalInfo.query.get(medical_id)
      
        if medical_details is None:
            return "Error: medical_id not found"
        
        tag_details = NfcTag.query.get(tag_id)
        
        if tag_details:
            tag_details.medical_id = medical_id
        else:
            tag_details = NfcTag(tag_id=tag_id, medical_id=medical_id)
            db.session.add(tag_details)
        
        db.session.commit()
        view_url = url_for('get_medical_info', medical_id=medical_id, _external=True)
        print("view_url", view_url)
       
        return view_url
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return f"Error: {str(e)}"



def read_nfc(tag_id):
    from models import NfcTag, MedicalInfo, db

    try:
    
        nfc_tag = NfcTag.query.filter_by(tag_id=tag_id).first()
        if nfc_tag is None:
            return jsonify({"error": "No data found for tag_id"}), 404
        
        medical_record = MedicalInfo.query.filter_by(medical_id=nfc_tag.medical_id).first()
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
    except Exception as e:
       
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500