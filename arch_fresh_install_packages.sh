#!/bin/bash

### Keep track of my preferred Arch Linux packages.

packages_default=(
    # low-level
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
    pbzip2
    perl-term-readkey # git-svn
    reflector
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
    ipython
    jupyter-notebook
    pygmentize
    pypy3
    python
    python-bottleneck
    python-docopt
    flake8
    python-gmpy2
    python-h5py
    python-joblib
    python-matplotlib
    python-mdanalysis
    python-mpmath
    python-nose
    python-numexpr
    python-numpy
    python-openbabel
    python-opengl
    python-openpyxl
    python-pandas
    python-periodictable
    python-pillow
    python-pint
    python-pip
    python-pycuda
    python-pylint
    python-pyqt4
    python-pyqt5
    python-pytables
    python-scikit-learn
    python-scipy
    python-sh
    python-sphinx
    python-statsmodels
    python-sympy
    python-terminado
    python-virtualenv
    python-virtualenvwrapper
    python-xlrd
    python-xlsxwriter
    python-xlwt
    jupyter-nbconvert
    autopep8
    yapf

    # editors
    emacs

    # GUI-based
    jmol
    firefox
    pymol
    transmission
    ristretto
    gnome-system-monitor
    thunar-archive-plugin
    gimp
    meld
)

packages_aur=(
    avogadro-git
    discord-canary
    dropbox
    fftw2
    figlet-fonts
    git-lfs
    haguichi
    libgfortran6
    lmod
    logmein-hamachi
    lzip
    molden
    multimarkdown
    pandoc-bin
    slack-desktop
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
    armadillo
    blitz

    # Programming: Ruby
    gist
    ruby-mdl
    travis-lint

    # Programming: Python
    mypy-git
    proselint
    python-ase
    python-llvmlite
    python-memory_profiler
    python-numba
    python-proselint
    python-pythonpy
    python-seaborn
    python-unp
    snakemake
    yamllint
)
