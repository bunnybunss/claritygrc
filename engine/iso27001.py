def get_iso_controls(data_types, eu_classification, automated_decisions, has_security_policy):
    controls = []

    # ALWAYS RECOMMENDED — baseline for every system
    controls.append({
        'id': 'A.5',
        'name': 'Information Security Policies',
        'description': 'Establish and maintain documented information security policies approved by management.',
        'priority': 'High'
    })
    controls.append({
        'id': 'A.8',
        'name': 'Asset Management',
        'description': 'Identify and classify all information assets including data, software, and hardware.',
        'priority': 'High'
    })
    controls.append({
        'id': 'A.9',
        'name': 'Access Control',
        'description': 'Restrict access to information and systems based on business and security requirements.',
        'priority': 'High'
    })

    # PERSONAL OR SENSITIVE DATA
    if any(d in data_types for d in ['personal', 'biometric', 'health', 'financial', 'children']):
        controls.append({
            'id': 'A.18',
            'name': 'Compliance',
            'description': 'Ensure compliance with legal, statutory, regulatory and contractual requirements including data protection laws.',
            'priority': 'High'
        })
        controls.append({
            'id': 'A.10',
            'name': 'Cryptography',
            'description': 'Implement encryption to protect sensitive personal and financial data at rest and in transit.',
            'priority': 'High'
        })

    # HIGH RISK OR UNACCEPTABLE CLASSIFICATION
    if eu_classification in ['HIGH RISK', 'UNACCEPTABLE RISK']:
        controls.append({
            'id': 'A.12',
            'name': 'Operations Security',
            'description': 'Ensure correct and secure operations of AI systems including change management and capacity planning.',
            'priority': 'Critical'
        })
        controls.append({
            'id': 'A.14',
            'name': 'System Acquisition and Development',
            'description': 'Ensure security is built into AI systems from design through deployment — security by design.',
            'priority': 'Critical'
        })
        controls.append({
            'id': 'A.16',
            'name': 'Incident Management',
            'description': 'Establish processes to detect, report, and respond to AI system failures and security incidents.',
            'priority': 'Critical'
        })

    # AUTOMATED DECISIONS
    if automated_decisions == 'yes':
        controls.append({
            'id': 'A.14.2',
            'name': 'Security in Development',
            'description': 'Implement secure development practices for automated decision-making systems including testing and validation.',
            'priority': 'High'
        })
        controls.append({
            'id': 'A.17',
            'name': 'Business Continuity',
            'description': 'Ensure automated decision-making systems remain available and recoverable in case of failure.',
            'priority': 'Medium'
        })

    # NO SECURITY POLICY EXISTS
    if has_security_policy == 'no':
        controls.append({
            'id': 'A.5.1',
            'name': 'Policies for Information Security',
            'description': 'Create and implement a formal information security policy as an immediate priority.',
            'priority': 'Critical'
        })

    # ALWAYS ADD SUPPLIER SECURITY
    controls.append({
        'id': 'A.15',
        'name': 'Supplier Relationships',
        'description': 'Manage security risks in supplier and third-party relationships including AI vendors and data processors.',
        'priority': 'Medium'
    })

    # REMOVE DUPLICATES
    seen = set()
    unique_controls = []
    for c in controls:
        if c['id'] not in seen:
            seen.add(c['id'])
            unique_controls.append(c)

    # SORT BY PRIORITY
    priority_order = {'Critical': 0, 'High': 1, 'Medium': 2}
    unique_controls.sort(key=lambda x: priority_order.get(x['priority'], 3))

    return unique_controls