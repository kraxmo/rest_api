import argparse
from todoserver import app

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--debug', default=False, action='store_true')
parser.add_argument('dbfile')

if __name__ == "__main__":
    args = parser.parse_args()
    print(args.debug, args.dbfile)
    app.debug = args.debug    
    app.init_db('sqlite:///' + args.dbfile)
    app.run()
