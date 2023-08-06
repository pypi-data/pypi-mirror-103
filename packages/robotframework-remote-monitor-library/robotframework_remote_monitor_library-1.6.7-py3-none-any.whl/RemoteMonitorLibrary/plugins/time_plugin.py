__doc__ = """# first time setup CentOS - for Ubuntu/Debian and others see https://www.cyberciti.biz/tips/compiling-linux-kernel-26.html 
curl  https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.11.10.tar.xz -o kernel.tar.xz
unxz kernel.tar.xz
tar xvf kernel.tar
cd linux-5.11.10/
cp -v /boot/config-$(uname -r) .config
sudo dnf -y group install  "Development Tools"
sudo dnf -y install time ncurses-devel hmaccalc zlib-devel binutils-devel elfutils-libelf-devel bison flex openssl-devel make gcc 
make defconfig
/usr/bin/time -f "$(date +'%Y-%m-%dT%H:%M:%S%:z'):\t%e real,\t%U user,\t%S sys,\t%M max_mem_kb,\t%F page_faults,\t%c involuntarily_ctx_swtc,\t%I file_inputs,\t%O file_outputs,\t%r socket_recieved,\t%s socket_sent" -a -o data.txt  make -j 4 clean all
and you'll know something is happening when you start to see real compilation happening... by looking at the data.txt and seeing something like the following 
2021-03-25T18:58:43+02:00:	679.22 real,	1082.81 user,	160.85 sys,	248824 max_mem_kb,	4 page_faults,	120697 involuntarily_ctx_swtc,	98104 file_inputs,	1492752 file_outputs,	0 socket_recieved,	0 socket_sent
#BTW the above was without mlp ... so let's make sure we run at least 10 samples without mlp and 10 samples after - to conclude on avg, max and min for without mlp and then for with mlp """

import os
from typing import Iterable, Any, Tuple

from SSHLibrary import SSHLibrary
from robot.utils import DotDict

from RemoteMonitorLibrary.api import model
from RemoteMonitorLibrary.api.plugins import *
from RemoteMonitorLibrary.api.tools import Logger

__doc__ = """
== Time plugin overview ==
    Wrap linux /usr/bin/time utility for periodical execution and monitor of customer command for process io, memory, cpu, etc

    Full documentation for time utility available on [https://linux.die.net/man/1/time|time man(1)]

    === Plugin parameters ===

    Parameters can be supplied via keyword `Start monitor plugin` as key-value pairs

    Time plugin arguments:

    - command: str -> command to be executed and measured by time (Mandatory)
    
    | Note: Pay attention not to redirect command stderr to stdout (avoid '2>&1'); 
    | Time write to stderr by itself and it send to parser

    - name: User friendly alias for command (Optional)
    - start_in_folder: path to executable binary/script if execution by path not relevant (Optional)
    - store_output: bool -> if true output store to cache in DB
    - sudo: True if sudo required, False if omitted (Optional)
    - sudo_password: True if password required for sudo, False if omitted (Optional)

      On plugin start sudo and sudo_password will be replace with sudo password provided for connection module
    
    Examples:
    |       Flags |  Command executed |
    | <command> | /usr/bin/time -f "..." 'command' > /dev/null |
    | <command> start_in_folder=<folder> | cd <folder> ; /usr/bin/time -f "..." command > /dev/null |
    | <command> start_in_folder=<folder> store_output=yes |  cd <folder> ;/usr/bin/time -f "..." command |
    | <command> start_in_folder=<folder> store_output=yes sudo=yes |  cd <folder> ;sudo /usr/bin/time -f "..." command |
    
"""

from RemoteMonitorLibrary.model.errors import RunnerError

from RemoteMonitorLibrary.utils import get_error_info

DEFAULT_TIME_COMMAND = r'/usr/bin/time'

CMD_TIME_FORMAT = DotDict(
    TimeReal="e",
    TimeKernel="S",
    TimeUser="U",
    TimeCPU="P",
    MemoryMaxResidentSize="M",
    MemoryAverage="t",
    MemoryAverageTotal="K",
    MemoryAverageProcessData="D",
    MemoryAverageProcessStack="p",
    MemoryAverageProcessShared="X",
    MemorySystemPageSize="Z",
    MemoryMajorPageFaults="F",
    MemoryMinorPageFaults="R",
    MemoryProcessSwapped="W",
    MemoryProcessContextSwitched="c",
    MemoryWait="w",
    IOInput="I",
    IOOutput="O",
    IOSocketRecieved="r",
    IOSocketSent="s",
    IOSignals="k",
    Rc="x",
    Command="C"
)


class TimeMeasurement(model.PlugInTable):
    def __init__(self):
        super().__init__('TimeMeasurement')
        self.add_time_reference()
        for f in [model.Field(f, model.FieldType.Int) for f in CMD_TIME_FORMAT.keys() if f != 'Command'] + \
                 [model.Field('Command')]:
            self.add_field(f)
        self.add_output_cache_reference()


class TimeChart(ChartAbstract):
    def __init__(self, table: model.Table, title, *sections):
        self._table = table
        ChartAbstract.__init__(self, *(sections if len(sections) > 0 else self._table.columns))
        self._title = title

    @property
    def sections(self):
        return self._sections

    @property
    def title(self):
        return self._title

    @property
    def file_name(self) -> str:
        return "{name}.png"

    @property
    def get_sql_query(self) -> str:
        return """
        SELECT t.TimeStamp as TimeStamp, {select}, n.Command
        FROM {table_name} n
        JOIN TraceHost h ON n.HOST_REF = h.HOST_ID
        JOIN TimeLine t ON n.TL_REF = t.TL_ID
        WHERE h.HostName = '{{host_name}}'""".format(select=', '.join([f"n.{c} as {c}" for c in self.sections]),
                                                     table_name=self._table.name)

    def y_axes(self, data: [Iterable[Iterable]]) -> Iterable[Any]:
        return [s.replace(self.title, '') for s in self.sections]

    def __str__(self):
        return f"{self.__class__.__name__}: {', '.join(self.sections)}"

    def generate_chart_data(self, query_results: Iterable[Iterable], extension=None) -> \
            Iterable[Tuple[str, Iterable, Iterable, Iterable[Iterable]]]:

        data_series = {}
        for row in query_results:
            if row[-1] not in data_series.keys():
                data_series.update({row[-1]: []})
            data_series[row[-1]].append(row[:-1])
        result = []
        for cmd, row in data_series.items():
            result.append(super().generate_chart_data(row, cmd)[0])
        return result


class TimeParser(Parser):
    def __call__(self, outputs) -> bool:
        command_out = outputs.get('stdout', None)
        time_output = outputs.get('stderr', None)
        rc = outputs.get('rc')
        try:
            assert rc == 0, f"Result return rc {rc}"
            data = time_output.split(',')
            row_dict = DotDict(**{k: v.replace('%', '') for (k, v) in [entry.split(':', 1) for entry in data]})
            for k in row_dict.keys():
                if k == 'Command':
                    continue
                row_dict.update({k: float(row_dict[k])})
            Logger().info(f"Command: {row_dict.get('Command')} [Rc: {row_dict.get('Rc')}]")

            row = self.table.template(self.host_id, None, *tuple(list(row_dict.values()) + [-1]))
            du = model.data_factory(self.table, row, output=command_out)

            self.data_handler(du)
            Logger().debug(f"Item enqueued - {du}")
            return True
        except Exception as e:
            f, li = get_error_info()
            raise RunnerError(f"{self.__class__.__name__} ->  {e}; File: {f}:{li}")


class TimeStartCommand(SSHLibraryCommand):
    def __init__(self, command, **user_options):
        self._time_cmd = user_options.pop('time_cmd', DEFAULT_TIME_COMMAND)
        self._format = ','.join([f"{name}:%{item}" for name, item in CMD_TIME_FORMAT.items()])
        command = f'{self._time_cmd} -f "{self._format}" {command}'
        start_in_folder = user_options.pop('start_in_folder', None)
        if start_in_folder:
            command = f"cd {start_in_folder}; {command}"
        if not user_options.get('return_stdout', False):
            command += ' > /dev/null'
        super().__init__(SSHLibrary.start_command, command,
                         **extract_method_arguments(SSHLibrary.start_command.__name__, **user_options))


class TimeReadOutput(SSHLibraryCommand):
    def __init__(self, **user_options):
        self._format = ','.join([f"{name}:%{item}" for name, item in CMD_TIME_FORMAT.items()])
        user_options.update({'return_stderr': True, 'return_rc': True})
        super().__init__(SSHLibrary.read_command_output, parser=user_options.pop('parser', None),
                         **extract_method_arguments(SSHLibrary.read_command_output.__name__, **user_options))


class Time(PlugInAPI):
    def __init__(self, parameters, data_handler, *args, **options):
        self._command = options.pop('command', None)
        PlugInAPI.__init__(self, parameters, data_handler, *args, **options)
        self._prefix = f"{self.__class__.__name__}_item:"

        self._time_cmd = options.get('time_cmd', DEFAULT_TIME_COMMAND)
        self._command_name = options.get('name', None)

        self._start_in_folder = options.get('start_in_folder', None)
        if self._start_in_folder:
            self._verify_folder_exist(self._start_in_folder)
        assert self._command, "SSHLibraryCommand not provided"
        
        self.set_commands(FlowCommands.Command,
                          TimeStartCommand(self._command, **self.options),
                          TimeReadOutput(parser=TimeParser(host_id=self.host_id,
                                                           table=self.affiliated_tables()[0],
                                                           data_handler=self.data_handler, Command=self.name),
                                         **self.options)
                          )

    def _verify_folder_exist(self, _path):
        with self.inside_host() as ssh:
            if self._start_in_folder.startswith('~'):
                user_home = ssh.execute_command('echo $HOME').strip()
                _path = _path.replace('~', user_home)
            ssh.directory_should_exist(os.path.expanduser(_path))

    @staticmethod
    def affiliated_tables() -> Iterable[model.Table]:
        return TimeMeasurement(),
        # LinesCache(), LinesCacheMap()

    @staticmethod
    def affiliated_charts() -> Iterable[ChartAbstract]:
        base_table = TimeMeasurement()
        return tuple(TimeChart(base_table, name, *[c.name for c in base_table.fields if c.name.startswith(name)])
                     for name in ('Time', 'Memory', 'IO'))

    @property
    def id(self):
        return f"{super().id}: {self._command}"

    def __str__(self):
        return f"{self.type} [on {self.host_alias}] start command '{self._command}'  [name={self.name}]"


__all__ = [
    Time.__name__,
    __doc__
]
