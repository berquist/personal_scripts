from flexnlp import Document
from flexnlp.model import antecedent


def getargs():
    import argparse
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("filename", nargs="*")
    return parser.parse_args()


if __name__ == "__main__":

    args = getargs()

    docs = dict()

    for filename in args.filename:

        with open(filename, "rb") as pickle_file:
            doc = Document.from_pickle_file(pickle_file)

        amt = doc.theory(antecedent.MentionAntecedentTheory)
        for ms in amt.mentions_scored:
            print('-' * 70)
            print(amt.antecedent_scores(ms))

        docs[doc] = amt
