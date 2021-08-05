from collections import deque
import time
import threading
import curses
import shared_memory

# c++ library binded to python, see srcp/wrappers in this package
from frequency_monitoring_wrp import FrequencyPoint, serialize, deserialize


class FrequencyMonitoring:

    """
    Encapsulate a rotating memory with time stamps.
    The ping method is used to trigger the addition
    of a timestamp to this memory. The share method
    writes a corresponding instance of FrequencyPoint
    (i.e. mean frequency and other values) into
    a shared memory.
    :param str segment_id: segment_id of the shared memory
    :param int size: size of the rotating memory
    """

    def __init__(self, segment_id: str, size: int):

        shared_memory.clear_shared_memory(segment_id)
        self._frequency_point = FrequencyPoint()
        self._segment_id = segment_id
        self._size = size
        self._timestamps = deque([None] * size, size)

    def __del__(self):
        shared_memory.clear_shared_memory(self._segment_id)

    def reset(self):
        """
        Remove all entries from the rotating memory
        """
        self._timestamps = deque([None] * self._size, self._size)
        
    def ping(self):
        """
        Add a time stamp (current time) to the rotating
        memory
        """
        self._timestamps.append(time.time())

    def share(self):
        """
        "Convert" the rotating memory of timestamps into a
        frequency point, that is then written in the shared
        memory
        """
        self._frequency_point.set(list([v for v in self._timestamps if v is not None]))
        serialize(self._segment_id, self._frequency_point)


def read(segment_id: str):
    """
    Reads an instance of FrequencyPoint
    from the shared memory and returns it
    :param str segment_id: segment_id of the
                           shared memory
    """

    fp = FrequencyPoint()
    try:
        deserialize(segment_id, fp)
    except:
        return None
    return fp


class _FrequencyDisplay:

    """
    class for reading instances of FrequencyPoint from the 
    shared memory and displaying the related content to the
    terminal
    """
    
    def __init__(self, segment_id: str):

        self._segment_id = segment_id

        # keeping in memory the lowest frequency
        # ever observed
        self._min = float("+inf")

        # managing curses and exit thread
        self.should_exit = False
        self._screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        self._screen.keypad(1)
        self._monitor_exit_thread = threading.Thread(target=self._monitor_exit)
        self._monitor_exit_thread.setDaemon(True)
        self._monitor_exit_thread.start()

        self._wait_for_segment_id()
        
    def _wait_for_segment_id(self):

        self._screen.clear()
        self._screen.addstr(str("\nwaiting for segment id: {}"
                                ". Press 'q' to exit\n\n").format(self._segment_id))
        self._screen.refresh()
        while not self.should_exit:
            started = shared_memory.wait_for_segment(self._segment_id,500)
            if started:
                return
            
    def _monitor_exit(self):
        # detecting if 'q' was pressed, which set _should_exit
        # to True, which will stop the loop
        while not self.should_exit:
            event = self._screen.getch()
            if event == ord("q"):
                self.should_exit = True

    def exit(self):
        # closing curses
        curses.endwin()

    def refresh(self):

        # read an instance of FrequencyPoint from the
        # shared memory, and write the corresponding
        # data to the console
        
        frequency_point = read(self._segment_id)

        self._screen.clear()
        self._screen.addstr(str("\nmonitoring frequency: {}"
                                 ". Press 'q' to exit\n\n").format(self._segment_id))

        if not frequency_point:
            report = "error: should be started after the main program"

        else:

            self._min = min(frequency_point.min, self._min)
            report = str(
                "mean: {} HZ\n"
                "standard deviation: {}\n"
                "min (this run): {} , min (since beginning): {}\n"
                "max (this run): {}"
            ).format(
                frequency_point.mean,
                frequency_point.sd,
                frequency_point.min,
                self._min,
                frequency_point.max,
            )

        self._screen.addstr(report)
        self._screen.refresh()


def frequency_display(segment_id: str, frequency: float):

    """
    Read a the given frequency from the shared memory
    instances of FrequencyPoint and display the related
    content in a terminal (assumes another process is
    using FrequencyMonitoring.share). 'q' to exit.
    """

    
    
    fd = _FrequencyDisplay(segment_id)

    period = 1.0 / frequency

    while not fd.should_exit:
        fd.refresh()
        time.sleep(period)

    fd.exit()
