from flask import Flask, render_template, request, jsonify, send_file
from engine.db import init_db, save_assessment, get_assessment, get_history
from engine.eu_ai_act import classify_eu_ai_act
from engine.gdpr import get_gdpr_obligations
from engine.iso27001 import get_iso_controls
from engine.risk_score import calculate_risk_score
from engine.report import generate_report
from engine.soa import generate_soa
from engine.nis2 import get_nis2_obligations
from engine.dora import get_dora_obligations
from engine.iso42001 import get_iso42001_controls
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assess')
def assess():
    return render_template('assess.html')

@app.route('/results', methods=['POST'])
def results():
    system_name = request.form.get('system_name')
    system_type = request.form.get('system_type')
    description = request.form.get('description')
    data_types = request.form.getlist('data_types')
    user_types = request.form.getlist('user_types')
    automated_decisions = request.form.get('automated_decisions')
    human_override = request.form.get('human_override')
    decision_impact = request.form.get('decision_impact')
    has_security_policy = request.form.get('has_security_policy')
    has_dpo = request.form.get('has_dpo')
    previous_assessment = request.form.get('previous_assessment')
    sector = request.form.get('sector')
    org_size = request.form.get('org_size')

    eu_result = classify_eu_ai_act(system_type, data_types, automated_decisions, human_override)
    gdpr_result = get_gdpr_obligations(data_types, automated_decisions, user_types)
    risk_result = calculate_risk_score(data_types, decision_impact, automated_decisions, human_override, user_types, has_security_policy, has_dpo, previous_assessment)
    iso_result = get_iso_controls(data_types, eu_result['classification'], automated_decisions, has_security_policy)
    nis2_result = get_nis2_obligations(sector, org_size)
    dora_result = get_dora_obligations(sector, org_size)
    iso42001_result = get_iso42001_controls(system_type, eu_result['classification'], automated_decisions)

    history = get_history(system_name) if system_name else []

    full_data = {
        'system_name': system_name,
        'system_type': system_type,
        'description': description,
        'eu_result': eu_result,
        'gdpr_result': gdpr_result,
        'risk_result': risk_result,
        'iso_result': iso_result,
        'nis2_result': nis2_result,
        'dora_result': dora_result,
        'iso42001_result': iso42001_result
    }

    assessment_id = save_assessment(
        system_name, system_type,
        risk_result['score'], risk_result['level'],
        eu_result['classification'], full_data
    )

    return render_template('results.html',
        assessment_id=assessment_id,
        system_name=system_name,
        system_type=system_type,
        description=description,
        eu_result=eu_result,
        gdpr_result=gdpr_result,
        risk_result=risk_result,
        iso_result=iso_result,
        nis2_result=nis2_result,
        dora_result=dora_result,
        iso42001_result=iso42001_result,
        history=history
    )

@app.route('/results/<assessment_id>')
def view_assessment(assessment_id):
    data = get_assessment(assessment_id)
    if not data:
        return "Assessment not found", 404

    history = get_history(data['system_name']) if data.get('system_name') else []

    return render_template('results.html',
        assessment_id=assessment_id,
        system_name=data.get('system_name'),
        system_type=data.get('system_type'),
        description=data.get('description'),
        eu_result=data.get('eu_result'),
        gdpr_result=data.get('gdpr_result'),
        risk_result=data.get('risk_result'),
        iso_result=data.get('iso_result'),
        nis2_result=data.get('nis2_result'),
        dora_result=data.get('dora_result'),
        iso42001_result=data.get('iso42001_result'),
        history=history
    )

@app.route('/download-report', methods=['POST'])
def download_report():
    data = request.get_json()
    pdf_path = generate_report(data)
    return send_file(pdf_path, as_attachment=True, download_name='ClarityGRC_Report.pdf')

@app.route('/download-soa', methods=['POST'])
def download_soa():
    data = request.get_json()
    pdf_path = generate_soa(data)
    return send_file(pdf_path, as_attachment=True, download_name='ClarityGRC_Statement_of_Applicability.pdf')

@app.route('/explain', methods=['POST'])
def explain():
    data = request.get_json()

    from groq import Groq
    client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

    prompt = f"""You are an AI governance consultant. A company has just assessed their AI system using ClarityGRC. Here are their results:

- System type: {data.get('system_type')}
- EU AI Act classification: {data.get('eu_classification')}
- Risk score: {data.get('risk_score')} - {data.get('risk_level')}
- GDPR obligations: {', '.join(data.get('gdpr_obligations', []))}
- ISO 27001 controls recommended: {', '.join([c['id'] + ' ' + c['name'] for c in data.get('iso_controls', [])])}

Write a clear, plain English paragraph (max 150 words) explaining what this means for the company, what they must do next, and what happens if they don't comply. Write directly to the company, not about them."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )

    return jsonify({'explanation': response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)