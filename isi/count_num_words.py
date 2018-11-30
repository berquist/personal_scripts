#!/usr/bin/env python

def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("transcripts", nargs='*')
    return parser.parse_args()


def main():
    args = getargs()
    for transcript_filename in args.transcripts:
        num_words = 0
        with open(transcript_filename) as transcript_file:
            for line in transcript_file:
                num_words += len(line.split()[1:])
        print(num_words, transcript_filename)
    return


if __name__ == "__main__":
    main()
