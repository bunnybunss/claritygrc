def get_dora_obligations(sector, org_size):

    # DORA ONLY APPLIES TO FINANCIAL SECTOR
    if sector != 'finance':
        return {
            'applicable': False,
            'classification': 'NOT APPLICABLE',
            'color': 'green',
            'meaning': 'DORA (Digital Operational Resilience Act) applies exclusively to financial sector entities. Your organization is not subject to DORA obligations.',
            'obligations': []
        }

    # DETERMINE ENTITY TYPE
    if org_size in ['small', 'medium']:
        entity_type = 'SIMPLIFIED REGIME'
        entity_color = 'yellow'
        meaning = 'As a small or medium financial entity, you fall under DORA\'s simplified regime. Fewer obligations apply but core resilience requirements still must be met.'
        obligations = [
            'Implement a simplified ICT risk management framework',
            'Maintain basic incident reporting capabilities',
            'Conduct annual review of ICT risks',
            'Ensure contractual protections with key ICT vendors',
            'Report major ICT incidents to your national financial regulator'
        ]
    else:
        entity_type = 'FULL REGIME'
        entity_color = 'red'
        meaning = 'Your organization is subject to the full DORA regime which became enforceable on January 17, 2025. Immediate compliance action is required.'
        obligations = [
            'Establish a comprehensive ICT Risk Management Framework approved by the board',
            'Implement ICT-related incident classification and reporting processes',
            'Report major ICT incidents to competent authority within 4 hours of classification',
            'Conduct annual Digital Operational Resilience Testing (DORT)',
            'Perform Threat-Led Penetration Testing (TLPT) every 3 years for significant entities',
            'Implement third-party ICT risk management framework for all critical vendors',
            'Register all ICT third-party service providers in the EU oversight framework',
            'Establish information sharing arrangements with other financial entities',
            'Ensure board-level accountability for ICT risk management',
            'Maintain detailed ICT asset registers and dependency mapping',
            'Implement robust backup and recovery capabilities with tested RTO/RPO targets',
            'Conduct post-incident reviews for all major ICT incidents'
        ]

    return {
        'applicable': True,
        'classification': entity_type,
        'color': entity_color,
        'meaning': meaning,
        'obligations': obligations,
        'key_dates': [
            'January 17, 2025 — DORA became fully enforceable',
            'Ongoing — annual DORT testing required',
            'Every 3 years — TLPT required for significant entities'
        ],
        'regulators': [
            'Netherlands — De Nederlandsche Bank (DNB) and AFM',
            'France — ACPR (Autorité de Contrôle Prudentiel et de Résolution)',
            'EU level — European Supervisory Authorities (EBA, EIOPA, ESMA)'
        ],
        'penalties': 'Up to 1% of average daily global turnover for each day of non-compliance. Individual managers can be held personally liable.',
        'nis2_overlap': 'DORA takes precedence over NIS2 for financial entities. Where both apply, DORA obligations are considered lex specialis and take priority.'
    }