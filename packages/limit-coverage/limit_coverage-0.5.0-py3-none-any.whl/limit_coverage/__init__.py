import argparse
import collections
import logging
import os
import pathlib
import re
import shutil
import sqlite3
import sys
import tempfile
import typing


__version__ = "0.5.0"

FileID = typing.NewType("FileID", int)
FileID.__doc__ = """\
The numeric identifier of a source file in the coverage database."""
ContextID = typing.NewType("ContextID", int)
ContextID.__doc__ = """\
The numeric identifier of an execution context in the coverage database."""
SourceModule = typing.NewType("SourceModule", str)
SourceModule.__doc__ = """The import path of a Python module."""
TestModule = typing.NewType("TestModule", str)
TestModule.__doc__ = """The import path of a Python module containing tests."""

MODULE_RE = re.compile(r"tests\.((?:\w+\.)*)test_(\w+)")

Rows = typing.List[typing.Tuple[int]]

logger = logging.getLogger(__name__)


def modules_under_test(test_module: TestModule) -> typing.Iterator[SourceModule]:
    # TODO: take the pragmas and such
    # Since it's hard to even FIND the module in a monorepo,
    # instead of pragmas, this needs a top-level config file that maps test
    # modules to source modules, and supports disabling "auto-discovery".
    match = MODULE_RE.fullmatch(test_module)
    if match:
        yield SourceModule("".join(match.groups()))


def get_module_contexts(
    c: sqlite3.Cursor
) -> typing.Tuple[typing.Mapping[TestModule, typing.Set[ContextID]], ContextID]:

    module_contexts: typing.MutableMapping[
        TestModule, typing.Set[ContextID]
    ] = collections.defaultdict(set)

    for id_, context in c.execute("SELECT id, context FROM context;"):
        if context == "":
            empty_context = ContextID(id_)
        else:
            module_contexts[TestModule(context.rsplit(".", 1)[0])].add(ContextID(id_))

    for context_set in module_contexts.values():
        context_set.add(empty_context)

    return module_contexts, empty_context


def get_contexts_for_module(
    module_contexts: typing.Mapping[TestModule, typing.Set[ContextID]],
    empty_context: ContextID,
) -> typing.Mapping[SourceModule, typing.Set[ContextID]]:

    contexts_for_module: typing.MutableMapping[
        SourceModule, typing.Set[ContextID]
    ] = collections.defaultdict(lambda: {empty_context})

    for test_module, contexts in module_contexts.items():
        for module in modules_under_test(test_module):
            contexts_for_module[module].update(contexts)

    return contexts_for_module


def get_cursor(cov_file) -> sqlite3.Cursor:
    return sqlite3.connect(cov_file).cursor()


def get_rows_to_drop_arc(
    c: sqlite3.Cursor, whitelisted_ids: typing.Mapping[FileID, typing.Set[ContextID]]
) -> Rows:

    rows_to_drop: Rows = []

    for rowid, file_id, context_id in c.execute(
        "SELECT rowid, file_id, context_id FROM arc;"
    ):
        allowed_contexts = whitelisted_ids.get(FileID(file_id))
        if allowed_contexts is None:
            continue
        if ContextID(context_id) not in allowed_contexts:
            rows_to_drop.append((rowid,))

    return rows_to_drop


def delete_arcs(c: sqlite3.Cursor, rows_to_drop: Rows):

    c.executemany("DELETE FROM arc WHERE rowid=?", rows_to_drop)


def get_rows_to_drop_lines(
    c: sqlite3.Cursor, whitelisted_ids: typing.Mapping[FileID, typing.Set[ContextID]]
) -> Rows:

    rows_to_drop: Rows = []

    for rowid, file_id, context_id in c.execute(
        "SELECT rowid, file_id, context_id FROM line_map;"
    ):
        allowed_contexts = whitelisted_ids.get(FileID(file_id))
        if allowed_contexts is None:
            continue
        if ContextID(context_id) not in allowed_contexts:
            rows_to_drop.append((rowid,))

    return rows_to_drop


def delete_lines(c: sqlite3.Cursor, rows_to_drop: Rows):

    c.executemany("DELETE FROM line_map WHERE rowid=?", rows_to_drop)


def get_rows_to_drop_line_bits(
    c: sqlite3.Cursor, whitelisted_ids: typing.Mapping[FileID, typing.Set[ContextID]]
) -> Rows:

    rows_to_drop: Rows = []

    for rowid, file_id, context_id in c.execute(
        "SELECT rowid, file_id, context_id FROM line_bits;"
    ):
        allowed_contexts = whitelisted_ids.get(FileID(file_id))
        if allowed_contexts is None:
            continue
        if ContextID(context_id) not in allowed_contexts:
            rows_to_drop.append((rowid,))

    return rows_to_drop


def delete_line_bits(c: sqlite3.Cursor, rows_to_drop: Rows):

    c.executemany("DELETE FROM line_bits WHERE rowid=?", rows_to_drop)


def conditional(dir_name: str, cwd: str) -> str:
    maybe_src = os.path.join(cwd, dir_name)
    if os.path.isdir(maybe_src):
        return maybe_src
    return cwd


def get_whitelisted_ids(
    c: sqlite3.Cursor,
    contexts_for_module: typing.Mapping[SourceModule, typing.Set[ContextID]],
) -> typing.Mapping[FileID, typing.Set[ContextID]]:

    cwd = os.getcwd()

    pardir = os.pardir + os.sep
    tests = "tests" + os.sep
    src = "src" + os.sep

    whitelisted_ids: typing.MutableMapping[FileID, typing.Set[ContextID]] = {}

    for id_, path in c.execute("SELECT id, path FROM file;"):
        repo_path = os.path.relpath(path, cwd)
        logger.debug("Getting info for path %r", repo_path)
        # Single project case
        if repo_path.startswith((src, tests)):
            logger.debug("Single project case")
            source_root = conditional("src", cwd)
        # "Monorepo" case
        else:
            logger.debug("Possible monorepo case")
            repo_path_pathlib = pathlib.Path(repo_path)
            if repo_path_pathlib.parts[0] == "projects":
                prefix = repo_path_pathlib.parts[:2]
            else:
                prefix = repo_path_pathlib.parts[:1]
            source_root = conditional("src", os.path.join(cwd, *prefix))
        logger.debug("Source root: %r", source_root)
        relpath = os.path.relpath(path, source_root)
        logger.debug("Relpath: %r", relpath)
        if relpath.startswith((pardir, tests)):
            logger.debug("Skipping whitelist")
            continue
        directory, file_ = os.path.split(os.path.splitext(relpath)[0])
        names = directory.split(os.sep)
        if file_ != "__init__":
            names.append(file_)
        whitelisted_ids[FileID(id_)] = contexts_for_module[
            SourceModule(".".join(names))
        ]

    return whitelisted_ids


def _common(c):
    return get_whitelisted_ids(c, get_contexts_for_module(*get_module_contexts(c)))


def line_schema_3(c):
    delete_lines(c, get_rows_to_drop_lines(c, _common(c)))


def line_schema_7(c):
    delete_line_bits(c, get_rows_to_drop_line_bits(c, _common(c)))


SCHEMATA_LINE = {3: line_schema_3, 7: line_schema_7}


def arc_schema_3_and_7(c):

    delete_arcs(c, get_rows_to_drop_arc(c, _common(c)))


SCHEMATA_ARC = {3: arc_schema_3_and_7, 7: arc_schema_3_and_7}


def meta_schema_3(c):
    return c.execute("SELECT has_arcs FROM meta;").fetchone()[0]


def meta_schema_7(c):
    return c.execute("SELECT value FROM meta WHERE key='has_arcs';").fetchone()[0]


def get_schema(c):
    return c.execute("SELECT version FROM coverage_schema;").fetchone()[0]


SCHEMATA_META = {3: meta_schema_3, 7: meta_schema_7}


def parse_args(args):
    default = os.environ.get("COVERAGE_FILE", ".coverage")
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", default=default)
    parser.add_argument("-o", "--output", default=default)
    parser.add_argument("--log-level", default="warning")
    return parser.parse_args(args)


def main():
    ns = parse_args(sys.argv[1:])
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG
    }
    level = levels.get(ns.log_level.lower())
    if level is None:
        raise ValueError(
            f"log level given: {ns.log_level}"
            f" -- must be one of: {' | '.join(levels.keys())}")
    logging.basicConfig(level=level)
    with tempfile.TemporaryDirectory() as tmp:
        cov_file = os.path.join(tmp, "coverage")
        shutil.copy(ns.input, cov_file)

        c = get_cursor(cov_file)
        schema = get_schema(c)
        
        logger.info("Input file had schema level %s", schema)

        if SCHEMATA_META[schema](c):

            logger.info("Filtering arcs")

            SCHEMATA_ARC[schema](c)

        else:

            logger.info("Filtering lines")

            SCHEMATA_LINE[schema](c)

        c.connection.commit()
        c.connection.close()
        
        shutil.copy(cov_file, ns.output)
