def csv_to_map(csv_file):
    f = list(csv_file)
    props = f[0].split(',')
    people = []

    for line in f:
        if not line is f[0]:
            person = {}
            person_opts = line.split(',')
            for i in range(len(person_opts)):
                person[props[i].strip('\n')] = person_opts[i].strip('\n')

            people.append(person)

    return people
