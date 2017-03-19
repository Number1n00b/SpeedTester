class CSVFileWriter:
    """
    Created by Christian on 21/12/2016.

    A general purpose CSV file writer.
    """

    def __init__(self, file):
        """
        Creates a general purpose csv file writer.
        :param file: The open file which to write to.
        """
        self._file = file

        self._delim = ','

    def writeitems(self, *items):
        """
        Write's the given entries in CSV format to the file.
        NOTE: Take care when passing multiple tuples to this method, it will simply write the string representation
        of the tuple which may cause undesirable results.
        :param items: Multiple Strings OR SINGLE tuple. (The items which to write.)
        :return: None.
        """
        # Check here if the argument passed was a single tuple, if it was: write each item in the tuple.
        if len(items) == 1:
            items = items[0]

        for ii in range(0, len(items)):
            self._file.write(str(items[ii]))

            # If not writing the last element, append a comma.
            if not ii == len(items) - 1:
                self._file.write(",")

        self._file.write("\n")

    def writeline(self, line):
        """
        Writes the given line to the file.
        :param line: The string which to write.
        :return: None
        """
        self._file.write(str(line))
        self._file.write("\n")

    # Properties
    @property
    def delim(self):
        return self._delim

    @delim.setter
    def delim(self, delim):
        self._delim = delim