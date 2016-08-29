input_list = ['all', 'this', 'happened', 'more', 'or', 'less']

def find_bigrams(input_list):
  return zip(input_list, input_list[1:])

