"""
    Module with different helper utilities
"""
import json
import logging
import os
import re
from argparse import ArgumentTypeError
from datetime import datetime, timedelta
from subprocess import CalledProcessError

import pytz
from stringcolor import cs

from videotools.model import ColoredException, COLOR_RED, DictionaryField
from videotools import DEFAULT_TIMEZONE

_logger = logging.getLogger('utils')


# ---------------
#    EXCEPTIONS
# ---------------

class FileNotExistsError(ArgumentTypeError):
    """
    Exception launched when supplied file path does not exists or is not a file
    """

    def __init__(self, filepath):
        super().__init__(cs(f'The path specified [ {filepath} ] is not a file, or does not exist', COLOR_RED))


class WrongFileExtException(ArgumentTypeError):
    """
    Exception launched when supplied file has not expected extension
    """

    def __init__(self, filepath, extension):
        super().__init__('The path specified has not expected extension', filepath=filepath, extension=extension)


class WrongCsvFormatException(ColoredException):
    """
    Exception launched when supplied string is not in csv format
    """

    def __init__(self, txt):
        super().__init__('Wrong csv format. It should be "key1:value1,value2;key2;value2;key3:value..." or '
                         'key1;key2;key3;...',
                         text=txt)


class UnknownStatNameException(ColoredException):
    """
    Exception launched when supplied stat name does not exists in StatsDict
    """

    def __init__(self, name):
        super().__init__('Supplied stat name does not exists', name=name)


# -----------
#    LOGIC
# -----------

class StatMeassure:
    COLUMNS_LENGTH = {'name': 40, 'other': 20}

    PRINT_SEPARATOR = '-' * 100
    PRINT_HEADER = '{:^{width}}'.format(' ' * COLUMNS_LENGTH['name'], width=COLUMNS_LENGTH['name']) + \
                   '{:^{width}}{:^{width}}{:^{width}}'.format('Total', 'Success', 'Failure',
                                                              width=COLUMNS_LENGTH['other'])

    __statkeys__ = ('name', 'total', 'success', 'failure')

    def __init__(self, name, **kwargs):
        self.name = name
        self.total = kwargs.get('total', 0)
        self.success = kwargs.get('success', 0)
        self.failure = kwargs.get('failure', 0)

    @staticmethod
    def _check_stats(stats):
        assert isinstance(stats, dict), 'Stats need to be a dictionary'
        len(set(stats).difference(StatMeassure.__statkeys__)) == 0, cs(f'Supplied dictionary must contain required '
                                                                       f'keys {StatMeassure.__statkeys__}', COLOR_RED)
        return stats

    @staticmethod
    def of(_dict):
        """
        Creates an instance of meassurement from supplied dictionary. Only stats with integer values are valid, stats
        with percent values can not be used
        """
        if isinstance(_dict, str):
            _dict = json.loads(_dict)
        _dict = StatMeassure._check_stats(_dict)
        return StatMeassure(_dict.pop('name'), **_dict)

    def successUp(self):
        self.success += 1

    def failureUp(self):
        self.failure += 1

    def totalUp(self):
        self.total += 1

    def stats(self, **kwargs):
        """
        Return number of total, success and failure as a dictionary
        :param kwargs: Any extra arguments
             json: Return a json dump
         percent: If True, return stats as percentage
         :return: A dictionary with stats or a json string ir param is given
        """
        _rst = self.__dict__
        if kwargs.get('json'):
            _rst = json.dumps(_rst)
        return _rst

    def percent(self, **kwargs):
        """
        Provides a dictionary with given values as percent
        :param kwargs: Any extra arguments
            json: Return a json dump
        :return: A dictionary with stats as percentages, or a json string ir param is given
        """
        _stats = self.stats()
        _rst = {'name': _stats['name'],
                'total': _stats['total'],
                'success': f'{(_stats["success"] / _stats["total"]) * 100:.1f}%',
                'failure': f'{(_stats["failure"] / _stats["total"]) * 100:.1f}%'}
        if kwargs.get('json'):
            _rst = json.dumps(_rst)
        return _rst

    def print(self, **kwargs):
        """
        Prints a formatted output of current stats
        :param kwargs: Any extra arguments
            percent: Print output as percent
        """
        _stats = self.stats()
        if kwargs.get('percent'):
            _stats = self.percent()

        _line = '{:^{width}}'.format(self.name, width=self.COLUMNS_LENGTH['name'])
        _line += '{:^{width}}{:^{width}}{:^{width}}'.format(_stats['total'], _stats['success'], _stats['failure'],
                                                            width=self.COLUMNS_LENGTH['other'])
        print(_line)


class Stats(DictionaryField):
    """
    Class that wraps logic to perform basic calculations of % success events over total actions.
    Name of actions are defined dynamically, so no event or action names (aka: keys) are known
    in advance
    """

    def __init__(self):
        self.__substats__ = dict()

    @staticmethod
    def of(serialized):
        """
        Creates an instance of stats from supplied serialized object, either as a dict, or as a json dump
        :param serialized: A dictionary or a json dump
        """
        if isinstance(serialized, str):
            serialized = json.loads(serialized)

        assert isinstance(serialized, dict), cs('Serialized param must be a dictionary or a json dump')

        _stats = Stats()
        for _name, _st in serialized.items():
            _stats.__substats__[_name] = StatMeassure.of(_st)
        return _stats

    def add(self, meassure):
        """
        Adss a prebuilt meassure to this instance
        """
        assert isinstance(meassure, StatMeassure), cs('Supplied meassure must be an instance of StatMeassure')
        self.__substats__[meassure.name] = meassure
        return meassure

    def successUp(self, name, **kwargs):
        """
        Increases the number of success events
        :param name: Increases success events of given substat name
        :param kwargs: Any extra arguments
         nototal: Skip total increase
        """
        nototal = kwargs.get('nototal', False)

        assert name, cs('Name of stat serie is required', COLOR_RED)

        if name not in self.__substats__.keys():
            self.__substats__[name] = StatMeassure(name)

        self.__substats__[name].successUp()
        if nototal:
            return
        self.__substats__[name].totalUp()

    def failureUp(self, name, **kwargs):
        """
        Increases the number of failure events
        :param name: Increases failure events of given substat name
        :param kwargs: Any extra arguments
         nototal: Skip total increase
        """
        nototal = kwargs.get('nototal', False)

        assert name, cs('Name of stat serie is required', COLOR_RED)

        if name not in self.__substats__.keys():
            self.__substats__[name] = StatMeassure(name)

        self.__substats__[name].failure += 1
        if nototal:
            return
        self.__substats__[name].total += 1

    def totalUp(self, name):
        """
        Increases the total number of events
        :param name: Increases total count of given substat name
        """
        assert name, cs('Name of stat serie is required', COLOR_RED)

        if name not in self.__substats__.keys():
            self.__substats__[name] = StatMeassure(name)
        self.__substats__[name].totalUp()

    def stats(self, name, **kwargs):
        """
        Return number of total, success and failure as a dictionary
        :param name: Provide stats of given substat name
        :param kwargs: Any extra arguments
              json: Return stats as json dump
        """
        assert name, cs('Name of stat serie is required', COLOR_RED)

        # given stat name does not exits. So no input value was given
        if name and name not in self.__substats__.keys():
            raise UnknownStatNameException(name)
        return self.__substats__[name].stats(**kwargs)

    def percent(self, name, **kwargs):
        """
        Return number of total, success and failure as a dictionary expessed in %
        :param name: Provide stats of given substat name
        :param kwargs: Any extra arguments
              json: Return stats as json dump
        """
        # given stat name does not exits. So no input value was given
        if name and name not in self.__substats__.keys():
            raise UnknownStatNameException(name)
        return self.__substats__[name].percent(**kwargs)

    def delete(self, name):
        """
        Delete stats of given name
        :param name: Stats of given name are deleted
        """
        assert name, cs('Name of stat serie is required', COLOR_RED)

        if name and name not in self.__substats__.keys():
            raise UnknownStatNameException(name)

        del self.__substats__[name]

    def print(self):
        """
        Prints a formatted output for included stats
        """
        print(StatMeassure.PRINT_SEPARATOR)
        print(StatMeassure.PRINT_HEADER)
        print(StatMeassure.PRINT_SEPARATOR)

        for _meassure in self.__substats__.values():
            _meassure.print(percent=True)

        print(StatMeassure.PRINT_SEPARATOR)

    # reformat
    def as_dict(self):
        """
        Provides a dictionary with all stats
        :return: All stats as a dictionary
        """
        _dict = {}
        for _name, _st in self.__substats__.items():
            _dict[_name] = _st.stats()
        return _dict

    def as_json(self):
        """
        Return stats as json dump
        """
        return json.dumps(self.as_dict(), indent=4)

    def save(self, **kwargs):
        """
        Saves stats as json
        :param kwargs: Extra args
            filename: Final target final name for stats
        """
        _filename = kwargs.get('filename', f'stats_{DateTimeHelper.short_date()}.json')
        _logger.info('saving stats as %s', _filename)
        with open(_filename, 'w') as _f:
            _f.write(self.as_json())
            _f.flush()



def build_csv_filter(csv_text):
    """
    Builds a filtering dictionary with supplied csv formatted string. WARN: ONLY valid for String filtering!!
    :param csv_text: String to be used as filter. It's a CSV formatted line with key:value pairs to match in
        inventory. If key:value pairs are found, a dictionary is returned. If only key values are provided
        (separated by semicolon too), an array is returned, for example: role:endpoint;site_id:Madrid...
        or ROLE;CITY;HOSTNAME ...
        Multiple values can be provided for filtering as key1:value1,value2;key2:value1,value2...'
    :return: A dictionary with supplied keys and values, or a list with supplied keys
    """
    if not csv_text:
        return ''

    if isinstance(csv_text, list) or isinstance(csv_text, dict):
        _logger.debug('skipping filter creation, a csv formatted string is needed')
        return csv_text

    assert isinstance(csv_text, str), cs('Supplied csv_text must be a csv formatted string', COLOR_RED)

    _logger.debug('building filtering dict from __%s__', csv_text)

    # remove any missing ; from ends of the line
    csv_text = csv_text.lstrip(';').rstrip(';')

    try:
        _logger.debug('\t checking if keyvalue pairs separator is [ ; ]...')

        # -- array filter
        _value = None

        # wrong filter:  'key1;value1,value2'
        if ';' in csv_text and ',' in csv_text and ':' not in csv_text:
            raise WrongCsvFormatException(csv_text)
        if ';' in csv_text and ':' not in csv_text:  # array of keys separated by semicolon 'key1;key2;key3'
            _value = csv_text.split(';')
            _logger.debug('\t returning array of filter keys %s', _value)
        elif ';' not in csv_text and ':' not in csv_text:  # single key   'key1'
            _value = [csv_text.strip()]
            _logger.debug('\t returning single key array %s', )

        # return array of values if given
        if _value:
            return [_v.strip() for _v in _value]

        # -- dictionary filter

        _fdict = {}

        # split values
        # Since it's a dict, all keys must specify a value, or an exception is raised
        for _tup in csv_text.split(';'):
            _logger.debug('\t checking if [ : ] separator exists in each found key:value pairs...')
            _keyvalue = _tup.split(':')
            if len(_keyvalue) == 1 or _keyvalue[1] == '':
                raise
            _logger.debug('\t key and value found, checking if multiple values are given...')
            _key = _keyvalue[0].strip()
            _value = _keyvalue[1].split(',')
            if len(_value) > 1:
                _logger.debug('\t\t multiple values found, adding list %s ...', _value)
                _fdict[_key] = [_v.strip() for _v in _value if _v]
            else:
                _logger.debug('\t\t single value found, adding %s ...', _value[0])
                _fdict[_key] = _value[0].strip()
        return _fdict
    except Exception:
        raise WrongCsvFormatException(csv_text)


def filter_dict(_dict, _csv_filter, **kwargs):
    """
    Filters a dictionary using supplied filter keys
    :param _dict: Dictionay to filter
    :param _csv_filter: CSV formatted string with keys and values, or a dictionary with keys and values
    to filter main dict. CSV format:  'key1:value1;key2;value2...'. If only keys are given the dict is filtered
    to return only those given keys
    :pram kwargs: Any extra arguments
            case: If given, inventory will be filtered using case sensitive matching
    :return:  If a filter by key:value is supplied, the same dictionary is return if supplied values are
    found in dict to be filtered, else, an empty dir is returned. If a list of keys is supplied as filter, then
    a dictionary with only the supplied keys is returned
    """
    assert isinstance(_dict, dict), '_dict must be a dictionary'
    if not _csv_filter:
        _logger.debug('skipping filtering, no filter provided')
        return _dict

    case = kwargs.get('case', False)
    if case:
        _logger.debug('\t case sensitive filtering enabled')

    # if csv formatted string was supplied, build a csv filter
    if isinstance(_csv_filter, str):
        _csv_filter = build_csv_filter(_csv_filter)

    # -- filter by key
    # Remove all entries not included in filter list, and return dictionary
    if isinstance(_csv_filter, list):
        _logger.debug('\t filtering by key names %s', _csv_filter)
        return {key: value for key, value in _dict.items() if key in _csv_filter}

    # -- filter by key:value
    # check if all filter values are found in dict to be filtered
    _logger.debug('\t filtering by key:value pairs in filter %s', _csv_filter)
    for _fkey, _fvalue in _csv_filter.items():
        _fvalue = [i for i in _fvalue if isinstance(_fvalue, list)] or [_fvalue]
        try:
            _dvalue = _dict[_fkey]
        except KeyError:
            _logger.warning('Filter key [ %s ] not found in supplied dict keys %s', _fkey, _dict.keys())
            return None

        found = False
        for _fv in _fvalue:
            if not case:
                _fv = _fv.upper()
                _dvalue = _dvalue.upper()
            # check if dict contains filter value, as soon as there's one match, we exit loop
            if _fv in _dvalue:
                found = True
                break
        if not found:
            _logger.debug('\t filter value [ %s:%s ] not found in dict value [ %s ]', _fkey, _fv, _dvalue)
            return None
    _logger.debug('\t\t filter values found')
    return _dict


def check_file(filepath, **kwargs):
    """
    Checks if a file location specified in parser's arguments exist or not
    :param filepath: The location of the file specified as argument
    :param kwargs: Extra arguments
        extensions: List of extensions that the file should have. If any matches, an exception is thrown
    :return: The file if exists or a parser error
    """
    assert filepath, cs('No path supplied', COLOR_RED)
    if not isinstance(filepath, str):
        raise FileNotExistsError(filepath)

    extensions = kwargs.get('extensions', [])

    _logger.debug('checking if [ %s ] path exists...', filepath)
    filepath = os.path.expanduser(filepath)
    if not os.path.isfile(filepath):
        raise FileNotExistsError(filepath)

    if extensions:
        file_ext = os.path.splitext(filepath)[1].lstrip('.')
        if file_ext not in extensions:
            raise WrongFileExtException(filepath, file_ext)

    _logger.debug('[ %s ] found. Ok', filepath)
    return filepath


def natural_order_key(text):
    """
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    """
    int_text = lambda text: int(text) if text.isdigit() else text

    return [int_text(c) for c in re.split('(\d+)', text)]


def check_output(sentence):
    """
    This is a convenience method to execute any sentence and check if an error occurred, and get output
    from sentence command
    :param sentence: whatever needs to be executed
    :return: The output from command. A CalledProcessError is thrown if an error occurs
    """
    try:
        output = check_output(sentence, shell=True)
    except CalledProcessError as ex:
        raise Exception('\t\t check_call ERROR executing [%s], return code:= [%s]' % (sentence, ex.returncode))
    return output


class DateTimeHelper:
    """
    Helper class to be use with date and time manipulations
    """
    _LOGGER = logging.getLogger('DateTimeHelper')

    ISO_FORMAT_DATE = '%Y-%m-%d'
    ISO_FORMAT_TIME = '%H:%M'

    @staticmethod
    def is_short_format(short_date_as_string):
        """
        Verifies if supplied date matches short date regex
        :param short_date_as_string: The string to verify in short format yyyy-mm-dd
        :return: True if matches format, False otherwise
        """
        try:
            datetime.strptime(short_date_as_string, DateTimeHelper.ISO_FORMAT_DATE)
            return True
        except (TypeError, ValueError, Exception):
            return False

    @staticmethod
    def yesterday(as_string=True):
        """
        Provides yesterday date
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: Yesterday date as s string or a datetime object
        """
        return DateTimeHelper.days_ago(1, as_string)

    @staticmethod
    def sixty_days_ago(as_string=True):
        """
        Provides the date of sixty days ago
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: Two months ago date as string or a datetime object
        """
        return DateTimeHelper.days_ago(60, as_string)

    @staticmethod
    def thirty_days_ago(as_string=True):
        """
        Provides the date of a thirty days ago
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: A month ago date as string or a datetime object
        """
        return DateTimeHelper.days_ago(30, as_string)

    @staticmethod
    def two_weeks_ago(as_string=True):
        """
        Provides the date of a week ago
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: Two weeks ago date as string or a datetime object
        """
        return DateTimeHelper.days_ago(14, as_string)

    @staticmethod
    def a_week_ago(as_string=True):
        """
        Provides the date of a week ago
        :param as_string: If true, provide the date as a string in short format yyyy-mm-dd. Return the datetime object
                          otherwise
        :return: A week ago date as string or a datetime object
        """
        return DateTimeHelper.days_ago(7, as_string)

    @staticmethod
    def days_ago(number_of_days, as_string=True):
        """
        Provides the date value of number of days in short format yyyy-mm-dd
        :param number_of_days: Number of days ago from current date
        :param as_string: If true, provide the date as a string. Return the datetime object otherwise
        :return: Yesterday date as yyyy-mm-dd
        """
        days_ago = datetime.now() - timedelta(days=number_of_days)
        if as_string:
            return DateTimeHelper.datetime_to_iso8601(days_ago, DateTimeHelper.ISO_FORMAT_DATE)
        else:
            return days_ago

    @staticmethod
    def days_between(date1, date2):
        """
        Provides the number of dates between supplied two dates. If supplied dates are a string, they are
        converted to a datetime object, and the format must be as yyyy-mm-dd
        :param date1: A date as a string or a datetime
        :param date2: A date as a string or a datetime
        :return: The difference in days between supplied dates as an integer. An exception is thrown
                 if a problem occurs
        """
        if isinstance(date1, str):
            date1 = datetime.strptime(date1, DateTimeHelper.ISO_FORMAT_DATE)
        if isinstance(date2, str):
            date2 = datetime.strptime(date2, DateTimeHelper.ISO_FORMAT_DATE)
        return abs((date2 - date1).days)

    @staticmethod
    def short_date(_datetime=datetime.now()):
        """
        Provides current date in short format yyyy-mm-dd
        :return: The date as  yyyy-mm-dd
        """
        return DateTimeHelper.datetime_to_iso8601(_datetime, DateTimeHelper.ISO_FORMAT_DATE)

    @staticmethod
    def short_time():
        """
        Provides current date in short format hh:mm
        :return: The date as hh:mm
        """
        return DateTimeHelper.datetime_to_iso8601(datetime.now(), DateTimeHelper.ISO_FORMAT_TIME)

    @staticmethod
    def iso8601_to_datetime(time_as_iso8601, iso_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        Given a date as a  ISO8601 string, i.e:  yyyy-MM-dd'T'HH:mm:ss.SSSZ, provides a datetime object.
        The string object is split at the <+> symbol.
        :param time_as_iso8601: String with a time representation in ISO8601 format as yyyy-MM-ddTHH:mm:ss.SSSZ
        :return: A datetime object with supplied date as string
        """
        # If string has the + symbol, split it:
        if '+' in time_as_iso8601:
            time_as_iso8601 = time_as_iso8601.split('+')[0]

        try:
            return datetime.strptime(time_as_iso8601, iso_format)
        except Exception as ex:
            raise Exception(f'\t\t Exception parsing strinng date in ISO8601 format {time_as_iso8601}')

    @staticmethod
    def datetime_to_iso8601(time_as_datetime, iso_format='%Y-%m-%d %H:%M:%S.%f'):
        """
        Given a datetime object provide a  ISO8601 string representation
        :param time_as_datetime: A datetime object
        :return: A string with ISO8601 representation of the supplied datetime object
        """

        try:
            return time_as_datetime.strftime(iso_format)
        except Exception:
            raise Exception('\t\t Exception converting datetime to ISO8601 format')

    @staticmethod
    def iso8601_to_anyformat(time_as_iso8601, format='%d-%m-%Y'):
        """
         Given a date as a  ISO8601 string, i.e:  yyyy-MM-dd'T'HH:mm:ss.SSSZ, provides a string with another format
         :param time_as_iso8601: String with a time representation in ISO8601 format as yyyy-MM-ddTHH:mm:ss.SSSZ
         :return: A string with date as dd-MM-yyyy
         """
        try:
            date_as_str = DateTimeHelper.iso8601_to_datetime(time_as_iso8601)
            date_as_str = DateTimeHelper.datetime_to_iso8601(date_as_str, iso_format=format)
        except Exception:
            date_as_str = 'Wrong Format'
        return date_as_str

    @staticmethod
    def compare_iso8601_dates(date1_as_iso8601, date2_as_iso8601):
        """
        Method that compares two dates, if the first one is bigger, the result is positive, if the second one is bigger
        the result is negative, if they are equal, a 0 is returned
        :param date1_as_iso8601: A string date representation as ISO8601
        :param date2_as_iso8601: A string date representation as ISO8601
        :return: An integer. Positive if date1>date2, negative if date2>date1 or 0 otherwise
        """
        try:
            date1 = DateTimeHelper.iso8601_to_datetime(date1_as_iso8601)
            date2 = DateTimeHelper.iso8601_to_datetime(date2_as_iso8601)

            if date1 > date2:
                return 1
            elif date2 > date1:
                return -1
            else:
                return 0
        except Exception as es:
            raise Exception(f'\t\t exception comparing iso8601 dates {date1_as_iso8601}{date2_as_iso8601}')

    @staticmethod
    def string_date_to_datetime(date_as_string, iso_format='%Y-%m-%d'):
        """
        Converts supplied date, to datetime object. Default format : %Y-%m-%d
        :param date_as_string: The date as a string, with format yyyy-mm-dds
        :return: A datetime object
        """
        try:
            return datetime.strptime(date_as_string, iso_format)
        except Exception as ex:
            DateTimeHelper._LOGGER.error(f'could not convert from date to datetime [{date_as_string}] using format '
                                         f'[{iso_format}]')
            raise ex

    @staticmethod
    def datetime_to_epoch(datetime_object):
        """
        Converts supplied datetime to epoch in milliseconds
        :param datetime_object: A datetime object
        :return: The number of milliseconds since epoch
        """
        epoch = int((datetime_object - datetime(1970, 1, 1)).total_seconds() * 1000)
        return f'{epoch}'

    @staticmethod
    def date_from_timezone(timezone=DEFAULT_TIMEZONE, iso_format=None, date=None):
        """
        Provides date as a string in a given timezone, using supplied format
        :param timezone:  A valid timezone
        :param iso_format: The format to use to express the datetime object
        :param date: The date to express in the former timezone
        :return: The date as a string
        """
        if date:
            date = pytz.timezone(timezone).localize(date)
        else:
            date = datetime.now(tz=pytz.timezone(timezone))
        if iso_format:
            date = date.strftime(iso_format)
        return date

    @staticmethod
    def to_hours_min_seconds(seconds):
        """
        Converts given seconds to hour, minutes and seconds
        :param seconds: The total number of seconds
        :return:  A tuple as (hour, min, sec)
        """
        min, sec = divmod(seconds, 60)
        hour, min = divmod(min, 60)
        return (hour, min, sec)
