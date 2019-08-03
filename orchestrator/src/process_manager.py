import subprocess
import os


class ProcessManager:
    def __init__(self, program_name):
        super().__init__()
        self.__program_name = program_name
        self.__args = []
        self.__env = dict(os.environ)
        self.__process = None
        self.__cwd = None

    def start(self, process_output):
        program_to_run = self.__program_name
        for arg in self.__args:
            if type(arg) is not str:
                arg = str(arg)
            program_to_run = program_to_run + ' ' + arg
        self.__process = subprocess.Popen(program_to_run, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                          cwd=self.__cwd, env=self.__env)

        for line in iter(self.__process.stdout.readline, b''):
            process_output(line.decode('utf-8'))
        self.__process.stdout.close()
        return self

    def with_args(self, *args):
        for arg in args:
            self.__args.append(arg)
        return self

    def with_cwd(self, cwd):
        self.__cwd = cwd
        return self

    def with_env(self, **kwargs):
        for k,v in kwargs.items():
            self.__env[k] = v
        return self

    def wait(self):
        return self.__process.wait()
