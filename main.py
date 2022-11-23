"""
input
  limit to one input, configuration file (.yml file)

  yaml file
    workPath:XXX

feature
  There are two mode running the pipeline: 1) using -u\-e\-n (or --uniprot\--entrez\--ensembl) to specify the
    corresponding ID.
    2) using -c to specify a configuration file which contain all of the needed arguments.
  multiple threads support
    when drawing data from server of the data source, threads number was limited to 3 (one thread for one data source in
      case of offending the official policy).
    if the data source was provided locally, the threads number is unlimited.
  resume support

extensibility
  supplement new data source
  requesting new data from old data source
  revising data requesting method

dependencies
  pandas
  numpy
  PyYaml
  requests
  xmltodict
  uuid

"""
import argparse
import Utils
from Workflow import MainWorkflow


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--Config", help="Specifying the configuration file (.yml file)")
    args = parser.parse_args()
    c = args.Output
    if c:
        mw = MainWorkflow(c)
        mw.run()
    else:
        Utils.consoleLog('Please using "-c" or "--Config" to specify configuration file.')


if __name__ == '__main__':
    main()
