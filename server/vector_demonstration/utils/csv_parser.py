"""
CSV Parser

Should be fairly resistant to ill-formated data, like missing header, blank cells and blank lines.


Quick example of calling code:
        # Load spreadsheet (either filename or file object)
        csv = CSVParser(csv_file)

        # Loop through rows and pull out values
        for row in csv.valid_rows:
            email = csv.lookup(row, 'EMAIL')
            ...


More advanced example of calling code:
        # Specify required headers
        required_headers = ['EMAIL', 'FIRST_NAME']

        # Specify headers that appear in CSV more than once
        duplicate_headers = ['SCORE']

        # Validate the spreadsheet contains required headers and is well-formatted
        try:
            csv = CSVParser(csv_file, required_headers, duplicate_headers)
        except ValidationError:
            ...

        # Loop through valid rows and pull out values
        for row in csv.valid_rows:
            email = csv.lookup(row, 'EMAIL'),
            scores = csv.lookup(row, 'SCORES', None)
            ...

        # Access headers
        headers = csv.headers

        # Loop through all invalid rows
        for row in csv.invalid_rows:
            ...

"""
import csv
import io

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError


class CSVParser:
    @property
    def headers(self):
        return self._headers

    @property
    def valid_rows(self):
        return list(self.valid_row_dict.values())

    @property
    def invalid_rows(self):
        return list(self.invalid_row_dict.values())

    def __init__(self, file, required=None, duplicate=None, header_starts_with=None):
        """
        Initialize CSV parser.

        Args:
            - file (InMemoryUploadedFile OR string)
                    File object or filename
            - required (list):
                    List of column headers that:
                    - CSV must contain to be valid
                    - Each row must contain a value to be a valid row
            - duplicate (list, optional)
                    List of optional column headers that may repeat.
            - header_starts_with (str, optional)
                    String used to recognize header. (Optionally comma-delimited)
                    If none provided, the first row is the header.
        """
        self.file = file
        self.required_headers = [h.upper() for h in required] if required else []
        self.duplicate_headers = [h.upper() for h in duplicate] if duplicate else []
        self.header_starts_with = header_starts_with
        self._col_lookup = {}
        self._dup_col_lookup = {}
        self.valid_row_dict = {}
        self.invalid_row_dict = {}
        self._load_csv()
        self._validate_csv()
        self._parse_csv()

    def _load_csv(self):
        """
        Load csv file (from disk or memory) into a list of rows.
        """
        # Handle files in memory
        if isinstance(self.file, InMemoryUploadedFile):
            # Start at the beginning of the file
            self.file.seek(0)
            # Read the file as a list of strings, and iterate through it
            try:
                readable_file = io.StringIO(self.file.read().decode("utf-8"))
            except UnicodeDecodeError:
                raise ValidationError(detail="Improper file detected. Input file must be CSV.")
            csv_reader = csv.reader(readable_file, delimiter=",")
            # Pull data out of reader by wrapping it in a list
            self._rows = list(csv_reader)

        # Handle filenames from disk
        elif isinstance(self.file, str):
            with open(self.file, "r") as opened_file:
                csv_reader = csv.reader(opened_file, delimiter=",")
                # Pull data out of reader by wrapping it in a list
                self._rows = list(csv_reader)

        # Raise an error for any other file type
        else:
            raise ValidationError(detail="Invalid file argument provided.")

    def _validate_csv(self):
        """
        Validate CSV and prep for parsing.
        """
        # Find header
        self._header_row_number = self._find_header_row_number()
        self._headers = self._rows[self._header_row_number]

        # Construct a lookup table to hold location of column(s) containing each header.
        for index, header in enumerate(self._headers):
            header = header.upper()

            # If an unexpected duplicate header is found, raise error
            if header in self._col_lookup and header not in self.duplicate_headers:
                raise ValidationError(detail="CSV contains unexpected duplicate headers.")

            # Store column numbers where all headers live
            self._col_lookup[header] = index

            # If a duplicate header is expected and found, store it in a separate structure
            if header in self.duplicate_headers:
                if header in self._dup_col_lookup:
                    self._dup_col_lookup[header].append(index)
                else:
                    self._dup_col_lookup[header] = [index]

        # Validate our CSV contains all required columns.
        for header in self.required_headers:
            try:
                self._col_lookup[header]
            except KeyError:
                required_headers = ", ".join(self.required_headers)
                raise ValidationError(detail=f"CSV missing one of required columns ({required_headers}).")

    def _parse_csv(self):
        """
        Parse CSV and create a dictionary of valid rows.
        """
        for row_num, row in enumerate(self._rows):

            # Skip ahead until we're past the header
            if row_num <= self._header_row_number:
                continue

            # Skip blank rows
            if not row:
                continue

            # Skip rows missing values for required headers
            missing_headers = False
            for header in self.required_headers:
                if self.lookup(row, header) == "":
                    missing_headers = True
            if missing_headers:
                self.invalid_row_dict[row_num] = row
                continue

            # Otherwise, this is a valid row
            self.valid_row_dict[row_num] = row

    def _get_col_num(self, header):
        """
        Returns column number of header.
        """
        # Validate this header is a header we're expecting
        if header.upper() not in [h.upper() for h in self._headers]:
            raise ValidationError(detail=f"Header {header} not found in CSV.")
        return self._col_lookup[header.upper()]

    def lookup(self, row, header, empty_val=""):
        """
        Lookup the value of a unique header within the current row.

        Args:
            - header (string): Header title
            - empty_val (optional): Value to return if row value is empty

        Returns:
            - value of single cell
        """
        col_num = self._get_col_num(header)

        # Return value from row
        try:
            val = row[col_num].strip()
        # This error means there were 1+ empty optional fields at the end of a row.
        except IndexError:
            return empty_val
        return val if val else empty_val

    def _get_col_nums(self, header):
        """
        Returns column numbers of header that appears multiple times in CSV.
        """
        # Validate this header is a header we're expecting
        if header.upper() not in self.duplicate_headers:
            raise ValidationError(detail=f"Duplicate header {header} not in specified duplicate headers.")

        # Look up locations of columns
        return self._dup_col_lookup[header.upper()]

    def lookup_all(self, row, header, empty_val=None):
        """
        Lookup all values of a duplicate header within the current row.

        Args:
            - header (string): Header title
            - empty_val (optional): Value to return if row value is empty

        Returns:
            - array of values of matching cells
        """
        values = []
        col_nums = self._get_col_nums(header)

        # Return array of row values
        for col_num in col_nums:
            try:
                val = row[col_num].strip()
            # This error means there were 1+ empty optional fields at the end of a row.
            except IndexError:
                continue
            val = val if val else empty_val
            values.append(val)

        return values

    def _find_header_row_number(self):
        """
        Returns number of header row.
        """
        # If no header string provided, return the first row
        if not self.header_starts_with:
            return 0
        for row, row_data in enumerate(self._rows):
            # Re-join header row into a single string
            row_data = ",".join(row_data)
            # Compare this string against the header string
            if row_data.upper().startswith(self.header_starts_with.upper()):
                return row
        raise ValidationError(detail="Failed to locate header row within CSV.")

    def get_column(self, header):
        """
        Returns values from a particular spreadsheet column, identified by a header.
        """
        col_num = self._get_col_num(header)
        return [row[col_num] for row in self._rows]
