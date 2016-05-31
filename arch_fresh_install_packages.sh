#!/usr/bin/env bash

### Keep track of my preferred packages and install them on a fresh
### Arch instance.

# sudo pacman -Syyu

packages=(
    # low-level
    base
    base-devel
    gcc-fortran
    gdb
    valgrind
    nvidia
    cuda
    nvidia-libgl
    libcl
    libclc
    libcl-headers
    lib32-glibc
    libstdc++5
    lib32-libstdc++5
    abs

    # groups
    xfce4
    texlive-most

    # command-line tools and general libraries
    mpdecimal
    tcsh
    zsh
    unrar
    htop
    lsb-release
    openssh
    mosh
    wget
    keychain
    # eigen
    eigen2
    git
    perl-term-readkey # git-svn
    mercurial
    ctags
    cmake
    blas
    lapack
    cblas
    hdf5
    netcdf
    netcdf-fortran
    grace
    openbabel
    openmpi
    boost
    boost-libs
    freeimage
    swig
    gsl
    iotop
    namcap
    xsel
    xclip
    dos2unix
    cronie
    markdown
    aspell
    aspell-en
    tmux
    gnuplot
    parallel
    arrayfire
    rlwrap
    ack
    colordiff
    lesspipe
    dos2unix
    atool

    # fonts
    ttf-inconsolata
    ttf-sazanami
    figlet
    cowsay

    # programming: C/C++
    gdb
    clang
    clang-analyzer

    # programming: Julia
    julia
    julia-docs

    # programming: Ruby
    ruby

    # programming: Lua
    lua51

    # programming: Python
    python
    python2
    pypy3
    pypy
    cython
    cython2
    python-numpy
    python2-numpy
    python-scipy
    python2-scipy
    python-openbabel
    python2-openbabel
    python-h5py
    python2-h5py
    ipython
    ipython2
    ipython-notebook
    ipython2-notebook
    python-terminado
    python2-terminado
    flake8
    python2-flake8
    python-pylint
    python2-pylint
    python-virtualenv
    python2-virtualenv
    python-virtualenvwrapper
    # python2-virtualenvwrapper
    python-pip
    python2-pip
    python-sphinx
    python2-sphinx
    python-numexpr
    python2-numexpr
    python-pytables
    python2-pytables
    python-pandas
    python2-pandas
    python-nose
    python2-nose
    python-bottleneck
    python2-bottleneck
    python-matplotlib
    python2-matplotlib
    python-statsmodels
    python2-statsmodels
    python-openpyxl
    python2-openpyxl
    python-xlsxwriter
    python2-xlsxwriter
    python-xlrd
    python2-xlrd
    python-xlwt
    python2-xlwt
    python-gmpy2
    python2-gmpy2
    python-mpmath
    python2-mpmath
    python-sympy
    python2-sympy
    python-docopt
    python2-docopt
    python-pyqt4
    python2-pyqt4
    python-pyqt5
    python2-pyqt5
    python-pillow
    python2-pillow
    python-opengl
    python2-opengl
    python-sh
    python2-sh
    pygmentize
    python-pycuda
    python2-pycuda

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
    logmein-hamachi
    modules
    molden
    multimarkdown
    pandoc-bin
    pelican
    swig2
    symlinks
    ttf-ms-fonts

    # command-line simple tools
    checkbashisms

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
    python-llvmlite
    python2-llvmlite
    python-numba
    python2-numba
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
