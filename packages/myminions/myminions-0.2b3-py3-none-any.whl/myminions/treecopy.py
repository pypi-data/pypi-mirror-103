# -*- coding: utf-8 -*-
from docopt import docopt
import os
import fnmatch
import shutil
import sys
from pathlib import Path
from typing import Generator, List, Tuple, Optional
from myminions import APath

LEVELDROP_ITEM_DELIMITER = ","


__all__ = ["copy_filepairs"]


def filter_next_file(
    source_path: APath, filter_pattern: str
) -> Generator[str, None, None]:
    """
    Examples:
        >>> for python_file in filter_next_file("./", "*.py"):
        ...     print(python_file.name)
        __init__.py
        treecopy.py
        minions.py
        __main__.py

    Args:
        source_path:
        filter_pattern:

    Returns:

    """
    for rootpath, foldernames, filenames in os.walk(source_path):
        for filename in filenames:
            filepath = Path(rootpath, filename)
            if filepath.match(filter_pattern):
                yield filepath


def prepare_file_pairs(
    source_path, destination_path, filter_pattern, drop_level_slice=None
):
    """
    Examples:
        >>> prepare_file_pairs("./", "./test", ".py")


    Args:
        source_path: 
        destination_path: 
        filter_pattern: 
        drop_level_slice: 

    Returns:

    """
    if drop_level_slice is None:
        drop_level_slice = slice(None, None, None)
    source_path = Path(source_path)
    sourcepathlen = len(source_path.parts)
    pullpairs = list()
    for sourcefilepath in filter_next_file(source_path, filter_pattern):
        sourcefile_parentpath = sourcefilepath.parent
        subpath = Path(*sourcefile_parentpath.parts[sourcepathlen:])
        subpath_parts = subpath.parts[drop_level_slice]
        destinationfilepath = Path(
            destination_path, *subpath_parts, sourcefilepath.name
        )
        pullpairs.append((sourcefilepath, destinationfilepath))
    return pullpairs


def dryrun(filepairs, count):
    foundcount = len(filepairs)
    message1 = "Item {} of {}"
    message2 = "    From {}"
    message3 = "      to {}"
    for index, pair in enumerate(filepairs[:count]):
        sourcefilepath, destfilepath = pair
        print(message1.format(index + 1, foundcount))
        print(message2.format(sourcefilepath))
        print(message3.format(destfilepath))


def ignore_existing_destinations(filepairs):
    filepairs_without_existing_destinations = []
    for sourcefilepath, destinationfilepath in filepairs:
        if destinationfilepath.exists():
            continue
        filepairs_without_existing_destinations.append(
            (sourcefilepath, destinationfilepath)
        )
    return filepairs_without_existing_destinations


def copy_filepairs(filepairs: List[Tuple[Path, Path]]):
    foundcount = len(filepairs)
    message = "Pulling {} of {}, {}"
    for index, pair in enumerate(filepairs):
        sourcefilepath, destfilepath = pair
        destfilepath.parent.mkdir(parents=True, exist_ok=True)
        sys.stdout.write("\r" + message.format(index + 1, foundcount, sourcefilepath))
        shutil.copy(str(sourcefilepath), str(destfilepath))
    print(". Finished pulling.")


def droppath(path, level):
    if level == 0:
        return path
    result = path
    for drop in range(level):
        result, pathname = os.path.split(result)
    return result


def convert_leveldrop_parameter_to_numbers(
    leveldrop_parameter: str,
) -> List[Optional[int]]:
    if leveldrop_parameter is None:
        return None
    if LEVELDROP_ITEM_DELIMITER not in leveldrop_parameter:
        single_leveldrop_value = int(leveldrop_parameter)
        return [single_leveldrop_value]
    numbers_as_str = leveldrop_parameter.split(LEVELDROP_ITEM_DELIMITER)
    numbers = [int(number_as_str) for number_as_str in numbers_as_str]
    return numbers


def convert_leveldrop_numbers_to_slice(leveldrop_numbers: List[int]) -> slice:
    if leveldrop_numbers is None:
        return slice(None, None, None)
    shall_simply_drop_end_of_subpath = (
        len(leveldrop_numbers) == 1 and leveldrop_numbers[0] < 0
    )
    if shall_simply_drop_end_of_subpath:
        drop_count = leveldrop_numbers[0]
        return slice(None, drop_count, None)

    shall_simply_drop_start_of_subpath = (
        len(leveldrop_numbers) == 1 and leveldrop_numbers[0] > 0
    )
    if shall_simply_drop_start_of_subpath:
        drop_count = leveldrop_numbers[0]
        return slice(drop_count, None, None)

    shall_simply_drop_part_of_subpath = len(leveldrop_numbers) == 2
    if shall_simply_drop_part_of_subpath:
        start = leveldrop_numbers[0]
        end = leveldrop_numbers[1]
        invalid_order = start > end
        return slice(start, end, None)


def copy_tree(
    source_path: APath, destination_path: APath, file_pattern: str, level_drop: int = 0
):
    arguments = docopt(__doc__, options_first=True, version="0.0.0a1")
    source_path = Path(source_path)
    destination_path = Path(destination_path)
    if not source_path.exists():
        raise FileExistsError("Sourcepath '{}' does not exists".format(source_path))
    targetrootpath = Path(destination_path.drive)
    if not targetrootpath.exists():
        raise FileExistsError(
            "Targetrootpath '{}' does not exists".format(targetrootpath)
        )
    leveldrop_numbers = convert_leveldrop_parameter_to_numbers(level_drop)
    leveldrop_slice = convert_leveldrop_numbers_to_slice(leveldrop_numbers)
    # if arguments["move"]:
    #     success = move(sourcepath, targetpath, filepattern, leveldrop)
    #     return success
    filepairs = prepare_file_pairs(
        source_path, destination_path, file_pattern, leveldrop_slice
    )
    filepairs = ignore_existing_destinations(filepairs)

    if arguments["dry"]:
        dryrun(filepairs, 5)
    elif arguments["copy"]:
        copy_filepairs(filepairs)
