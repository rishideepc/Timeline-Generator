class DataParser:
    def __init__(self):
        pass

    def parse_request(self, request):
        text_keyword = request.form['keyword']
        text_date_time = request.form['timeframe']
        text_location = request.form['location']
        text_features = request.form['features']
        return text_keyword, text_date_time, text_location, text_features

    def parse_db_data(self, items):
        # date_time_ = []
        title = []
        desc = []
        casualty_injured = []
        severity = []
        summary = []

        no_items = 0
        visited = {}
        for item in items:
            group = (item[1][:16], item[3])
            if group in visited:
                if item[0] not in desc[visited[group]]:
                    desc[visited[group]] += "; " + item[0]
                continue
            visited[group] = no_items
            title.append(item[2])
            # date_time_.append(item[1])
            desc.append(item[0])
            casualty_injured.append(item[4])
            severity.append(item[5])
            summary.append(item[6])
            no_items += 1
        return title, desc, casualty_injured, severity, summary, no_items