def get_gdpr_obligations(data_types, automated_decisions, user_types):
    obligations = []
    articles = []

    # Basic personal data — always applies
    if any(d in data_types for d in ['personal', 'behavioral', 'location', 'financial', 'biometric', 'health', 'children']):
        obligations.append('Establish a lawful basis for processing personal data (consent, contract, or legitimate interest)')
        obligations.append('Provide a clear and accessible privacy notice to all affected individuals')
        obligations.append('Implement data minimization — only collect what is strictly necessary')
        obligations.append('Define and enforce data retention periods — do not keep data longer than needed')
        articles.append('Art. 5 — Principles of processing')
        articles.append('Art. 6 — Lawful basis for processing')
        articles.append('Art. 13/14 — Transparency and privacy notice')

    # Special category data — stricter rules
    special_category = ['biometric', 'health']
    if any(d in data_types for d in special_category):
        obligations.append('Obtain explicit consent for processing special category data (biometric or health data)')
        obligations.append('Appoint a Data Protection Officer (DPO) — mandatory for large scale processing of sensitive data')
        obligations.append('Conduct a Data Protection Impact Assessment (DPIA) before processing begins')
        articles.append('Art. 9 — Special category data')
        articles.append('Art. 35 — Data Protection Impact Assessment')
        articles.append('Art. 37 — Appointment of DPO')

    # Children's data — extra protection
    if 'children' in data_types:
        obligations.append('Obtain verifiable parental consent for users under 16')
        obligations.append('Apply enhanced data protection measures for children\'s data')
        obligations.append('Avoid profiling or behavioral advertising targeting children')
        articles.append('Art. 8 — Conditions for children\'s consent')

    # Automated decision making
    if automated_decisions == 'yes':
        obligations.append('Inform individuals when automated decision-making is being used')
        obligations.append('Provide individuals the right to request human review of automated decisions')
        obligations.append('Explain the logic behind automated decisions when requested')
        obligations.append('Conduct a DPIA specifically for the automated decision-making process')
        articles.append('Art. 22 — Automated individual decision-making')

    # Vulnerable users
    if 'vulnerable' in user_types or 'children' in user_types:
        obligations.append('Apply enhanced safeguards for vulnerable or at-risk user groups')
        obligations.append('Ensure consent mechanisms are appropriate for vulnerable populations')
        articles.append('Art. 9 — Enhanced protection for vulnerable groups')

    # Individual rights — always applies
    obligations.append('Respect individual rights: access, rectification, erasure, portability, and objection')
    articles.append('Art. 15-21 — Individual rights')

    return {
        'obligations': obligations,
        'articles': articles,
        'dpia_required': (
            any(d in data_types for d in special_category) or
            automated_decisions == 'yes' or
            'children' in data_types
        )
    }