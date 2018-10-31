#!/usr/bin/env bash

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

    # programming: C/C++
    clang
    clang-analyzer
    gdb

    # programming: Julia
    julia
    julia-docs

    # programming: JVM
    kotlin
    scala

    # programming: Lisp
    chicken
    clisp
    cmucl
    mit-scheme
    racket
    # racket-docs
    sbcl

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
    python-mccabe
    python-mdanalysis
    # apparently there are problems with 3.x
    python2-mdanalysis
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
    python-pycodestyle
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

    # programming: Ruby
    ruby

    # fonts
    cowsay
    figlet
    ttf-inconsolata
    ttf-sazanami

    # editors
    emacs

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
    cppcheck
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
    keybase-gui
    keychain
    htop
    iotop
    jq
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
    pacman-contrib
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

    # GUI-based
    firefox
    gimp
    gnome-system-monitor
    jmol
    meld
    pymol
    ristretto
    thunar-archive-plugin
    transmission
)

packages_aur=(

    # Programming: C++
    armadillo
    blitz
    cpplint
    pgi-compilers

    # Programming: Fortran
    ftnchek

    # Programming: JVM
    ktlint

    # Programming: Lisp
    chez-scheme-git
    chibi-scheme-git
    hy-git
    roswell

    # Programming: Python
    doc8
    mypy-git
    proselint
    python-ase
    python-black
    python-deepdiff
    python-hypothesis
    python-pyfiglet
    python-language-server
    python-llvmlite
    python-memory_profiler
    python-numba
    python-proselint
    python-pythonpy
    python-seaborn
    python-unp
    python-versioneer
    snakemake
    yamllint

    # Programming: Ruby
    gist
    ruby-mdl
    travis-lint

    # command-line simple tools
    bash-language-server
    checkbashisms
    pipman-git
    zerotier-one

    # GUI tools
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
    shellcheck-static
    slack-desktop
    swig2
    symlinks
    tmux-git
    ttf-ms-fonts
    visual-studio-code-bin
    yay
)
