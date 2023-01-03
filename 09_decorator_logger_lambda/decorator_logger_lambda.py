import re
import os
import logging

file_path = 'D:/data.txt'
output = []

#logger
loggingFile = 'D:/mylog.log'
logging.basicConfig(filename=loggingFile,
                    filemode='w',
                    level=logging.DEBUG,
                    # format='[%(module)s.%(funcName)s.%(lineno)d] %(levelname)s:%(message)s'
                    format='[%(message)s'
                    )

def regular_expr(line):

     comb_expr = re.compile("^[+-]?[0]+[1-9]+\Z|^[+-]?[0]?[1-9][0-9]{0,6}\Z|^0\Z")

     if comb_expr.match(line):
          output.append(line)
          # logging.info(' ' + line + ' - ' + 'passed')
          return True
     else:
          # logging.info(line + ' - ' + 'not passed')
          return False


def read_lines(file_path):
     with open(file_path, 'r') as read_file:
          for index, line in enumerate(read_file):
               o = regular_expr(line.strip())
               if o:
                    logging.info(' line nr ' + str(index + 1) + ' - ' + line.strip() + ' - ' + 'passed')
               else:
                    logging.info(' line nr ' + str(index + 1) + ' - ' + line.strip() + ' - ' + 'not passed')


def result():
     for i in output:
          print(i)

def write_result():

     input_file_name = os.path.basename(file_path) #data.txt
     base_name_to_save = os.path.splitext(input_file_name)[0] #data

     path_to_save = os.path.dirname(file_path)
     name_to_save = base_name_to_save + '_filtered.txt'
     path_to_file = os.path.join(path_to_save, name_to_save)

     logging.info('output file = ' + path_to_file)

     with open(path_to_file, 'w') as outfile:
          for i in output:
               outfile.write(i)
               outfile.write('\n')

###########################################
# decorator
###########################################

def filepath(fpath):
     def wrap(f):
          def wrapper(*args):

               return f(fpath)
          return wrapper
     return wrap

###########################################

@filepath('D:/data2.txt')
def setPath(path='D:/data.txt'):
     global file_path
     file_path = path

def main():
     logging.info('input file = ' + file_path)

     setPath()
     read_lines(file_path)
     result()
     # write_result()

if __name__ == "__main__":
    main()
