from collections import Counter

from vistautils.iter_utils import windowed


def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("transcripts", nargs="*")
    arg("--lexicon-words")
    return parser.parse_args()


def main() -> None:
    args = getargs()
    with open(args.lexicon_words) as lexicon_file:
        lexicon = set(lexicon_file.readlines())
    for transcript_filename in args.transcripts:
        transcript = list()
        compound_candidates = dict()
        with open(transcript_filename) as transcript_file:
            for utterance in transcript_file:
                utterance_id, *tokens = utterance.split()
                tokens = list(filter(lambda token: token[0] not in ("!", "<"), tokens))
                # crude starting point:
                #
                # 1. look for a word `i` of length 2, join it to the next word
                # `j`, then create a mapping (`i`, `j`) -> `ij`. This is the
                # part that is naive; it doesn't consider what the next word
                # is.
                #
                # 2. flatten all words from the text
                #
                # For each element in the mapping, create frequencies for
                #
                # 3. how many times (`i`, `j`) occurs in the original text
                #
                # 4. how many times `ij` occurs in the original text
                transcript.extend(tokens)
                for window in windowed(tokens, 2):
                    if len(window[0]) == 2:
                        compound_candidates[window] = ''.join(window)
        transcript_frequencies = Counter(transcript)
        for separate, combined in compound_candidates.items():
            if combined in lexicon:
                print(separate, transcript_frequencies[separate[0]], transcript_frequencies[separate[1]], combined, transcript_frequencies[combined])
            else:
                print(f"{combined} is not in the lexicon")
    return


if __name__ == "__main__":
    main()
