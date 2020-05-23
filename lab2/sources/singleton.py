def Singleton(cls):
    '''Makes class acts like Singleton class.
    '''

    class Wrapper:
        __instance = None

        def get_instance(*args, **kwargs):
            if not Wrapper.__instance:
                Wrapper.__instance = cls(*args, **kwargs)
            return Wrapper.__instance

    return Wrapper
