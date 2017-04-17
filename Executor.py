from collections import OrderedDict
import itertools
import types



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
    _data = {}
    _classMethods = {}

    def __init__(self):
        self.id = next(self.__class__._ids)
        if issubclass(self.__class__, Executor) and not isinstance(self, Executor):
            print("Is a subclass of Executor")
            #for methodname, classmethod in self.__class__._classMethods.items():
                #setattr(self, methodname, classmethod)
        print(self.id)




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
            #todo modify process
            print("Executing: ", _process)
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
        print("adding:", item)
        print(self._data)
        setattr(item, "_data", self._data)
        for name, classmethod in self.__class__._classMethods.items():
            print(name, classmethod)
            #setattr(item, name, classmethod(classmethod))
            bound = types.MethodType(classmethod, item)
            setattr(item, name, bound)
        self.append(item)

    @classmethod
    def getData(cls):
        return cls._data

    @classmethod
    def getDataName(cls, name):
        return cls._data[name]








class Data(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class ObjectMaker(object):

    #add system variables

    @classmethod
    def makeObject(cls):

        def __init__(self):
            Executor.__init__(self)


        def addData(cls, data):
            """
            This functions adds data to the class so any class derived from this one has access
            through special functions.


            :param data:
            :return:
            """

            # cls.__setattr__(cls, data.name, data.value)

            # self.__class__.__setattr__( data.name, data.value)
            cls._data[data.name] = data.value

            # add functions

            def getFunction(cls):
                print("running function")
                # append key error
                print(cls._data)
                return cls._data[data.name]

            getFunction.__name__ = data.name
            print("setting fn:", str(getFunction))
            cls._classMethods["get" + data.name] = getFunction
            setattr(cls, "get" + data.name, classmethod(getFunction))


        d_init = {'__init__': __init__,
                  'addData': classmethod(addData)}



        newclass = type("Acolyte", (Executor, ), d_init)
        newclass._classMethods = dict()
        newclass._data = dict()
        newclass._operators = []
        return newclass()





E = ObjectMaker.makeObject()

myData = Data("Driver","MyDriverObj")
E.addData(myData)
print(E.getDriver())
print(E)

"""

Disciple = Executor.makeDisciple()()
print(Disciple.__class__)
Disciple.append(5)

myData = Data("Test","poopy")
Disciple.addData(myData)

Disciple2 = Executor.makeDisciple()()

print(Disciple.data is Disciple2.data)
print(Disciple2.data["Test"])
print(Disciple2.__class__.__dict__)
print(Disciple2.getTest())

"""


