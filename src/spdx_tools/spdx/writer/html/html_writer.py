# SPDX-FileCopyrightText: 2023 spdx contributors
#
# SPDX-License-Identifier: Apache-2.0
import yaml
from beartype.typing import IO

from spdx_tools.spdx.jsonschema.document_converter import DocumentConverter
from spdx_tools.spdx.model import Document
from spdx_tools.spdx.writer.write_utils import convert, validate_and_deduplicate


def write_document_to_stream(
    document: Document,
    stream: IO[str],
    validate: bool = True,
    converter: DocumentConverter = None,
    drop_duplicates: bool = True,
):
    """
    Serializes the provided document to HTML and writes it to a file with the provided name.
    """
    document = validate_and_deduplicate(document, validate, drop_duplicates)
    document_dict = convert(document, converter)

    stream.write("<!DOCTYPE html>\n")
    stream.write("<html>\n")

    for package in document.packages:
        stream.write(f"<h2>{package.name} ({package.version}) </h2>\n")
        stream.write(f"<h3>{package.license_concluded}</h3>\n\n")

    stream.write("</html>\n")


def write_document_to_file(
    document: Document,
    file_name: str,
    validate: bool = True,
    converter: DocumentConverter = None,
    drop_duplicates: bool = True,
):
    with open(file_name, "w", encoding="utf-8") as out:
        write_document_to_stream(document, out, validate, converter, drop_duplicates)
