import logging
from pathlib import Path

import numpy as np
import pandas as pd


logging_fmt = "[%(asctime)s] [%(levelname)s] [%(lineno)s] %(message)s"
logging.basicConfig(format=logging_fmt, level=logging.DEBUG)


def peval(s):
    """Print something before evaluating it as a command."""
    logging.debug(s)
    eval(s)
    return


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
    n = 5
    if len(a_minus_b) > 0:
        logging.debug(sorted(a_minus_b)[:n])
    if len(b_minus_a) > 0:
        logging.debug(sorted(b_minus_a)[:n])
    return


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("uid_info", type=Path)
    arg("parent_children", type=Path)
    arg("allzip_uids_types", type=Path)
    arg("twitter_info", type=Path)
    arg("--inner-files-sources", type=Path, help="A list of IDs extracted from every inner corpus zip file.")
    args = parser.parse_args()

    if "uid_info.tab" not in args.uid_info.name:
        raise RuntimeError
    if "parent_children.tab" not in args.parent_children.name:
        raise RuntimeError
    if "allzip_uids_types.tab" not in args.allzip_uids_types.name:
        raise RuntimeError
    if "twitter_info.tab" not in args.twitter_info.name:
        raise RuntimeError

    # relation of root HTML assets to topics and language
    uid_info = pd.read_csv(str(args.uid_info), sep="\t")
    # relation of child assets to root HTML pages
    parent_children = pd.read_csv(str(args.parent_children), sep="\t")
    allzip_uids_types = pd.read_csv(str(args.allzip_uids_types), sep="\t", header=None)
    twitter_info = pd.read_csv(str(args.twitter_info), sep="\t")

    # All possible columns containing IDs.
    uids_uid_info = remove_nan(set(uid_info.loc[:, "uid"]))
    derived_uids_uid_info = remove_nan(set(uid_info.loc[:, "derived_uid"]))
    child_sources_parent_children = remove_nan(set(parent_children.loc[:, "child_uid"]))
    parent_sources_parent_children = remove_nan(set(parent_children.loc[:, "parent_uid"]))
    sources_allzip_uids_types = remove_nan(set(allzip_uids_types.iloc[:, 0]))
    twitter_uids = remove_nan(set(twitter_info.loc[:, "uid"]))

    #   <original_file_name>  <original_file_column_name> <variable_name>
    # Parents:
    # - uid_info.tab          uid         uids_uid_info
    # - parent_children.tab   parent_uid  parent_sources_parent_children
    # - twitter_info.tab      uid         twitter_uids
    # Children:
    # - uid_info.tab          derived_uid derived_uids_uid_info
    # - parent_children.tab   child_uid   child_sources_parent_children
    # - allzip_uids_types.tab [col 0]     sources_allzip_uids_types
    # - []                    []          inner_files_sources (optional)

    parent_sets = (
        uids_uid_info,
        parent_sources_parent_children,
        twitter_uids,        
    )
    child_sets = (
        derived_uids_uid_info,
        child_sources_parent_children,
        sources_allzip_uids_types,
    )

    # The overlap (intersection) of parents and children should be zero:
    for parent_set in parent_sets:
        for child_set in child_sets:
            assert len(parent_set & child_set) == 0

    # The two main sets of parent IDs must be identical.
    assert uids_uid_info == parent_sources_parent_children
    # Not every parent ID is from Twitter, but Twitter IDs must be a subset of
    # the others.
    assert twitter_uids.issubset(uids_uid_info)

    ## Consistency of child IDs

    peval("print_set_differences(derived_uids_uid_info, child_sources_parent_children)")
    try:
        assert derived_uids_uid_info.issubset(child_sources_parent_children)
    except AssertionError:
        logging.error("There are child IDs in `uid_info.tab` that aren't in `parent_children.tab`!")
    try:
        assert child_sources_parent_children.issubset(derived_uids_uid_info)
    except AssertionError:
        logging.info("There are child IDs in `parent_children.tab` that aren't in `uid_info.tab`! This is ok.")
        # TODO what is this correlated with?
        # child_ids = child_sources_parent_children - derived_uids_uid_info

    # Are there entries in parent_children.tab where status_in_corpus !=
    # present and the child ID is _not_ in twitter_info.tab?
    df_not_present_in_corpus = parent_children[parent_children.loc[:, "status_in_corpus"] != "present"]
    # child_uids_not_present_in_corpus = remove_nan(set(df_not_present_in_corpus.loc[:, "child_uid"]))
    parent_uids_not_present_in_corpus = remove_nan(set(df_not_present_in_corpus.loc[:, "parent_uid"]))
    assert parent_uids_not_present_in_corpus == twitter_uids

    # TODO sources_allzip_uids_types

    if args.inner_files_sources:
        with open(str(args.inner_files_sources)) as handle:
            inner_file_sources = set(line.strip() for line in handle.readlines())
        logging.debug("Comparing inner zip file IDs...")

        # Inner files correspond to child documents and shouldn't overlap with
        # parents
        for parent_set in parent_sets:
            assert len(parent_set & inner_file_sources) == 0

        peval("print_set_differences(inner_file_sources, derived_uids_uid_info)")
        if not inner_file_sources.issubset(derived_uids_uid_info):
            logging.info("There are original sources that aren't children in `uid_info.tab`! This is ok.")
            # TODO what is this correlated with?
            # child_ids = inner_file_sources - derived_uids_uid_info
        if not derived_uids_uid_info.issubset(inner_file_sources):
            # This might be Twitter data, in which case it's ok, because that
            # couldn't be distributed.
            child_ids = derived_uids_uid_info - inner_file_sources
            # These are child IDs, and twitter_info.tab corresponds to parent
            # IDs. However, there may also be child IDs that come from
            # Twitter.
            mask_uid_info = uid_info.loc[:, "derived_uid"].replace(np.nan, "").apply(lambda x: x in child_ids)
            child_ids_uid_info = uid_info[mask_uid_info]
            assert child_ids_uid_info.loc[:, "url"].apply(lambda url: "twitter.com" in url).all()
            try:
                assert len(child_ids.symmetric_difference(child_ids_uid_info.loc[:, "derived_uid"])) == 0
            except AssertionError:
                logging.error("There are children in `uid_info.tab` that aren't in original sources!")
            try:
                derived_uids = set(child_ids_uid_info.loc[:, "derived_uid"])
                mask_derived_uids = parent_children.loc[:, "child_uid"].apply(lambda x: x in derived_uids)
                assert set(parent_children[mask_derived_uids].loc[:, "status_in_corpus"]) == {"diy"}
            except AssertionError:
                logging.error("There are children in `uid_info.tab` that aren't in original sources!")            

        peval("print_set_differences(inner_file_sources, child_sources_parent_children)")
        if not inner_file_sources.issubset(child_sources_parent_children):
            logging.info("There are original sources that aren't children in `parent_children.tab`!")
        if not child_sources_parent_children.issubset(inner_file_sources):
            # Only Twitter data should be missing.
            child_ids = child_sources_parent_children - inner_file_sources
            # These are child IDs, and twitter_info.tab corresponds to parent
            # IDs. However, there may also be child IDs that come from
            # Twitter.
            mask_parent_children = parent_children.loc[:, "child_uid"].apply(lambda x: x in child_ids)
            child_ids_parent_children = parent_children[mask_parent_children]
            try:
                assert set(child_ids_parent_children.loc[:, "status_in_corpus"]) == {"diy"}
            except AssertionError:
                logging.error("There are children in `parent_children.tab` that aren't in original sources!")
            try:
                assert set(child_ids_parent_children.loc[:, "parent_uid"]).issubset(twitter_uids)
            except AssertionError:
                logging.error("There are children in `parent_children.tab` that aren't in original sources!")

        # Every mapping from source ID to its file extension corresponds to an
        # original source file and every original source file has a mapping
        # from its ID to its file extension. Twitter shouldn't be an issue
        # here.
        try:
            assert inner_file_sources == sources_allzip_uids_types
        except AssertionError:
            peval("print_set_differences(inner_file_sources, sources_allzip_uids_types)")
            if not inner_file_sources.issubset(sources_allzip_uids_types):
                logging.error("There are original sources that aren't in the mapping!")
            if not sources_allzip_uids_types.issubset(inner_file_sources):
                logging.error("There are entries in the mapping that aren't in the sources!")
