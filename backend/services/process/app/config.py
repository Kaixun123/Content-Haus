from dotenv import dotenv_values


class Config:
    """
    A singleton class used to manage the configurations of the application.

    This class loads the environment variables from a .env file and sets them as its attributes.
    The class ensures that only one instance of it exists throughout the application.

    Attributes
    ----------
    _instance : Config
        The single instance of the Config class
    _env : dict
        A dictionary holding the key-value pairs of the environment variables

    Methods
    -------
    __new__(cls, *args, **kwargs)
        Creates a new instance of the class or returns the existing instance
    __init__()
        Loads the environment variables from the .env file into the _env attribute
    __set_attributes()
        Sets each key-value pair in _env as an attribute of the Config object
    __getitem__(key)
        Returns the value of the environment variable with the given key
    """

    _instance = None
    _env = {}

    def __new__(cls, *args, **kwargs):
        """
        Creates a new instance of the class or returns the existing instance.

        Parameters
        ----------
        *args
            Variable length argument list
        **kwargs
            Arbitrary keyword arguments

        Returns
        -------
        Config
            The single instance of the Config class
        """
        if not isinstance(cls._instance, cls):
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """
        Loads the environment variables from the .env file into the _env attribute.

        The environment variables are loaded only if they haven't been loaded before.
        """
        if not self._env:
            self.__set_attributes(dotenv_values('../var.env'))

    def __set_attributes(self, env):
        """
        Sets each key-value pair in _env as an attribute of the Config object.

        The keys are converted to lowercase to match the case of the attribute names.
        """
        for k, v in env.items():
            self._env[k.lower().replace('_', '.')] = v

    def __getitem__(self, key):
        """
        Returns the value of the environment variable with the given key.

        Parameters
        ----------
        key : str
            The key of the environment variable

        Returns
        -------
        str
            The value of the environment variable

        Raises
        ------
        KeyError
            If the key is not found in the environment variables
        """
        if key not in self._env:
            raise KeyError(f"Key {key} not found in environment variables")

        return self._env[key]
