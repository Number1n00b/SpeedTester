from errors.file_errors import InvalidFileFormatError
from errors.calling_errors import InvalidArgumentError


class CSVFileReader(object):
    """
    Created by Christian on 21/12/2016.

    A general purpose CSV file reader.

    Features:
    - Custom Delimiter
    - Handle Quoted Strings
    - Read Line by Line or entire file
    """

    def __init__(self, file_name):
        """
        Creates a CSV file reader.
        :param file_name: The name of the file to read.
        """
        self._file = open(file_name, 'r')

        # Assign default delimiter
        self._delim = ','

        # Set the line number to 0.
        self._linenum = 0

    def readline(self):
        """
        Reads the next line of the file.
        :return: A list containing each item in the row.
        """
        # Read the next line.
        read_string = self._file.readline()
        self._linenum += 1

        # Parse the line and put it in a list.
        parts = self._parseline(read_string)

        # Return the parts
        return parts

    def readfile(self):
        """
        Read the entire file.
        :return: A list containing a list for each row in the file.
        """
        # The entire contents of the file.
        contents = []

        # Read until the end of the file.
        while not self.eof:
            line = self.readline()
            contents.append(line)

        return contents

    @staticmethod
    def _parseline(string):
        """
        Parses the given line, splitting it on the delimeter. (Removes quotes and escapes characters within them).
        :param string: The string which to parse.
        :return: A list of the parts contained in the string.
        """
        parts = []

        # Keeps track if the current section is within a quote.
        in_quote = False

        # The indices on which to split the string (Where commas are enclose a substring).
        cur_index = 0
        start_index = 0
        end_index = 0

        for char in string:
            end_of_line = False

            # Detect whether current section is quoted or not.
            if char == '"':
                in_quote = not in_quote

            # If we are at the end of the line, treat it as a delimeter.
            # (Note: This is only necessary when at the last line of the file.)
            if cur_index == len(string) - 1:
                end_of_line = True
                end_index += 1

            if ((not in_quote) and (char == ',' or char == "\n")) or end_of_line:
                # Here we found a valid place to split, so place the sub-string in parts.
                part = string[start_index:end_index]

                # Remove any remaining quotation marks.
                part = part.replace("\"", "")

                # Remove trailing newline characters.
                part = part.replace("\n", "")

                # Add the part to the list
                parts.append(part)

                # Reset starting index.
                start_index = end_index + 1

            end_index += 1
            cur_index += 1

        return parts

    # Properties
    @property
    def delim(self):
        return self._delim

    @delim.setter
    def delim(self, delim):
        self._delim = delim

    @property
    def eof(self):
        """
        Checks to see if the reader has come to the end of the file.
        :return: eof
        """
        eof = False

        # Attempt to read the next line, catching the error if required.
        try:
            line = self._file.readline()
            length = len(line)

            # If the length was 0, the end of file was reached.
            if length == 0:
                eof = True
            else:
                # Return to the line's starting position.
                self._file.seek(self._file.tell() - (length+1))

                # Eww look... it's a hack...
                """
                Okay so for some reason at the end of the file, on the last line, seeking will cause the pointer
                to move back one character too far, causing the next line read to be just the final "\n" character
                from the previous line.

                If I change the seek so that it seeks to (length) instead of (length+1) as above, it causes the first
                letter of each line to be missed, since it isn't seeking back far enough.

                In conclusion:
                The only way I could see to fix the problem was to check the next line and make sure that it isn't
                just a newline character, and if it is, just read it and continue without seeking back.
                TODO - Find a better way to seek through the file and check for EOF.
                """

                line = self._file.readline()

                if line == "\n":
                    return False

                self._file.seek(self._file.tell() - (length+1))

        except EOFError:
            eof = True

        return eof


class CSVHeaderReader(CSVFileReader):
    """
    Created by Christian on 21/12/2016.

    A CSVFileReader that validates each row's length based on the header of the file. It also has extra
    functionality (see below).

    Features:
        - Custom Delimiter
        - Handle Quoted Strings
        - Read Line by Line or entire file

    Added Features:
        - Automatic header checking. (Ensures each row has the right number of columns)
        - Ability to read only specific columns.
    """
    def __init__(self, file_name):
        """
        Standard constructor.
        :param file_name: The name of the file to read.
        """
        super(CSVHeaderReader, self).__init__(file_name)

        # Read the first line of the file and save it as the header line for later comparison.
        header_line = self._file.readline()
        self._header = self._parseline(header_line)

        # Save the un-parsed header for if the calling module needs it.
        self.header = header_line.replace("\n", "")

    def readline(self, column_names_to_read):
        """
        Reads the next line of the file, returning the values required.
        :param column_names_to_read: The names of the column which to read. (Default = all columns)
        :return: The values of the columns selected, in the order selected.
        """
        # Check that the given columns are valid, if specified.
        if column_names_to_read:
            self._validate_columns(column_names_to_read)

        # Get the parts contained in the next line.
        parts = super(CSVHeaderReader, self).readline()

        # If the file does not contain a value for each column, the format is invalid.
        if len(parts) != len(self._header):
            raise InvalidFileFormatError("The file contained an invalid number of columns at line: "
                                         + str(self._linenum)
                                         + ". Expected: " + str(len(self._header))
                                         + ", got: " + str(len(parts)) + ".")

        # If specific columns are specified, select only them.
        if column_names_to_read:
            new_parts = self._select_columns(column_names_to_read, parts)

            parts = new_parts

        # Return the required parts
        return parts

    def readfile(self, column_names_to_read):
        """
        Read the entire file, returning only the columns selected.
        :param column_names_to_read: Any amount of names of columns to return. (Can contain duplicates).
        :return: A list containing a list for each row in the file.
        """
        # Ensure the columns are in contained in the header.
        self._validate_columns(column_names_to_read)

        # The entire contents of the file.
        contents = []

        # Read until the end of the file.
        while not self.eof:
            line = self.readline(column_names_to_read)
            contents.append(line)

        return contents

    def _select_columns(self, columns, line):
        """
        Selects only the given columns from the line.
        :param columns: The names of the header columns to select.
        :param line: The line which to select columns from.
        :return: A tuple containing only the selected columns.
        """
        new_line = []

        for column in columns:
            # Get the origional index of the column
            index = self._header.index(column)

            # Append that column from parts to new_parts
            new_line.append(line[index])

        return new_line

    def _validate_columns(self, column_names_to_read):
        """
        Ensures that the given columns are contained in the header of the file.
        :param column_names_to_read: The columns selected
        :return: None. Fails if not valid.
        """
        for column_name in column_names_to_read:
            if column_name not in self._header:
                raise InvalidArgumentError("Column \"" + str(column_name) + "\" is not in the file!")
