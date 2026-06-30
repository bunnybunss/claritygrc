def get_nis2_obligations(sector, org_size):
    
    # SECTORS COVERED BY NIS2
    covered_sectors = ['finance', 'health', 'energy', 'transport', 'digital', 'public']
    
    # CHECK IF APPLICABLE
    if sector not in covered_sectors:
        return {
            'applicable': False,
            'classification': 'NOT APPLICABLE',
            'color': 'green',
            'meaning': 'Your organization does not operate in a sector covered by NIS2. No mandatory obligations apply under this directive.',
            'obligations': [],
            'deadlines': []
        }

    if org_size == 'small':
        return {
            'applicable': False,
            'classification': 'LIKELY EXEMPT',
            'color': 'green',
            'meaning': 'Small organizations (under 50 employees) are generally exempt from NIS2 unless they are identified as critical by a member state.',
            'obligations': [
                'Verify with your national authority whether an exemption applies',
                'Consider voluntary compliance as good practice'
            ],
            'deadlines': []
        }

    # ESSENTIAL vs IMPORTANT ENTITIES
    essential_sectors = ['energy', 'transport', 'finance', 'health', 'digital', 'public']
    
    if sector in essential_sectors and org_size == 'large':
        entity_type = 'ESSENTIAL ENTITY'
        entity_color = 'red'
    else:
        entity_type = 'IMPORTANT ENTITY'
        entity_color = 'orange'

    # SECTOR SPECIFIC OBLIGATIONS
    sector_notes = {
        'finance': 'As a financial sector entity, NIS2 overlaps significantly with DORA. Coordinate compliance efforts across both frameworks.',
        'health': 'Healthcare entities must pay particular attention to incident reporting and supply chain security for medical devices and systems.',
        'energy': 'Energy sector entities must implement enhanced monitoring for operational technology (OT) and industrial control systems.',
        'transport': 'Transport entities must secure both IT and operational systems including traffic management and navigation systems.',
        'digital': 'Digital infrastructure providers face the strictest NIS2 requirements due to their systemic importance.',
        'public': 'Public administration entities must implement NIS2 measures and report to national cybersecurity authorities.'
    }

    return {
        'applicable': True,
        'classification': entity_type,
        'color': entity_color,
        'meaning': f'Your organization qualifies as an {entity_type} under NIS2. This directive became enforceable across EU member states in October 2024 and requires immediate compliance action.',
        'sector_note': sector_notes.get(sector, ''),
        'obligations': [
            'Implement a comprehensive cybersecurity risk management framework',
            'Establish and maintain an incident response plan',
            'Report significant cybersecurity incidents to national authority within 24 hours (early warning) and 72 hours (full report)',
            'Conduct regular cybersecurity risk assessments',
            'Implement supply chain security measures for all critical vendors',
            'Ensure business continuity and crisis management capabilities',
            'Implement multi-factor authentication and encryption across systems',
            'Conduct regular cybersecurity training for all staff',
            'Designate a responsible person or team for NIS2 compliance',
            'Register with your national NIS2 competent authority'
        ],
        'deadlines': [
            'Immediate — appoint NIS2 compliance responsible person',
            'Within 3 months — complete initial risk assessment',
            'Within 6 months — implement core technical measures',
            'Ongoing — 24/72 hour incident reporting obligation'
        ],
        'penalties': 'Essential entities: up to €10 million or 2% of global annual turnover. Important entities: up to €7 million or 1.4% of global annual turnover.'
    }