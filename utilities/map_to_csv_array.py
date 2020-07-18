def map_to_csv_array(map_object):
    csv = [','.join(map_object[0].keys())]

    for obj in map_object:
        csv.append(','.join(obj.values()))

    return csv
