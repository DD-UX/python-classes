def print_matrix(m):
  text = ""
  for x in m:
    for y in x:
      text += " {:2}".format(y)
    text += "\n"

  print(text)