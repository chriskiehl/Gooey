import argparse

from gooey import Gooey


@Gooey
def main():
  parser = argparse.ArgumentParser('Get my users')
  parser.add_argument('-type', "--type", type=str, action='store', dest='type', help= "type Query")
  parser.add_argument('-dst', "--datestart", type=str, action='store', dest='date_start', help= "from Date")
  parser.add_argument('-dsp', "--datestop", type=str, action='store', dest='date_stop', help= "to Date")
  parser.add_argument('-n',"--IDuser", type=str, action='store', dest='idu', help="IDuser")
  parser.add_argument('-t',"--text", type=str, action='store', dest='text', help="find Text")
  parser.add_argument('-f',"--file", type=str, action='store', dest='filepath', help="File Save")
  args = parser.parse_args()
  query_type = args.type
  date_start=args.date_start
  date_stop=args.date_stop
  userid=args.idu
  input_data = args.text
  path_to_file = args.filepath
  print path_to_file

if __name__ == '__main__':
  main()
