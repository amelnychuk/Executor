from collections import OrderedDict
import itertools



class ExecutorMeta(type):
    """
    This meta class allows class functions to be ordered in the class dict.

    New instances of classes with functions containing _filter attributes
    are appeneded to an array.



    """

    @classmethod
    def __prepare__(metacls, name, bases):
        return OrderedDict()

    def __new__(metacls, name, bases, namespace, **kwds):
        newClass = type.__new__(metacls, name, bases, dict(namespace))
        newClass._fns = []
        if isinstance(bases, tuple):
            if len(bases) > 0:
                if hasattr(bases[0],"_Executor"):
                    for value in namespace.values():
                        if hasattr(value, '_task'):
                            newClass._fns.append(value)

        return newClass

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls._ids = itertools.count(1)


class Executor(list, metaclass=ExecutorMeta):
    """
    This class sequentialy executes functions wrapped by the process function when called.
    Any Executor classes that are returned by child functions are appeneded .



    """
    name = "Executor"
    _Executor = True

    def __init__(self):
        self.id = next(self.__class__._ids)
        print("Count:", self.id)

    def task(func):
        """
        Wrapper fuction for child class functions to use

        :return: wrapped function with _filter attribute set to true
        """

        func._task = True
        return func


    def __call__(self, *args, **kwargs):

        #todo add proper debugging

        for _process in self._fns:

            result = _process(self, *args, **kwargs)

            if hasattr(result, "_Executor"):
                self.append(result)

        #recursive execution

        if len(self) > 0:
            for cls in self:
                cls(*args, **kwargs)


    def __repr__(self):
        return "<{0} Object: {1}{2}>".format(self.__class__.__name__, self.name, list(self)).replace("[","(").replace("]",")")

    def add(self, item):
        self.append(item)

    @classmethod
    def taskall(cls):
        for fn in cls.__dict__.keys():
            if callable(fn):
                fn._filter = True