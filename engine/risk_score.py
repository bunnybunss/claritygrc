def calculate_risk_score(data_types, decision_impact, automated_decisions, human_override, user_types, has_security_policy, has_dpo, previous_assessment):
    score = 0
    breakdown = []

    # DATA SENSITIVITY
    if 'personal' in data_types:
        score += 10
        breakdown.append('+10 — processes personal data')

    if any(d in data_types for d in ['biometric', 'health']):
        score += 20
        breakdown.append('+20 — processes sensitive data (biometric or health)')

    if 'financial' in data_types:
        score += 15
        breakdown.append('+15 — processes financial data')

    if 'children' in data_types:
        score += 25
        breakdown.append('+25 — processes children\'s data')

    if 'location' in data_types:
        score += 10
        breakdown.append('+10 — processes location data')

    if 'behavioral' in data_types:
        score += 10
        breakdown.append('+10 — processes behavioral data')

    # DECISION IMPACT
    impact_scores = {
        'low': 5,
        'moderate': 15,
        'serious': 25,
        'critical': 35
    }
    if decision_impact in impact_scores:
        points = impact_scores[decision_impact]
        score += points
        breakdown.append(f'+{points} — decision impact is {decision_impact}')

    # AUTOMATED DECISIONS
    if automated_decisions == 'yes':
        score += 15
        breakdown.append('+15 — system makes automated decisions')

        if human_override == 'no':
            score += 10
            breakdown.append('+10 — no human override available')

    # VULNERABLE USERS
    if any(u in user_types for u in ['vulnerable', 'children']):
        score += 15
        breakdown.append('+15 — system affects vulnerable users or children')

    # EXISTING CONTROLS — reduce score
    if has_security_policy == 'yes':
        score -= 10
        breakdown.append('-10 — existing security policy in place')

    if has_dpo == 'yes':
        score -= 10
        breakdown.append('-10 — Data Protection Officer appointed')

    if previous_assessment == 'yes':
        score -= 10
        breakdown.append('-10 — previous risk assessment completed')

    # CAP score between 0 and 100
    score = max(0, min(score, 100))

    # DETERMINE LEVEL
    if score <= 30:
        level = 'LOW'
        color = 'green'
        advice = 'Your system presents low risk. Maintain good practices and review annually.'
    elif score <= 55:
        level = 'MEDIUM'
        color = 'yellow'
        advice = 'Your system presents medium risk. Address identified gaps and implement recommended controls within 6 months.'
    elif score <= 75:
        level = 'HIGH'
        color = 'orange'
        advice = 'Your system presents high risk. Immediate action is required. Prioritize implementing controls and conduct a full DPIA.'
    else:
        level = 'CRITICAL'
        color = 'red'
        advice = 'Your system presents critical risk. Do not deploy until all controls are implemented and a full compliance review is completed.'

    return {
        'score': score,
        'level': level,
        'color': color,
        'advice': advice,
        'breakdown': breakdown
    }