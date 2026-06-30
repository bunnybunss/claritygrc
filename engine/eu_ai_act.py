def classify_eu_ai_act(system_type, data_types, automated_decisions, human_override):
    
    # UNACCEPTABLE RISK — banned outright
    unacceptable_systems = ['social_scoring', 'realtime_biometric_public']
    if system_type in unacceptable_systems:
        return {
            'classification': 'UNACCEPTABLE RISK',
            'color': 'red',
            'meaning': 'This AI system is banned under the EU AI Act. It cannot be deployed in the European Union under any circumstances.',
            'obligations': [
                'This system cannot be deployed in the EU',
                'Immediate cessation of development is required',
                'Legal counsel should be consulted immediately'
            ]
        }

    # HIGH RISK — heavily regulated
    high_risk_systems = ['hiring', 'credit_scoring', 'medical', 'education', 'law_enforcement', 'border_control', 'critical_infrastructure']
    high_risk_data = ['biometric', 'health', 'criminal']

    is_high_risk = (
        system_type in high_risk_systems or
        any(d in data_types for d in high_risk_data) or
        (automated_decisions == 'yes' and human_override == 'no')
    )

    if is_high_risk:
        return {
            'classification': 'HIGH RISK',
            'color': 'orange',
            'meaning': 'This AI system is classified as high risk under the EU AI Act. It is legal but subject to strict obligations before and during deployment.',
            'obligations': [
                'Mandatory conformity assessment before deployment',
                'Registration in the EU database of high-risk AI systems',
                'Comprehensive technical documentation required',
                'Human oversight mechanisms must be in place',
                'Ongoing monitoring and incident reporting required',
                'Transparency obligations to affected individuals'
            ]
        }

    # LIMITED RISK — transparency obligations only
    limited_risk_systems = ['customer_service', 'chatbot', 'content_recommendation', 'emotion_recognition']
    if system_type in limited_risk_systems:
        return {
            'classification': 'LIMITED RISK',
            'color': 'yellow',
            'meaning': 'This AI system has limited risk. Users must be informed they are interacting with an AI system.',
            'obligations': [
                'Inform users they are interacting with an AI',
                'Clear disclosure when AI generates content',
                'Basic transparency documentation recommended'
            ]
        }

    # MINIMAL RISK — no obligations
    return {
        'classification': 'MINIMAL RISK',
        'color': 'green',
        'meaning': 'This AI system poses minimal risk under the EU AI Act. No mandatory obligations apply, but good practices are recommended.',
        'obligations': [
            'No mandatory obligations under the EU AI Act',
            'Voluntary codes of conduct are recommended',
            'Basic documentation of system purpose is good practice'
        ]
    }