def moving_average_forecast(values, period, years_count):
    data = values.copy()
    forecast = []

    for _ in range(years_count):
        value = sum(data[-period:]) / period
        forecast.append(round(value, 2))
        data.append(value)

    return forecast

def max_percent_change(values):
    max_change = 0
    year_index = 0

    for i in range(1, len(values)):
        change = abs(
            (values[i] - values[i - 1])
            / values[i - 1] * 100
        )

        if change > max_change:
            max_change = change
            year_index = i

    return year_index, max_change
