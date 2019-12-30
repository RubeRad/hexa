# hexa
Print templates for trihexaflexagons, hexahexaflexagons, etc

Your python3 needs opencv-python (which in turn uses numpy).

If everything is set up right, then examples.sh should create some
useful examples, and the commands in there should give you basically
an idea how to use it.

The first example you should probably start with is ex_num_tri.png or
ex_col_tri.png. Make sure when printing that the aspect is not messed
up -- the triangles must remain equilateral! After printing, cut out,
and pre-crease every line so it can easily fold both ways.

ex_num_trif?.png (produced using trif?.cfg) are not for printing (or
at least not for folding); those constitute a folding tutorial showing
what ex_num_tri.png should look like after fold 1, fold 2, ... fold
5. Every fold is behind/away (origami 'mountain') not towards you
(origami 'valley'). f4 is a 'flip through'. f5 should put the two
blank triangles face to face, then glue-stick them together.

ex_col_tri.png is the same deal, but with colored images (generated by
trainers.py) instead of numbers. The tri version uses the 3 primary
colors red ylw blu. Folding according to the instructions assembles
the red face. If you flex red by pinching the yellow dots and
unfolding from the middle, you get to yellow. Then blue dots gets you
to blue, then red dots gets you to back to red.

The hexahexaflexagons are necessarily more difficult. If you print
ex_col_hex.png, after cutting out and creasing all lines, first you
fold the strip in half (like trif1.cfg), then 'roll' it together by
folding adjacent greens together, then adjacent purples together,
etc. At that point you should have a flattened tube of paper that
looks just like ex_col_f1.png, and you continue from there the same
way.

When assembled, each primary (red/ylw/blu) face has two flexing
possibilities, from red you can take a primary flex to get to yellow
(as before), or a new secondary flex to get to orange (which is the
color 'between' red and yellow). From orange you can only flex back to
red. Etc.

When you're ready to create templates using your own photos/images,
you can use hexacrop.py to make same-size square images (default
1000x1000) that crop your subject nicely (for instance you probably
don't want triangles to chop eyesballs in half). `hexacrop.py
yourimg.jpg' will raise a window with your image and a six-triangled
hexagon on it. You can use wasd keys to pan the hexagon around, and
,. to shrink/expand. When you're happy with how your crop will be
chopped into triangles, c will save out the crop and quit.
