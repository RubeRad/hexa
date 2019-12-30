#! /bin/sh

hexaflexagon.py --cfg tri.cfg   --out ex_num_tri.png   0.png 1.png 2.png
hexaflexagon.py --cfg trif1.cfg --out ex_num_trif1.png 0.png 1.png 2.png
hexaflexagon.py --cfg trif2.cfg --out ex_num_trif2.png 0.png 1.png 2.png
hexaflexagon.py --cfg trif3.cfg --out ex_num_trif3.png 0.png 1.png 2.png
hexaflexagon.py --cfg trif4.cfg --out ex_num_trif4.png 0.png 1.png 2.png
hexaflexagon.py --cfg trif5.cfg --out ex_num_trif5.png 0.png 1.png 2.png
hexaflexagon.py --cfg hex.cfg   --out ex_num_hex.png   0.png 1.png 2.png 3.png 4.png 5.png

trainers.py -q
hexaflexagon.py --cfg tri.cfg   --out ex_col_tri.png   0red.png 1ylw.png 2blu.png
hexaflexagon.py --cfg trif1.cfg --out ex_col_trif1.png 0red.png 1ylw.png 2blu.png
hexaflexagon.py --cfg trif2.cfg --out ex_col_trif2.png 0red.png 1ylw.png 2blu.png
hexaflexagon.py --cfg trif3.cfg --out ex_col_trif3.png 0red.png 1ylw.png 2blu.png
hexaflexagon.py --cfg trif4.cfg --out ex_col_trif4.png 0red.png 1ylw.png 2blu.png
hexaflexagon.py --cfg trif5.cfg --out ex_col_trif5.png 0red.png 1ylw.png 2blu.png
hexaflexagon.py --cfg hex.cfg   --out ex_col_hex.png   0red.png 1ylw.png 2blu.png 3ppl.png 4org.png 5grn.png

