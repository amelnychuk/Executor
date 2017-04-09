from Executor import Executor


class FirstClass(Executor):

    @Executor.task
    def fn_B(self):
        print("In Function B")

    @Executor.task
    def fn_A(self):
        print("In Function A")


    def fn_C(self):
        print("In Function C")

class SecondClass(Executor):

    @Executor.task
    def fn_A(self):
        print("Second class function A")
        return ThirdClass()

class ThirdClass(Executor):

    @Executor.task
    def fn_B(self):
        print("In Third Class Function B")

    @Executor.task
    def fn_A(self):
        print("In Third Class Function A")


    def fn_C(self):
        print("In Thrid Class Function C")



def main():

    Process = Executor()
    Process.add(FirstClass())

    SecondProcess = Executor()
    SecondProcess.add(SecondClass())

    Process.add(SecondProcess)

    Process()

main()

