import logging
from pathlib import Path

import numpy as np
import pandas as pd


logging.basicConfig(level=logging.DEBUG)


def remove_nan(s):
    try:
        s.remove(np.nan)
    except KeyError:
        pass
    return s


def print_set_differences(a, b):
    logging.debug(f"a = {len(a)}")
    logging.debug(f"b = {len(b)}")
    a_minus_b = a - b
    b_minus_a = b - a
    logging.debug(f"a - b = {len(a_minus_b)}")
    logging.debug(f"b - a = {len(b_minus_a)}")
    # Inspect a few
    if len(a_minus_b) > 0:
        logging.debug(sorted(a_minus_b)[:5])
    if len(b_minus_a) > 0:
        logging.debug(sorted(b_minus_a)[:5])
    return


def is_from_twitter(child_id, parent_children_df):
    mask = parent_children_df.loc[:, "child_uid"] == child_id
    if mask.any():
        status_in_corpus = parent_children_df[mask].loc[:, "status_in_corpus"].iloc[0]
        return status_in_corpus == "diy"
    return False


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("--inner-files-sources", type=Path)
    arg("uid_info", type=Path)
    arg("parent_children", type=Path)
    arg("allzip_uids_types", type=Path)
    args = parser.parse_args()

    if "uid_info.tab" not in args.uid_info.name:
        raise RuntimeError
    if "parent_children.tab" not in args.parent_children.name:
        raise RuntimeError
    if "allzip_uids_types.tab" not in args.allzip_uids_types.name:
        raise RuntimeError

    uid_info = pd.read_csv(str(args.uid_info), sep="\t")
    parent_children = pd.read_csv(str(args.parent_children), sep="\t")
    allzip_uids_types = pd.read_csv(str(args.allzip_uids_types), sep="\t", header=None)

    uids_uid_info = remove_nan(set(uid_info.loc[:, "uid"]))
    derived_uids_uid_info = remove_nan(set(uid_info.loc[:, "derived_uid"]))
    child_sources_parent_children = remove_nan(set(parent_children.loc[:, "child_uid"]))
    parent_sources_parent_children = remove_nan(set(parent_children.loc[:, "parent_uid"]))
    # "child_asset_type" may also be important
    sources_allzip_uids_types = remove_nan(set(allzip_uids_types.iloc[:, 0]))

    print_set_differences(derived_uids_uid_info, child_sources_parent_children)
    try:
        assert derived_uids_uid_info.issubset(child_sources_parent_children)
    except AssertionError:
        logging.error("There are child IDs in `uid_info.tab` that aren't in `parent_children.tab`!")
    try:
        assert child_sources_parent_children.issubset(derived_uids_uid_info)
    except AssertionError:
        logging.info("There are child IDs in `parent_children.tab` that aren't in `uid_info.tab`! This is ok.")

    assert uids_uid_info == parent_sources_parent_children

    # Parents:n
    # - uid (uids_uid_info)
    # - parent_uid (parent_sources_parent_children)
    # Children:
    # - derived_uid (derived_uids_uid_info)
    # - child_uid (child_sources_parent_children)
    # - first column of allzip_uids_types.tab (sources_allzip_uids_types)
    # - [inner_files_sources]

    # The overlap (intersection) of parents and children should be zero:
    parent_child_intersection = parent_sources_parent_children & child_sources_parent_children
    assert len(parent_child_intersection) == 0
    # The overlap (intersection) of uids and derived uids should be zero
    uid_derived_intersection = uids_uid_info & derived_uids_uid_info
    assert len(uid_derived_intersection) == 0

    # The mapping from uid to type corresponds to child documents and also
    # shouldn't overlap with parent documents
    assert len(sources_allzip_uids_types & parent_sources_parent_children) == 0
    assert len(sources_allzip_uids_types & uids_uid_info) == 0

    if args.inner_files_sources:
        with open(str(args.inner_files_sources)) as handle:
            inner_file_sources = set(line.strip() for line in handle.readlines())
        logging.debug("inner zip file sources")

        # Inner files correspond to child documents so shouldn't overlap with
        # parents
        assert len(inner_file_sources & uids_uid_info) == 0
        assert len(inner_file_sources & parent_sources_parent_children) == 0

        if not inner_file_sources.issubset(derived_uids_uid_info):
            # This is ok if they're not HTML stuff.
            logging.info("There are original sources that aren't children in `uid_info.tab`! This is ok.")
            # child_ids = inner_file_sources - derived_uids_uid_info
            # for child_id in child_ids:
            #     mask = allzip_uids_types.iloc[:, 0] == child_id
            #     file_type = allzip_uids_types[mask].iloc[0, 1]
            #     print(child_id, file_type)
        if not derived_uids_uid_info.issubset(inner_file_sources):
            # This might be Twitter data, check, in which case it's ok because
            # that couldn't be distributed.
            child_ids = derived_uids_uid_info - inner_file_sources
            for child_id in child_ids:
                if not is_from_twitter(child_id, parent_children):
                    logging.error("There are children in `uid_info.tab` that aren't in original sources!")
                    break

        # print("print_set_differences(inner_file_sources, child_sources_parent_children)")
        # print_set_differences(inner_file_sources, child_sources_parent_children)
        if not inner_file_sources.issubset(child_sources_parent_children):
            logging.info("There are original sources that aren't children in `parent_children.tab`!")
        if not child_sources_parent_children.issubset(inner_file_sources):
            child_ids = child_sources_parent_children - inner_file_sources
            for child_id in child_ids:
                if not is_from_twitter(child_id, parent_children):
                    logging.error("There are children in `parent_children.tab` that aren't in original sources!")
                    break

        # Every mapping from source ID to its file extension corresponds to an
        # original source file and every original source file has a mapping
        # from its ID to its file extension.
        try:
            assert inner_file_sources == sources_allzip_uids_types
        except AssertionError:
            print("print_set_differences(inner_file_sources, sources_allzip_uids_types)")
            print_set_differences(inner_file_sources, sources_allzip_uids_types)
            if not inner_file_sources.issubset(sources_allzip_uids_types):
                print("There are original sources that aren't in the mapping!")
            if not sources_allzip_uids_types.issubset(inner_file_sources):
                print("There are entries in the mapping that aren't in the sources!")
