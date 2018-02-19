from matplotlib.figure import Figure

def assertIsFigure(value, variableName):
    assert isinstance(value, Figure), variableName + ' must be an instance of ' + str(Figure)

def assertIsInt(value, variableName):
    assert isinstance(value, int), variableName + ' must be an instance of ' + str(int) 

def assertIsFunction(value, variableName):
    assert callable(value), name + ' must be a callable function'