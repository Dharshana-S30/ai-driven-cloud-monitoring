def analyze_traffic(rate):

    if rate > 1000:
        return "Abnormal traffic spike detected."

    return "Traffic normal."