#!/usr/bin/env bash

# Prepare a PDB file for amber by only leaving ATOM, HETATM, TER, and END cards.
# All other lines get deleted.

sed '/^HEADER/d' $1 > $2
sed -i '/^TITLE /d' $2
sed -i '/^COMPND/d' $2
sed -i '/^KEYWDS/d' $2
sed -i '/^EXPDTA/d' $2
sed -i '/^AUTHOR/d' $2
sed -i '/^REVDAT/d' $2
sed -i '/^JRNL  /d' $2
sed -i '/^REMARK/d' $2
sed -i '/^DBREF /d' $2
sed -i '/^SEQRES/d' $2
sed -i '/^HET   /d' $2
sed -i '/^HETNAM/d' $2
sed -i '/^FORMUL/d' $2
sed -i '/^HELIX /d' $2
sed -i '/^SHEET /d' $2
sed -i '/^LINK  /d' $2
sed -i '/^SITE  /d' $2
sed -i '/^ORIG/d' $2
sed -i '/^SCALE/d' $2
sed -i '/^CRYST/d' $2
sed -i '/^ANISOU/d' $2
sed -i '/^CONECT/d' $2
sed -i '/^MASTER/d' $2
sed -i '/^SOURCE/d' $2
