from custom_loggers.ColoredFormatter import ColoredFormatter
import logging
from typing import Union
import inspect
from pathlib import Path


class CustomLogRecord(logging.LogRecord):
    """
    Log Records generate the record that is passed into any handlers (ColoredFormatter) for processing
    This class' primary responsibility is set the levelname based on the CustomLogger Logic rather than
    default
    """

    def __init__(self, name, level, *args, **kwargs):
        super().__init__(name, level, *args, **kwargs)
        self.levelname = CustomLogger.get_level_name(level)


logging.setLogRecordFactory(CustomLogRecord)


class CustomLogger(logging.Logger):
    """
    The Magic Comes Together Here:
    CustomLogger inherits from logging.Logger and overrides the minimum number of methods to retain logger functions.

    add_script_location: bool will add the file and line number of the file where log was called
        * In PyCharm if you install the Awesome Console plugin it will make it a hyperlink that will navigate you to
          the code
    logging_disabled: bool enables or disables ALL Logging from CustomLogger
    default_logging_level: int the logging level assigned to each logger by default
    log_level: int the current log level.
    inclusive: bool when calculating whether to log or not if inclusive is True we'll accept the set log level and below
        if false only loglevel matching the exact level will log
    default_colored_formatter:Formatter when creating an instance with add_formatter is True this is the class used to
        create the formatter
    default_colored_format:str the format string that the formatter will use
    default_asctime_format:str the asctime format the formatter will use
    """
    add_script_location: bool = False
    logging_disabled: bool = False
    default_logging_level: int = 0
    global_log_level: int = 0
    use_global_log_level_default: bool = False
    inclusive: bool = True
    default_formatter: logging.Formatter = ColoredFormatter
    default_colored_format: str = '%(asctime)s %(levelname)-8s %(name)s: %(message)s'
    default_asctime_format: str = "%Y-%m-%d %H:%M:%S"

    _levels = dict(
        CRITICAL=50,
        ERROR=40,
        WARNING=30,
        TRACE=25,
        DEBUG=20,
        INFO=10,
        NOTSET=0,
    )
    _channels = dict(
        GENERAL=True
    )
    _level_names = {v: k for k, v in _levels.items()}

    def __init__(self, name: str, level: Union[str, int] = None, add_formatter: bool = True, channel: str = "GENERAL"):
        """
        :param name: the name assign the logger
        :param level: the level set to the logger
        :param add_formatter: when set to True will create a default colored formatter
        :param channel: The channel this lagger is assigned to
            channels can be disabled and re-enabled using channel_disabled(bool)
        """

        super().__init__(name, 0)
        self._channel = channel
        self._disabled = False
        # looks like a duplicate but is not. This will ensure the channel passed into the constructor is added
        # to the channels dictionary
        self.channel = channel
        if level is None:
            self._log_level = CustomLogger.default_logging_level
        else:
            self._log_level = self.check_level(level)
        self.use_global_level: bool = CustomLogger.use_global_log_level_default

        if add_formatter:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.level)

            formatter = CustomLogger.default_formatter(CustomLogger.default_colored_format,
                                                       CustomLogger.default_asctime_format)
            console_handler.setFormatter(formatter)

            self.addHandler(console_handler)

    def trace(self, msg, *args, **kwargs):
        self.log("TRACE", msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.log("DEBUG", msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log("INFO", msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.log("WARNING", msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.log("WARNING", msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log("WARNING", msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log("ERROR", msg, *args, **kwargs)

    @property
    def level(self):
        return self._log_level

    @level.setter
    def level(self, value):
        self.check_level(value)

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, channel: str):
        if channel not in CustomLogger._channels.keys():
            CustomLogger._channels[channel.upper()] = True

        self._channel = channel

    @classmethod
    def channel_disabled(cls, channel: str, disabled: bool):
        cls._channels[channel.upper()] = not disabled

    @property
    def disabled(self):
        """
        a representation of whether this logger is disabled via class, channel, or self settings

        :return:
        """
        return CustomLogger.logging_disabled or not CustomLogger._channels[self._channel.upper()] or self._disabled

    @disabled.setter
    def disabled(self, value: bool):
        self._disabled = value

    @classmethod
    def add_level(cls, level_name: str, level_value: int, dynamic_create_method: bool = False):
        """
        Adds a custom level to CustomLogger class affecting ALL instances of the class
        This can also be used to modify the integer value of a level

        :param level_name: UPPER the level name
        :param level_value: The integer value for this level (remember when in inclusive mode everything <= the set
                loglevel will be logged
        :param dynamic_create_method: When True, will create a method to the Class with the name of the level
            rather than needing to do:
                logger_inst.log("level_name","msg)
            can use:
                logger_inst.level_name("msg")

            The problem with this method is that IDE's like pyCharm will most likely not recognize it as a method.
            To get IDE's to recognize the method it would probably be better to inherit CustomLogger in your own class.

            ex.
            class NewLevelsClass(CustomLogger):
                def __init(self,name:str,level:int,formatter:bool=True,channel:str="CHANNEL"):
                    super().__init__(name,level,formatter,channel)
                    self.add_level("NEWLEVEL",1)

                def newlevel(msg):
                    self.log("NEWLEVEL",msg)

        :return: None
        """

        cls._levels[level_name.upper()] = level_value
        cls._level_names[level_value] = level_name.upper()

        if dynamic_create_method:
            new_method = lambda new_self, msg, *args, **kwargs: new_self.log(level_value, msg, *args, **kwargs)
            exec('cls.{}=new_method'.format(level_name.replace(" ", "_").lower()))

    @classmethod
    def check_level(cls, level: Union[str, int]):
        """
        Ensures the level exists, and if found returns the integer value of the level.

        :param level: either the level_name or level_value
        :return: Returns the integer value of a level
        """
        if isinstance(level, int):
            if level not in list(cls._levels.values()):
                raise ValueError("Level Not Defined")
            return level
        else:
            level = level.upper()
            if level not in cls._levels.keys():
                raise ValueError("Level Not Defined")
            return cls._levels[level]

    @classmethod
    def get_level_name(cls, level: int):
        """
        returns the level name from the integer value

        :param level:
        :return: level_name
        """
        if level not in cls._level_names:
            raise ValueError("Level: {} not found".format(level))
        return cls._level_names[level]

    def setLevel(self, level) -> None:
        self.level = self.check_level(level)
        self.manager._clear_cache()

    def isEnabledFor(self, level: int) -> bool:
        """
        Ensures that the current logger is enabled for the level
        checks if this logger is enabled
        based on inclusiveness will return enabled based on level vs loglevel settings in the class

        :param level:
        :return:
        """
        if self.disabled:
            return False

        comp_level = self.level
        if self.use_global_level:
            comp_level = CustomLogger.global_log_level

        if CustomLogger.inclusive:
            return level <= comp_level or comp_level == 0
        else:
            return level == comp_level or comp_level == 0

    def log(self, level: Union[str, int], msg, *args, **kwargs):
        """
        Primary change is allows for the level_name to be passed in
        the super class always expected the integer value

        :param level: level_name or level_value
        :param msg: message to log
        :param args: arguments passed to super
        :param kwargs: kwargs passed to super
        :return: None
        """
        if isinstance(level, str):
            level = self.check_level(level)

        return super().log(level, msg, *args, **kwargs)

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False, stacklevel=1):
        """
        Used to add the script location to the super implementation, when add_class_from_frame is set to True
        It will add it to the beginning of msg

        :param level:
        :param msg:
        :param args:
        :param exc_info:
        :param extra:
        :param stack_info:
        :param stacklevel:
        :return:
        """

        def get_class_from_frame(fr):
            import inspect
            insp_args, _, _, value_dict = inspect.getargvalues(fr)
            # we check the first parameter for the frame function is
            # named 'self'
            if len(insp_args) and insp_args[0] == 'self':
                # in that case, 'self' will be referenced in value_dict
                instance = value_dict.get('self', None)
                if instance:
                    # return its class
                    return getattr(instance, '__class__', None)
                instance = value_dict.get('cls', None)
                if instance:
                    return instance
            # return None otherwise
            return None

        if self.__class__.add_script_location:
            frame = inspect.currentframe()
            while True:
                class_type = get_class_from_frame(frame)
                if class_type != self.__class__:
                    break
                frame = frame.f_back

            func = frame.f_code
            msg = f"[{Path(func.co_filename).name}, line {str(frame.f_lineno).ljust(4)}] " + msg

        super()._log(level, msg, args, exc_info, extra, stack_info, stacklevel)

