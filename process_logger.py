import json

class Logger:

    def __init__(self, dirpath: str):
        self.log_path = f'{dirpath}/processed.json'
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as log:
                self.__log = json.load( log )

        except FileNotFoundError:
            self.__init_log()
            self.__log = dict()

    def __init_log(self):
        with open(self.log_path, 'w', encoding='utf-8') as log:
            log.write('{}')

    def is_processed(self, album: str, file: str):
        return (album in self.__log) and (file in self.__log[album])

    def log_processed(self, album: str, file: str):

        if album in self.__log:
            if file not in self.__log[album]:
                self.__log[album] .append(file)
            else:
                print('Warning: duplicate')

        else:
            self.__log[album] = [file]

    def save(self):
        with open(self.log_path, 'w', encoding='utf-8') as log:
            json.dump( self.__log, log, indent=4 )
