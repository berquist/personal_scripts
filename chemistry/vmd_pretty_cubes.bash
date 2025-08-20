#!/usr/bin/env bash
# Original script by Felix Plasser (http://www.chemical-quantum-images.blogspot.de)
# Modified by Jan-Michael Mewes (http://workadayqc.blogspot.de)
#
# 0. $pointval mo 65-74 (Turbomole), plots (QChem), ...
# 1. call this script (choose 2 or 3 surfaces)
# 2. open the molecular structure file in VMD
# 3. load the .plt/.cube files and some settings
#    - "Load state" load_all_plt.vmd
#    - click "Apply" in "Graphical Representations"
# 4. adjust perspective
# 5. "Load state" plot_all.vmd (play plot_all.vmd)
# 6. Run convert.bash script to convert to PNG if desired

# RB note:
# Steps 2 and 3 can also be performed by launching vmd from the shell like this: vmd file.xyz -e load_all_plt.vmd
# Step 6: convert.bash script requires Imagemagick convert utility. For Mac OS X: install e.g. through Macports(http://www.macports.org): sudo port install imagemagick

###
ifmt=cube
ofmt=tga
out=load_all_plt.vmd
plot=plot_all.vmd
conv=convert.bash
html=vmd_plots.html
ncol=4
###

echo 'USAGE: $0 [<2 or 3 surfaces, STD = 3 >] [<highest iso, STD(2/3) = (0.1/0.128)>]'

isotemp=$2

if [ $1 -eq 2 ]; then
    isov=${isotemp:=0.01}
    isov2=$(echo $isov'/8' | bc -l)
    isov3=0.99
    #isovalue of 0.99 will produce no surface
    echo 'Using 2 surfaces for isovalues:'
    echo $isov $isov2
    echo "material change opacity Glass3 0.150000" > $out
    echo "material change diffuse Glass3 0.10000" >> $out
elif [ $1 -eq 3 ]; then
    isov=${isotemp:=0.0128}
    isov2=$(echo $isov'/4' | bc -l)
    isov3=$(echo $isov'/16' | bc -l)
    echo 'Using 3 surfaces for isovalues:'
    echo $isov $isov2 $isov3
    echo "material change opacity Glass3 0.400000" > $out
else
    echo "Please enter 2 or 3 for # of surfaces!"
    echo "Falling back to 3 surfaces with standard values"
    isov=0.0128
    isov2=0.0032
    isov3=0.0008
    echo "Using standard isovalues: "
    echo "Values: "$isov $isov2 $isov3
    echo "material change opacity Glass3 0.400000" > $out
fi

echo "axes location Off" >> $out
echo "display projection Orthographic" >> $out
echo "display rendermode GLSL" >> $out
echo "display depthcue off" >> $out
echo "color Display Background white" >> $out
echo "menu graphics on" >> $out
echo "material change diffuse Ghost 0.000000" >> $out
echo "material change ambient Ghost 0.300000" >> $out
echo "material change opacity Ghost 0.100000" >> $out
echo "material change shininess Ghost 0.000000" >> $out
echo "mol addrep 0" >> $out
echo "mol addrep 0" >> $out
echo "mol addrep 0" >> $out
echo "mol addrep 0" >> $out
echo "mol addrep 0" >> $out
echo "mol addrep 0" >> $out
echo "mol modmaterial 1 0 Opaque" >> $out
echo "mol modmaterial 2 0 Opaque" >> $out
echo "mol modmaterial 3 0 Glass3" >> $out
echo "mol modmaterial 4 0 Glass3" >> $out
echo "mol modmaterial 5 0 Ghost" >> $out
echo "mol modmaterial 6 0 Ghost" >> $out
echo "mol modstyle 1 0 Isosurface  $isov 0 0 0 1 1" >> $out
echo "mol modstyle 2 0 Isosurface -$isov 0 0 0 1 1" >> $out
echo "mol modstyle 3 0 Isosurface  $isov2 0 0 0 1 1" >> $out
echo "mol modstyle 4 0 Isosurface -$isov2 0 0 0 1 1" >> $out
echo "mol modstyle 5 0 Isosurface  $isov3 0 0 0 1 1" >> $out
echo "mol modstyle 6 0 Isosurface -$isov3 0 0 0 1 1" >> $out
echo "mol modcolor 1 0 ColorID 0" >> $out
echo "mol modcolor 2 0 ColorID 1" >> $out
echo "mol modcolor 3 0 ColorID 0" >> $out
echo "mol modcolor 4 0 ColorID 1" >> $out
echo "mol modcolor 5 0 ColorID 0" >> $out
echo "mol modcolor 6 0 ColorID 1" >> $out
echo "" > $plot

echo "#!/usr/bin/env bash" > $conv
chmod +x $conv

echo -e "<html>\n<head></head>\n<body>" > $html
echo -e "<table>\n<tr>" >> $html

N=0
for I in *$ifmt; do
    echo "mol addfile $I" >> $out
    echo "mol modstyle 1 0 Isosurface  $isov $N 0 0 1 1" >> $plot
    echo "mol modstyle 2 0 Isosurface -$isov $N 0 0 1 1" >> $plot
    echo "mol modstyle 3 0 Isosurface  $isov2 $N 0 0 1 1" >> $plot
    echo "mol modstyle 4 0 Isosurface -$isov2 $N 0 0 1 1" >> $plot
    echo "mol modstyle 5 0 Isosurface  $isov3 $N 0 0 1 1" >> $plot
    echo "mol modstyle 6 0 Isosurface -$isov3 $N 0 0 1 1" >> $plot
    echo "render TachyonInternal $I.$ofmt" >> $plot

    echo "convert $I.$ofmt $I.png" >> $conv
    echo "rm $I.$ofmt" >> $conv

    echo "<td><img src=\"$I.png\" border=\"1\" width=\"400\">" >> $html
    echo "$I<br></td>" >> $html

    N=$(($N + 1))

    if [ $((N % $ncol)) -eq 0 ]; then
        echo "</tr><tr>" >> $html
    fi
done

echo -e "</tr></table>" >> $html
echo -e "</body>\n</html>" >> $html

echo "... finished."
