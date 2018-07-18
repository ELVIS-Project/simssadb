def get_contributions_summaries(contributions):
    summaries = []
    contributions = contributions.iterator()
    for contribution in contributions:
        summaries.append(contribution.summary())
    return summaries


def filter_contributions_by_role(contributions, role):
    filtered_contributions = []
    for contribution in contributions:
        if contribution['role'] == role:
            filtered_contributions.append(contribution)
    return filtered_contributions


def dates_of_contribution(contributions):
    dates = []
    for contribution in contributions:
        dates.append(contribution['date'])
    return dates


def places_of_contribution(contributions):
    places = []
    for contribution in contributions:
        places.append(contribution['location'])
    return places
