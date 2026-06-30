def get_iso42001_controls(system_type, eu_classification, automated_decisions):

    controls = []

    # ALWAYS RECOMMENDED — baseline for every AI system
    controls.append({
        'id': '4.1',
        'name': 'Understanding the Organization and its Context',
        'description': 'Identify internal and external factors that affect the organization\'s ability to manage AI responsibly.',
        'priority': 'High'
    })
    controls.append({
        'id': '5.1',
        'name': 'Leadership and AI Policy',
        'description': 'Top management must demonstrate commitment to responsible AI and establish a formal AI policy.',
        'priority': 'High'
    })
    controls.append({
        'id': '6.1',
        'name': 'AI Risk Assessment',
        'description': 'Establish a process to identify, analyze, and evaluate AI-specific risks before and during deployment.',
        'priority': 'High'
    })
    controls.append({
        'id': '8.2',
        'name': 'AI System Impact Assessment',
        'description': 'Conduct an impact assessment covering potential harms to individuals, groups, and society from AI system outputs.',
        'priority': 'High'
    })
    controls.append({
        'id': '9.1',
        'name': 'Monitoring and Measurement',
        'description': 'Monitor AI system performance, behavior, and outcomes continuously against defined criteria.',
        'priority': 'High'
    })

    # HIGH RISK OR UNACCEPTABLE CLASSIFICATION
    if eu_classification in ['HIGH RISK', 'UNACCEPTABLE RISK']:
        controls.append({
            'id': '6.2',
            'name': 'AI Objectives and Planning',
            'description': 'Establish measurable AI objectives aligned with responsible AI principles and regulatory requirements.',
            'priority': 'Critical'
        })
        controls.append({
            'id': '8.3',
            'name': 'AI System Design and Development Controls',
            'description': 'Implement controls throughout the AI system lifecycle — from data collection through training, testing, and deployment.',
            'priority': 'Critical'
        })
        controls.append({
            'id': '8.4',
            'name': 'Data Governance for AI',
            'description': 'Establish data governance processes ensuring training data is relevant, representative, and free from harmful bias.',
            'priority': 'Critical'
        })
        controls.append({
            'id': '8.6',
            'name': 'Human Oversight of AI Systems',
            'description': 'Define and implement human oversight mechanisms appropriate to the risk level of the AI system.',
            'priority': 'Critical'
        })

    # AUTOMATED DECISIONS
    if automated_decisions == 'yes':
        controls.append({
            'id': '8.5',
            'name': 'Transparency and Explainability',
            'description': 'Ensure AI system decisions can be explained in understandable terms to affected individuals and regulators.',
            'priority': 'Critical'
        })
        controls.append({
            'id': '8.7',
            'name': 'Accountability Framework',
            'description': 'Assign clear accountability for AI system decisions and establish escalation paths for contested outcomes.',
            'priority': 'High'
        })

    # HIRING, CREDIT, MEDICAL — human impact systems
    high_impact_systems = ['hiring', 'credit_scoring', 'medical', 'law_enforcement']
    if system_type in high_impact_systems:
        controls.append({
            'id': '8.8',
            'name': 'Bias and Fairness Assessment',
            'description': 'Regularly assess the AI system for bias across protected characteristics and document mitigation measures.',
            'priority': 'Critical'
        })
        controls.append({
            'id': '8.9',
            'name': 'Affected Parties Communication',
            'description': 'Establish processes to inform affected individuals about AI system use and provide meaningful recourse.',
            'priority': 'High'
        })

    # ALWAYS ADD THESE
    controls.append({
        'id': '10.1',
        'name': 'Continual Improvement',
        'description': 'Establish processes to continuously improve the AI management system based on monitoring results and incidents.',
        'priority': 'Medium'
    })
    controls.append({
        'id': '7.3',
        'name': 'AI Awareness and Training',
        'description': 'Ensure all staff involved in AI development, deployment, or oversight receive appropriate AI ethics training.',
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

    return {
        'controls': unique_controls,
        'meaning': 'ISO 42001 is the international standard for AI Management Systems (AIMS). Published in 2023, it provides a framework for responsible development and use of AI systems.',
        'certification_note': 'Organizations can pursue ISO 42001 certification to demonstrate responsible AI governance to regulators, clients, and stakeholders.',
        'eu_ai_act_alignment': 'ISO 42001 implementation significantly supports EU AI Act compliance, particularly for high-risk AI systems requiring technical documentation and governance frameworks.'
    }