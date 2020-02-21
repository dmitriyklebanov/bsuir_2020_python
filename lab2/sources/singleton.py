def Singleton(cls):
    '''Makes class acts like Singleton class.
    '''

    class Wrapper:
        instance = None

        def __init__(self, *args, **kwargs):
            if not Wrapper.instance:
                Wrapper.instance = cls(*args, **kwargs)

        def __getattr__(self, name):
            return getattr(Wrapper.instance, name)

        def __setattr__(self, name, *args, **kwargs):
            return setattr(Wrapper.instance, name, *args, **kwargs)

    return Wrapper
