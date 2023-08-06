__author__ = "David Scheliga"
__email__ = "david.scheliga@gmx.de"
__version__ = "0.0.1a0.dev5"

__all__ = [
    "DocuSetup",
    "get_target_path_of_documentation",
    "is_static_html_file",
    "unzip_documentation",
    "validate_docu_setup",
]


import copy
import getpass
import json
import re
from collections import namedtuple
from collections.abc import Mapping
from pathlib import Path
from typing import Tuple, Iterator, Optional, Union
from zipfile import ZipFile
import click as click
import requests
from jsonschema import Draft7Validator
from myminions import (
    load_yaml_file_content,
    update_yaml_file_content,
    try_decoding_potential_text_content,
)

APath = Union[str, Path]

STATIC_HTML_ARCHIVE_FOLDER_NAME = "html"
STATIC_HTML_MEMBER_PATTERN = re.compile("^html[/\\\\].*")

DOCUMENTATION_NAME_PATTERN = re.compile("^[a-zA-Z][a-zA-Z0-9_]{2,29}$")
"""
The allowed name pattern of documentations to be uploaded onto handadoc.
"""

SPHINX_SETUP_FILENAME = "conf.py"
"""
Configuration file of sphinx.
"""


PROJECT_SETUP_FILENAME = ".handadoc.yml"
"""
Filename of the handadoc-client setup for an automated documentation deployment.
"""

ARCHIVE_SETUP_FILENAME = "handadoc.json"
SETUP_IS_FINE_VALIDATION_MESSAGE = "Setup is fine."

_HANDADOC_UPLOAD_URL_TEMPLATE = "{handadoc_base_url}/docuitems/"


class DocuSetup(Mapping):
    NAME = "name"
    """
    The documentation unique name, which also will be used as part of the resulting
    url at the handadoc webpage.
    """

    DESCRIPTION = "description"
    """
    The description which appears at the handadoc webpage.
    """

    TITLE = "title"
    """
    The title which appears at the handadoc webpage.
    """

    DOC_LOCATION = "doc_location"
    """
    The location of the static html documentation, 
    which should be post to the handadoc webpage.
    """

    VERSION = "version"
    """
    The version this documentation is related to.
    """

    SERVER_URL = "server_url"
    """
    Base url of the handadoc server.
    """

    REQUIRED_FIELDS = [NAME, DESCRIPTION, DOC_LOCATION]
    """
    The required fields for a minimum setup file declaration.
    """

    ARCHIVE_FIELDS = [NAME, TITLE, DESCRIPTION, VERSION]
    SETUP_FIELDS = [NAME, TITLE, DESCRIPTION, VERSION, DOC_LOCATION]

    def __init__(
        self,
        name: str = "",
        description: str = "",
        doc_location: str = "",
        title: str = "",
        version: str = "",
        server_url: str = "",
        location: Path = None,
    ):
        """

        Examples:
            >>> from handadocclient import DocuSetup
            >>> from doctestprinter import doctest_iter_print
            >>> sample_setup = DocuSetup.from_zip("tests/resources/sample_1/handadoc.zip")
            >>> doctest_iter_print(sample_setup, max_line_width=70)
            name:
              handadoc-client
            title:
              Handadoc Client Documentation
            description:
              Documentation on how to use the handadoc-client within local repositories
              to package and post the build documentation to the handadoc webserver.
            doc_location:
            <BLANKLINE>
            version:
              0.0.1a0
            server_url:
            <BLANKLINE>

            >>> sample_setup.name
            'handadoc-client'
            >>> sample_setup.version
            '0.0.1a0'
        """
        self._values = self._get_blank_setup_values()
        self._values[self.NAME] = name
        self._values[self.DESCRIPTION] = description
        self._values[self.TITLE] = title
        self._values[self.DOC_LOCATION] = doc_location
        self._values[self.VERSION] = version
        self._values[self.SERVER_URL] = server_url
        assert location is None or isinstance(
            location, Path
        ), "location must be a pathlib.Path"
        self._location = location

    def __repr__(self):
        return str(self._values)

    def __getitem__(self, k: str) -> str:
        return self._values[k]

    def __len__(self) -> int:
        return len(self._values)

    def __iter__(self) -> Iterator:
        return iter(self._values)

    @property
    def name(self):
        """"""
        return self._values[self.NAME]

    @property
    def title(self):
        return self._values[self.TITLE]

    @property
    def description(self):
        return self._values[self.DESCRIPTION]

    @property
    def doc_location(self):
        return self._values[self.DOC_LOCATION]

    @property
    def version(self):
        return self._values[self.VERSION]

    @version.setter
    def version(self, new_version: str):
        if new_version is None:
            self._values[self.VERSION] = ""
        else:
            self._values[self.VERSION] = str(new_version)

    @property
    def server_url(self):
        return self._values[self.SERVER_URL]

    @property
    def location(self):
        return self._location

    @property
    def is_from_project_setup(self):
        """
        States whether this setup was from a project .handadoc.yml file or not; which
        would be than from a zip-file.

        .. doctest::
           :hide:

            >>> from handadocclient import DocuSetup
            >>> sample_setup_filepath = "tests/resources/sample_1/.handadoc.yml"
            >>> sample_setup = DocuSetup.from_yaml(sample_setup_filepath)
            >>> sample_setup.is_from_project_setup
            True

            >>> from handadocclient import DocuSetup
            >>> blank_setup = DocuSetup()
            >>> blank_setup.is_from_project_setup
            False

            >>> from pathlib import Path
            >>> zip_filepath = Path("tests/resources/sample_1/handadoc.zip")
            >>> zip_setup = DocuSetup.from_zip(zip_filepath=zip_filepath)
            >>> zip_setup.is_from_project_setup
            False

        """
        return (
            self._location is not None and self._location.name == PROJECT_SETUP_FILENAME
        )

    @classmethod
    def _get_blank_setup_values(cls) -> dict:
        return {
            cls.NAME: "",
            cls.TITLE: "",
            cls.DESCRIPTION: "",
            cls.DOC_LOCATION: "",
            cls.VERSION: "",
            cls.SERVER_URL: "",
        }

    @classmethod
    def docu_setup_to_archive_setup(cls, project_setup) -> dict:
        """
        Turns the project setup containing more options to the required setup
        for the handadoc webpage.

        Args:
            project_setup(dict):
                Setup of the local repository.

        Returns:
            dict

        Examples:
            >>> from handadocclient import DocuSetup
            >>> sample_setup = DocuSetup()
            >>> DocuSetup.docu_setup_to_archive_setup(sample_setup)
            {'name': '', 'title': '', 'description': '', 'version': ''}
        """
        archive_setup = {
            archive_field: copy.copy(project_setup[archive_field])
            for archive_field in cls.ARCHIVE_FIELDS
            if archive_field in project_setup
        }
        return archive_setup

    @classmethod
    def create_yaml_filepath(cls, project_root_path: APath) -> Path:
        """
        Creates the filepath of the handadoc setup yaml file.

        Args:
            project_root_path:
                The project's root path.

        Returns:
            Path

        Examples:
            >>> from handadoc_client import DocuSetup

            This function returns the default, targeted setup filepath.

            >>> str(DocuSetup.create_yaml_filepath("/a/path"))
            '/a/path/.handadoc.yml'

            Existing, different file name will be changed.

            >>> str(DocuSetup.create_yaml_filepath("../handadoc_client/setup.py"))
            '../handadoc_client/.handadoc.yml'

            But non existing filepath's will be used and may lead to errors.

            >>> str(DocuSetup.create_yaml_filepath("./not_existing_file.yml"))
            'not_existing_file.yml/.handadoc.yml'
        """
        project_root_path = Path(project_root_path)
        if project_root_path.is_file():
            project_root_path = project_root_path.parent
        setup_filepath = project_root_path.joinpath(PROJECT_SETUP_FILENAME)
        return setup_filepath

    @classmethod
    def from_yaml(cls, filepath: APath) -> "DocuSetup":
        """
        Reads a handadoc setup from a yaml file.

        Args:
            filepath:
                The yaml filepath from which to read.

        Returns:
            DocuSetup

        .. doctest::

            >>> from handadocclient import DocuSetup
            >>> from doctestprinter import doctest_iter_print
            >>> sample_path = "tests/resources/sample_1/.handadoc.yml"
            >>> sample_setup = DocuSetup.from_yaml(sample_path)
            >>> doctest_iter_print(sample_setup)
            name:
              handadoc-client-test1
            title:
              Handadoc Client Documentation Test1
            description:
              A set of test documentation files.
            doc_location:
              tests/resources/sample_1/html
            version:
              0.1a2.dev3
            server_url:
              http://127.0.0.1:8000
        """
        docu_setup_content = load_yaml_file_content(filepath=filepath)
        return DocuSetup(location=Path(filepath), **docu_setup_content)

    def to_yaml(self, project_root_path: Optional[APath]) -> Path:
        """
        Writes a yaml handadoc configuration file.

        Notes:
            The resulting configuration filename will be *.handadoc.yml*

        Args:
            project_root_path:
                The project's root path.

        Returns:
            Path:
                The resulting yaml filepath.

        Examples:

            >>> from handadoc_client import DocuSetup
            >>> from tempfile import TemporaryDirectory
            >>> with TemporaryDirectory() as temp_dir:
            ...     test_path = Path(temp_dir)
            ...     sample_doc = DocuSetup(
            ...         "test", "This is a test.", "A test", "some/where/html"
            ...     )
            ...     yaml_filepath = sample_doc.to_yaml(test_path)
            ...     print("Resulting file path:", yaml_filepath.relative_to(test_path))
            Resulting file path: .handadoc.yml

        .. doctest::

            >>> from handadoc_client import DocuSetup
            >>> from tempfile import TemporaryDirectory
            >>> from doctestprinter import doctest_iter_print
            >>> with TemporaryDirectory() as temp_dir:
            ...     test_path = Path(temp_dir)
            ...     sample_doc = DocuSetup(
            ...         "test", "This is a test.", "A test", "some/where/html"
            ...     )
            ...     resulting_filepath = sample_doc.to_yaml(test_path)
            ...     retrieved_setup = sample_doc.from_yaml(resulting_filepath)
            ...     doctest_iter_print(retrieved_setup)
            name:
              test
            title:
              some/where/html
            description:
              This is a test.
            doc_location:
              A test
            version:
            <BLANKLINE>
            server_url:
            <BLANKLINE>

        """
        project_root_path = Path(project_root_path)
        if project_root_path.is_file():
            project_root_path = project_root_path.parent
        setup_filepath = project_root_path.joinpath(PROJECT_SETUP_FILENAME)

        setup_fields = {key: self._values[key] for key in self.SETUP_FIELDS}

        update_yaml_file_content(setup_filepath, setup_fields)
        return setup_filepath

    @classmethod
    def from_bytes(cls, byte_content) -> "DocuSetup":
        """
        .. doctest::

            >>> from handadocclient import DocuSetup
            >>> from doctestprinter import doctest_iter_print
            >>> sample_path = "tests/resources/sample_1/handadoc.json"
            >>> with open(sample_path, "rb") as setup_file:
            ...     binary_content = setup_file.read()
            ...     sample_setup = DocuSetup.from_bytes(binary_content)
            >>> doctest_iter_print(sample_setup, max_line_width=70)
            name:
              handadoc-client
            title:
              Handadoc Client Documentation
            description:
              Documentation on how to use the handadoc-client within local repositories
              to package and post the build documentation to the handadoc webserver.
            doc_location:
              docs/_build/html
            version:
              0.0.1a0
            server_url:
            <BLANKLINE>

        """
        utf8_representation = try_decoding_potential_text_content(byte_content)
        archive_setup = json.loads(utf8_representation)
        return cls(**archive_setup)

    @classmethod
    def from_opened_zip(cls, opened_archive: ZipFile) -> dict:
        """
        .. doctest::

            >>> from handadocclient import DocuSetup
            >>> from doctestprinter import doctest_iter_print
            >>> sample_archive_path = "tests/resources/sample_1/handadoc.zip"
            >>> from zipfile import ZipFile
            >>> with ZipFile(sample_archive_path, "r") as doc_zip_filepath:
            ...     setup_from_archive = DocuSetup.from_opened_zip(doc_zip_filepath)
            >>> doctest_iter_print(setup_from_archive, max_line_width=70)
            name:
              handadoc-client
            title:
              Handadoc Client Documentation
            description:
              Documentation on how to use the handadoc-client within local repositories
              to package and post the build documentation to the handadoc webserver.
            doc_location:
            <BLANKLINE>
            version:
              0.0.1a0
            server_url:
            <BLANKLINE>
        """
        byte_content = opened_archive.read("handadoc.json")
        return cls.from_bytes(byte_content=byte_content)

    @classmethod
    def from_zip(cls, zip_filepath: Union[str, Path]) -> "DocuSetup":
        """"""
        with ZipFile(zip_filepath, "r") as zip_file:
            docu_setup = cls.from_opened_zip(opened_archive=zip_file)
        return docu_setup

    @staticmethod
    def is_a_valid_documentation_name(documentation_name_to_check: str) -> bool:
        """
        Validates the name in terms of the regular expression ^[a-zA-Z][a-zA-Z0-9_]{2,29}$

        Examples:
            >>> from handadocclient import DocuSetup
            >>> DocuSetup.is_a_valid_documentation_name("A_valid_name")
            True
            >>> DocuSetup.is_a_valid_documentation_name("A_valid_name_2")
            True
            >>> DocuSetup.is_a_valid_documentation_name("A")  # to short
            False
            >>> DocuSetup.is_a_valid_documentation_name(
            ...     "A_name_which_is_to_long_is_invalid"
            ... )
            False
            >>> DocuSetup.is_a_valid_documentation_name("4_leading_number_is_invalid")
            False
            >>> DocuSetup.is_a_valid_documentation_name("Whitespaces are invalid")
            False

        Args:
            documentation_name_to_check(str):
                The documentation name.

        Returns:
            bool
        """
        return DOCUMENTATION_NAME_PATTERN.match(documentation_name_to_check) is not None


_SETUP_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Setup for the handadoc client.",
    "description": "Field of the handadoc client setup for packaging "
    "and release of documentations via handadoc.",
    "type": "object",
    "properties": {
        DocuSetup.NAME: {
            "description": "An alternate path fitting url path for the documentation.",
            "type": "string",
            "minLength": 1,
            "maxLength": 36,
            "pattern": "^[a-zA-Z0-9-_]+$",
        },
        DocuSetup.TITLE: {"type": "string", "pattern": r"[a-zA-Z0-9\s'_]+$"},
        DocuSetup.DESCRIPTION: {
            "type": "string",
            "minLength": 0,
            "maxLength": 1024,
        },
        DocuSetup.DOC_LOCATION: {
            "type": "string",
            "description": "The location of the build static html documentation.",
        },
        DocuSetup.VERSION: {
            "description": "The project's or documentation's version.",
            "type": "string",
        },
    },
    "required": DocuSetup.REQUIRED_FIELDS,
}


ProcessMessage = namedtuple("ProcessMessage", "success message")


def validate_docu_setup(setup_to_validate: dict) -> ProcessMessage:
    """

    .. doctest::

        >>> # access of protected member for doctest
        >>> # noinspection PyProtectedMember
        >>> from handadocclient import validate_docu_setup, _get_project_setup
        >>> from pathlib import Path
        >>> from doctestprinter import doctest_print
        >>> archive_setup = _get_project_setup(Path("./"))
        >>> validate_docu_setup(setup_to_validate=archive_setup)
        ProcessMessage(success=True, message='Setup is fine.')

        >>> an_invalid_setup = {
        ...     "title": "Title invalid $%&§$()§) characters.",
        ...     "name": "Invalid documentation name."
        ... }
        >>> doctest_print(validate_docu_setup(an_invalid_setup), max_line_width=60)
        ProcessMessage(success=False, message='\\'Invalid documentation
        name.\\' does not match \\'^[a-zA-Z0-9-_]+$\\' and \\'Title invalid
        $%&§$()§) characters.\\' does not match "[a-zA-Z0-9\\\\\\\\s\\'_]+$"
        and \\'description\\' is a required property and \\'doc_location\\'
        is a required property')


        >>> an_invalid_setup["description"] = "This is an invalid setup."
        >>> an_invalid_setup["doc_location"] = "docs/_build/html"
        >>> doctest_print(validate_docu_setup(an_invalid_setup), max_line_width=60)
        ProcessMessage(success=False, message='\\'Invalid documentation
        name.\\' does not match \\'^[a-zA-Z0-9-_]+$\\' and \\'Title invalid
        $%&§$()§) characters.\\' does not match "[a-zA-Z0-9\\\\\\\\s\\'_]+$"')

    """
    mapping_to_validate = dict(setup_to_validate)
    setup_schema_validator = Draft7Validator(_SETUP_SCHEMA)
    if setup_schema_validator.is_valid(mapping_to_validate):
        return ProcessMessage(True, SETUP_IS_FINE_VALIDATION_MESSAGE)

    caught_error_messages = []
    for error in sorted(
        setup_schema_validator.iter_errors(mapping_to_validate), key=str
    ):
        caught_error_messages.append(error.message)

    all_whats_wrong = " and ".join(caught_error_messages)
    return ProcessMessage(False, all_whats_wrong)


def _find_setup_filepath(root_path: Path) -> Path:
    """
    Finds the filepath of the *handadoc client setup*.

    Args:
        root_path(Path):
            Root path in which the setup file lives.

    Raises:
        FileNotFoundError:
            If root path doesn't exist or no setup file found.

    .. doctest::

        >>> from doctestprinter import repr_posix_path
        >>> from pathlib import Path
        >>> package_root = Path("./")
        >>> found_setup_filepath = _find_setup_filepath(package_root)
        >>> repr_posix_path(found_setup_filepath)
        '.handadoc.yml'
        >>> sample_1_path = Path("tests/resources/sample_1")
        >>> found_setup_filepath = _find_setup_filepath(sample_1_path)
        >>> repr_posix_path(found_setup_filepath)
        'tests/resources/sample_1/.handadoc.yml'

    """
    if not root_path.exists():
        raise FileNotFoundError("Path {} does not exist.".format(root_path))
    found_file_path = None
    for setup_file_path in root_path.rglob(PROJECT_SETUP_FILENAME):
        found_file_path = setup_file_path
        break
    if found_file_path is None:
        raise FileNotFoundError(
            "No {} file found within path tree of {}".format(
                PROJECT_SETUP_FILENAME, root_path
            )
        )
    return found_file_path


def _extract_version_number(content: str) -> str:
    """
    .. doctest::

        >>> from handadocclient import _extract_version_number
        >>> sample_1 = '#\\n#\\n#\\n\\nrelease = "0.0.1a0"#\\n\\n'
        >>> _extract_version_number(sample_1)
        '0.0.1a0'
        >>> sample_2 = '#\\n#\\n#\\n\\nrelease = "0.0.1a0.dev1.post1"#\\n\\n'
        >>> _extract_version_number(sample_2)
        '0.0.1a0.dev1.post1'
        >>> sample_3 = "#\\n#\\n#\\n\\nrelease = no_number#\\n\\n"
        >>> _extract_version_number(sample_3)

    """
    finds_version_number = re.compile(
        r"^release = [\"']([0-9\.abrcdevpost]+)[\"']", re.MULTILINE
    )
    found_match = finds_version_number.search(content)
    if found_match is None:
        return None
    return found_match.group(1)


def _find_sphinx_config_filepath(root_path: Path) -> Path:
    """
    Finds the filepath of the *sphinx configuration*.

    Args:
        root_path(Path):
            Root path in which the setup file lives.

    .. doctest::

        >>> from doctestprinter import repr_posix_path
        >>> from pathlib import Path
        >>> package_root = Path("./")
        >>> found_setup_filepath = _find_sphinx_config_filepath(package_root)
        >>> repr_posix_path(found_setup_filepath)
        'docs/conf.py'
    """
    for setup_file_path in root_path.rglob(SPHINX_SETUP_FILENAME):
        with setup_file_path.open("r") as configuration_file:
            first_line = configuration_file.readline()
            if "Sphinx" not in first_line:
                continue
        return setup_file_path


def _get_sphinx_docu_version_number(sphinx_config_filepath: Path) -> str:
    """
    .. doctest::
        >>> from handadocclient import (
        ...     _find_sphinx_config_filepath, _get_sphinx_docu_version_number
        ... )
        >>> from pathlib import Path
        >>> config_filepath = _find_sphinx_config_filepath(Path("./"))
        >>> _get_sphinx_docu_version_number(config_filepath)
        '0.0.1a0.dev3'
    """
    assert isinstance(
        sphinx_config_filepath, Path
    ), "sphinx_config_filepath must be a pathlib.Path"
    with sphinx_config_filepath.open("r") as sphinx_config_file:
        sphinx_config_content = sphinx_config_file.read()
    version_number = _extract_version_number(content=sphinx_config_content)
    return version_number


def _get_project_setup(root_path: Path) -> DocuSetup:
    """
    Generates the setup based on the .handadoc.yml file.

    .. doctest::

        >>> from doctestprinter import doctest_iter_print
        >>> from pathlib import Path
        >>> archive_setup = _get_project_setup(Path("tests/resources/sample_1"))
        >>> doctest_iter_print(archive_setup, max_line_width=70)
        name:
          handadoc-client-test1
        title:
          Handadoc Client Documentation Test1
        description:
          A set of test documentation files.
        doc_location:
          tests/resources/sample_1/html
        version:
          0.1a2.dev3
        server_url:
          http://127.0.0.1:8000

    """
    assert isinstance(root_path, Path), "project_root_path should be a pathlib.Path"
    setup_filepath = _find_setup_filepath(root_path=root_path)
    docu_setup = DocuSetup.from_yaml(filepath=setup_filepath)

    a_specific_doc_version_is_not_set = docu_setup.version == ""
    if a_specific_doc_version_is_not_set:
        sphinx_config_filepath = _find_sphinx_config_filepath(root_path=root_path)
        doc_version = _get_sphinx_docu_version_number(sphinx_config_filepath)
        docu_setup.version = doc_version
    return docu_setup


def _zip_docu_setup(opened_archive: ZipFile, archive_setup: DocuSetup):
    """
    Archives the setup file.

    Args:
        opened_archive:
        archive_setup:

    """
    serializable_setup = dict(archive_setup)
    setup_file_content = json.dumps(
        serializable_setup, indent="    ", ensure_ascii=False
    )
    byte_content = setup_file_content.encode("utf-8")
    opened_archive.writestr(zinfo_or_arcname=ARCHIVE_SETUP_FILENAME, data=byte_content)


def _zip_docu_folder(opened_archive: ZipFile, documentation_path: Path):
    all_file_paths = list(documentation_path.rglob("*"))
    for file_path in all_file_paths:
        archive_path = file_path.relative_to(documentation_path)
        opened_archive.write(file_path, arcname=str(archive_path))


def _make_docu_upload_zipfile(zip_filepath: Path, docu_setup: dict):
    """
    Archives the documentation and returns the archive path.

    Args:
        zip_filepath(Path):
            The destination package path.

        docu_setup(dict):
            The documentation's setup states the title, description, location,
            path_url and version.

    Returns:
        Path:
            Path of the archive-file.
    """
    archive_setup = DocuSetup.docu_setup_to_archive_setup(docu_setup)
    documentation_path = Path(docu_setup.doc_location).resolve()
    if not documentation_path.exists():
        raise FileExistsError(
            "The documentation html build path {} does not exist. Build it first!"
            "".format(documentation_path)
        )

    with ZipFile(str(zip_filepath), mode="w") as archive_file:
        _zip_docu_setup(archive_file, archive_setup)
        _zip_docu_folder(archive_file, documentation_path)


def _get_archive_filename(valid_project_setup: dict) -> str:
    """

    Args:
        valid_project_setup:

    Returns:

    .. doctest::
       :hide:

        >>> # access of protected member for doctest
        >>> # noinspection PyProtectedMember
        >>> from handadocclient import _get_archive_filename, _get_project_setup
        >>> from pathlib import Path
        >>> sample_setup = DocuSetup(
        ...     name="handadoc-client",
        ...     description="A simple docu-html-server.",
        ...     version="0.1.2"
        ... )
        >>> _get_archive_filename(sample_setup)
        'handadoc-client-0.1.2.zip'
    """
    project_name = valid_project_setup.name
    version = valid_project_setup.version
    if not version:
        version = "latest"
    return "{}-{}.zip".format(project_name, version)


def _package_project(work_path: Path, valid_docu_setup: dict) -> Path:
    """
    Packages the project's documentation for transfer.

    Args:
        work_path(Path):
            A work path in which the package will be created.

        valid_docu_setup(Path):
            The project's setup from teh .handadoc.yml, which was validated.

    Returns:
        Path:
            Path of the archived documentation for the handadoc webpage.
    """
    assert isinstance(work_path, Path), "work_path needs to be a pathlib.Path"
    assert isinstance(valid_docu_setup, DocuSetup), "setup needs to be a DocuSetup."

    if not valid_docu_setup.is_from_project_setup:
        raise ValueError(
            "The documentation setup needs a .handadoc.yml filepath defined."
        )

    filename = _get_archive_filename(valid_project_setup=valid_docu_setup)
    zip_file_path = valid_docu_setup.location.with_name(filename)
    _make_docu_upload_zipfile(zip_filepath=zip_file_path, docu_setup=valid_docu_setup)
    return zip_file_path


def _get_upload_post_url(handadoc_url: str) -> str:
    """
    .. doctest::

        >>> from handadocclient import _get_upload_post_url
        >>> _get_upload_post_url("http://handadoc")
        'http://handadoc/docuitems/'
        >>> _get_upload_post_url("http://handadoc/")
        'http://handadoc/docuitems/'
    """
    if handadoc_url[-1] != "/":
        return _HANDADOC_UPLOAD_URL_TEMPLATE.format(handadoc_base_url=handadoc_url)
    return _HANDADOC_UPLOAD_URL_TEMPLATE.format(handadoc_base_url=handadoc_url[:-1])


def _transfer_to_handadoc(
    handadoc_base_url: str, zip_filepath: Path, user_credentials: Tuple[str, str]
) -> bool:
    """

    Raises:
        requests.exceptions.ConnectionError:
            If server is offline.

    Args:
        handadoc_base_url:

    Returns:
        bool:
            If upload was successful.
    """
    with requests.Session() as s:
        s.auth = user_credentials
        with zip_filepath.open("rb") as zip_archive:
            upload_file = {"zip_archive": zip_archive}
            upload_url = _get_upload_post_url(handadoc_url=handadoc_base_url)
            r = s.post(upload_url, files=upload_file)
            r.raise_for_status()
    return True


def _request_user_credentials() -> dict:
    logged_in_username = getpass.getuser()
    input_user = input("Username [{}]: ".format(logged_in_username))
    if input_user == "":
        username = logged_in_username
    else:
        username = input_user
    password = getpass.getpass()
    return username, password


def _archive_and_transfer(handadoc_ulr: str, project_root_path: Path) -> ProcessMessage:
    """

    Args:
        handadoc_ulr:
        project_root_path:

    Returns:

    """
    assert isinstance(
        project_root_path, Path
    ), "project_root_path must be a pathlib.Path"
    project_setup = _get_project_setup(root_path=project_root_path)
    validation_message = validate_docu_setup(setup_to_validate=project_setup)
    project_setup_is_ok = validation_message.success
    if not project_setup_is_ok:
        return False
    valid_project_setup = project_setup

    user_credentials = _request_user_credentials()
    package_path = _package_project(
        work_path=project_root_path, valid_docu_setup=valid_project_setup
    )
    _transfer_to_handadoc(
        handadoc_base_url=handadoc_ulr,
        zip_filepath=package_path,
        user_credentials=user_credentials,
    )
    return True


def get_docu_sub_path(project_setup: dict) -> Path:
    """
    .. doctest::

        >>> from handadocclient import get_docu_sub_path
        >>> sample_setup = {"name": "handadoc-client", "version": "0.0.1a0"}
        >>> get_docu_sub_path({"name": "handadoc-client", "version": "0.0.1a0"})
        'handadoc-client/0.0.1a0'
        >>> get_docu_sub_path(
        ...     {"name": "handadoc-client", "version": ""}
        ... )
        'handadoc-client/latest'
    """
    doc_name = project_setup[DocuSetup.NAME]
    version = project_setup[DocuSetup.VERSION]
    if version is None or not version:
        version = "latest"
    sub_path = "{doc_name}/{version}".format(doc_name=doc_name, version=version)
    return sub_path


def get_target_path_of_documentation(
    root_path_of_documentations: Path,
    docu_setup: dict,
) -> Path:
    """
    Makes the root folder path of the documentation.

    Args:
        root_path_of_documentations(Path):
            Root path of the static html documentations.

        docu_setup:
            The documentation's setup.

    Returns:
        Path

    Examples:
        >>> from handadocclient import get_target_path_of_documentation
        >>> from pathlib import Path
        >>> from doctestprinter import repr_posix_path
        >>> sample_path = get_target_path_of_documentation(
        ...     "root", {"name": "handadoc-client", "version": "0.0.1a0"}
        ... )
        >>> repr_posix_path(sample_path)
        'root/handadoc-client/0.0.1a0'
        >>> sample_path = get_target_path_of_documentation(
        ...     "root", {"name": "handadoc-client", "version": ""}
        ... )
        >>> repr_posix_path(sample_path)
        'root/handadoc-client/latest'
    """
    sub_path = get_docu_sub_path(project_setup=docu_setup)
    root_path_of_documentation = Path(root_path_of_documentations).joinpath(sub_path)
    return root_path_of_documentation


def is_static_html_file(filepath: str) -> bool:
    return STATIC_HTML_MEMBER_PATTERN.match(filepath) is not None


def _unzip_doc_files_into_target_directory(
    doc_zip_filepath: Path, docu_target_path: Path
):
    """
    Examples:
        >>> import tempfile
        >>> from pathlib import Path
        >>> with tempfile.TemporaryDirectory() as temporary_documentation_root:
        ...     project_root_path = Path(temporary_documentation_root)
        ...     docu_root_path = project_root_path.joinpath("docu")
        ...     docu_root_path.mkdir(parents=True)
        ...     _unzip_doc_files_into_target_directory(
        ...         Path("tests/resources/sample_1/handadoc.zip"),
        ...         docu_target_path=docu_root_path
        ...     )
        ...     for filepath in project_root_path.rglob("*"):
        ...         print(filepath.relative_to(project_root_path))
        docu
        docu/subdir
        docu/index.html
        docu/dummy_icon.png
        docu/handadoc.json
        docu/subdir/subdir
        docu/subdir/.subfile.txt

    Args:
        doc_zip_filepath(ZipFile):

        docu_target_path:

    Returns:

    """
    with ZipFile(doc_zip_filepath) as documentation_archive:
        documentation_archive.extractall(docu_target_path)


def unzip_documentation(destination_path: str, doc_zip_filepath):
    """
    Extracts the documentation.

    Examples:
        >>> from handadocclient import unzip_documentation
        >>> from tempfile import TemporaryDirectory
        >>> from pathlib import Path
        >>> with TemporaryDirectory() as temp_dir:
        ...     test_root = Path(temp_dir)
        ...     docu_path = test_root.joinpath("handadoc-client/0.0.1a0")
        ...     unzip_documentation(
        ...         docu_path, "tests/resources/sample_1/handadoc.zip"
        ...     )
        ...     for filepath in docu_path.rglob("*"):
        ...         print(filepath.relative_to(test_root))
        handadoc-client/0.0.1a0/subdir
        handadoc-client/0.0.1a0/index.html
        handadoc-client/0.0.1a0/dummy_icon.png
        handadoc-client/0.0.1a0/handadoc.json
        handadoc-client/0.0.1a0/subdir/subdir
        handadoc-client/0.0.1a0/subdir/.subfile.txt




    """
    destination_path = Path(destination_path)
    if destination_path.exists():
        is_not_empty = len(list(destination_path.rglob("*"))) > 0
        if is_not_empty:
            raise FileExistsError(
                "The destination '{}' already exist and"
                " is not empty.".format(destination_path)
            )

    _unzip_doc_files_into_target_directory(
        doc_zip_filepath=doc_zip_filepath,
        docu_target_path=destination_path,
    )


@click.group()
def cli():
    pass


def _validate_if_path_exist(ctx, param, value):
    if value is not None and not Path(value).exists():
        raise click.BadParameter("Path '{}' does not exist.".format(value))


@click.command("pack")
@click.option(
    "-d", "--project-root-path",
    type=click.Path(),
    help="The project's root path (where the .handadoc.yml and sphinx doc live).",
    callback=_validate_if_path_exist,
)
def cli_pack(project_root_path: Optional[Path] = None):
    """
    Archives a build sphinx documentation to a handadoc-<version>.zip file for
    manual upload.
    """
    if project_root_path is None:
        project_root_path = Path("./").resolve()

    docu_setup = _get_project_setup(project_root_path)
    _package_project(work_path=project_root_path, valid_docu_setup=docu_setup)


@click.command("init")
@click.option(
    "-d", "--project-root-path",
    type=click.Path(),
    help="The project's root path (where the .handadoc.yml and sphinx doc live).",
    callback=_validate_if_path_exist,
)
def cli_init(project_root_path: str):
    """
    Creates an starter .handadoc.yml configuration file.
    """
    if project_root_path is None:
        project_root_path = Path("./").resolve()

    target_yaml_filepath = DocuSetup.create_yaml_filepath(
        project_root_path=project_root_path
    )
    if target_yaml_filepath.exists():
        click.echo("{} already exist. Done nothing.".format(PROJECT_SETUP_FILENAME))
    else:
        DocuSetup().to_yaml(project_root_path=project_root_path)


@click.command("over")
@click.option(
    "-d", "--project-root-path",
    type=click.Path(),
    help="The project's root path (where the .handadoc.yml and sphinx doc live).",
    callback=_validate_if_path_exist,
)
@click.option(
    "-s", "--server-url",
    type=click.STRING,
    help="The server address to push to if not within the .handadoc.yml",
)
def cli_push(
    project_root_path: Optional[Path] = None, server_url: Optional[str] = None
):
    """
    (Archives and) push a valid documentation to the server.
    """
    if project_root_path is None:
        project_root_path = Path("./").resolve()
    else:
        project_root_path = Path(project_root_path)
    project_setup = _get_project_setup(project_root_path)
    if server_url is None:
        server_url = project_setup.server_url

    no_server_was_defined = server_url is None or server_url == ""
    if no_server_was_defined:
        click.echo(
            "Error: The server url is not specified within the {} or by the parameter"
            " --server-url."
            "".format(PROJECT_SETUP_FILENAME),
            err=True,
        )

    try:
        success = _archive_and_transfer(
            handadoc_ulr=server_url, project_root_path=project_root_path
        )
    except requests.exceptions.ConnectionError:
        click.echo("Error: Server {} cannot be reached.".format(server_url), err=True)
        return

    if not success:
        click.echo("Error: Documentation could not be uploaded.", err=True)


cli.add_command(cli_pack)
cli.add_command(cli_init)
cli.add_command(cli_push)


if __name__ == "__main__":
    cli()