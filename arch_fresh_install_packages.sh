#!/bin/bash

### Keep track of my preferred packages and install them on a fresh
### Arch instance.

# sudo pacman -Syyu

packages=(
    # low-level
    abs
    base
    base-devel
    compton
    cuda
    gcc-fortran
    gdb
    lib32-glibc
    lib32-libstdc++5
    libcl
    libclc
    libcl-headers
    libstdc++5
    nvidia
    nvidia-libgl
    valgrind

    # groups
    xfce4
    texlive-most

    # command-line tools and general libraries
    ack
    arb
    arrayfire
    aspell
    aspell-en
    atool
    blas
    boost
    boost-libs
    cblas
    cmake
    colordiff
    cpio
    cronie
    ctags
    diffoscope
    dos2unix
    # eigen
    eigen2
    freeimage
    git
    gnuplot
    grace
    gsl
    hdf5
    hub
    keybase
    keychain
    htop
    iotop
    languagetool
    lapack
    lesspipe
    lftp
    lsb-release
    markdown
    mercurial
    mlocate
    mosh
    mpdecimal
    namcap
    netcdf
    netcdf-fortran
    openbabel
    openmpi
    openssh
    parallel
    perl-term-readkey # git-svn
    rlwrap
    swig
    tcsh
    # tmux
    tree
    unrar
    wget
    xsel
    xclip
    zsh

    # fonts
    cowsay
    figlet
    ttf-inconsolata
    ttf-sazanami

    # programming: C/C++
    clang
    clang-analyzer
    gdb

    # programming: Julia
    julia
    julia-docs

    # programming: Ruby
    ruby

    # programming: Lua
    lua51

    # programming: Python
    # If something is commented out here, then it's probably a split
    # package.
    cython
    cython2
    ipython
    ipython2
    ipython-notebook
    ipython2-notebook
    pygmentize
    pypy
    pypy3
    python
    python2
    python-bottleneck
    python2-bottleneck
    python-docopt
    python2-docopt
    flake8
    python2-flake8
    python-gmpy2
    python2-gmpy2
    python-h5py
    python2-h5py
    python-joblib
    python2-joblib
    python-matplotlib
    python2-matplotlib
    python-mpmath
    python2-mpmath
    python-nose
    python2-nose
    python-numexpr
    python2-numexpr
    python-numpy
    python2-numpy
    python-openbabel
    python2-openbabel
    python-opengl
    python2-opengl
    python-openpyxl
    python2-openpyxl
    python-pandas
    python2-pandas
    python-periodictable
    # python-periodictable
    python-pillow
    python2-pillow
    python-pint
    python2-pint
    python-pip
    python2-pip
    python-pycuda
    python2-pycuda
    python-pylint
    python2-pylint
    python-pyqt4
    python2-pyqt4
    python-pyqt5
    python2-pyqt5
    python-pytables
    python2-pytables
    python-scikit-learn
    python-scipy
    python2-scipy
    python-sh
    python2-sh
    python-sphinx
    python2-sphinx
    python-statsmodels
    python2-statsmodels
    python-sympy
    python2-sympy
    python-terminado
    python2-terminado
    python-virtualenv
    python2-virtualenv
    python-virtualenvwrapper
    # python2-virtualenvwrapper
    python-xlrd
    python2-xlrd
    python-xlsxwriter
    python2-xlsxwriter
    python-xlwt
    python2-xlwt
    jupyter-nbconvert

    # editors
    emacs
    gvim
    neovim
    python-neovim
    python2-neovim

    # GUI-based
    leafpad
    firefox
    thunderbird
    pymol
    transmission
    ristretto
    gnome-system-monitor
    thunar-archive-plugin
    gimp
    meld
)

for package in ${packages[@]}; do
    sudo pacman -S ${package}
done

# sudo abs

# echo "[archlinuxfr]
# SigLevel = Never
# Server = http://repo.archlinux.fr/$arch
# " >> /etc/pacman.conf

# sudo pacman -Syyu

# sudo pacman -S yaourt

packages=(
    avogadro-git
    dropbox
    fftw2
    figlet-fonts
    haguichi
    libgfortran6
    logmein-hamachi
    lzip
    modules
    molden
    multimarkdown
    pandoc-bin
    pelican
    swig2
    symlinks
    tmux-git
    ttf-ms-fonts

    # command-line simple tools
    checkbashisms
    pipman-git

    # Programming: Fortran
    ftnchek

    # Programming: C++
    # armadillo
    blitz

    # Programming: Ruby
    gist
    travis-lint

    # Programming: Python
    mypy-git
    python-ase
    # python2-ase
    python-llvmlite
    python2-llvmlite
    python-memory_profiler
    python-numba
    python2-numba
    python-proselint
    python-pythonpy
    python-seaborn
    python2-seaborn
    python-unp
    snakemake
)

# for package in ${packages[@]}; do
#     yaourt -S ${package}
# done

## The following packages should't use yaourt:
# mathematica
# vmd

# What to do about these?
# udisks2 dosfstools
