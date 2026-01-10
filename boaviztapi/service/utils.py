def temporal_granularity_to_ttl(temporalGranularity: str) -> int:
    """
    Convert the temporal granularity string to a time-to-live (TTL) value in seconds.
    """
    temporalGranularity = temporalGranularity.lower()
    if temporalGranularity == '15_minutes':
        return 15 * 60
    elif temporalGranularity == 'hourly':
        return 60 * 60
    elif temporalGranularity == 'daily':
        return 24 * 60 * 60
    elif temporalGranularity == 'monthly':
        return 30 * 24 * 60 * 60
    elif temporalGranularity == 'quarterly':
        return 90 * 24 * 60 * 60
    elif temporalGranularity == 'yearly':
        return 365 * 24 * 60 * 60
    else:
        raise ValueError(f"Invalid temporal granularity: {temporalGranularity}")