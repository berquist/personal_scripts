#!/usr/bin/env bash

### Keep track of my preferred Arch Linux packages.

packages_default=(
    # low-level
    arch-install-scripts
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
    # nvidia
    # nvidia-libgl
    nvidia-340xx
    opencl-nvidia-340xx
    opencl-headers
    valgrind

    # programming: C/C++
    clang
    clang-analyzer
    gdb

    # programming: Julia
    julia
    julia-docs

    # programming: JVM
    jdk8-openjdk
    jdk-openjdk
    openjdk8-src
    openjdk-src
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
    jupyter-notebook
    pygmentize
    pypy3
    python-black
    python-bottleneck
    python-cookiecutter
    python-docopt
    flake8
    python-gmpy2
    python-h5py
    python-hypothesis
    python-joblib
    python-matplotlib
    python-mccabe
    python-mdanalysis
    # apparently there are problems with 3.x
    python2-mdanalysis
    python2-mock
    python-mpmath
    python-networkx
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
    python-pydocstyle
    python-pylint
    python-pyqt4
    python-pyqt5
    python-pytables
    python-pytest-cov
    python-pytest-shutil
    python-rope
    python-scikit-learn
    python-scipy
    python-seaborn
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
    asp
    aspell
    aspell-en
    atool
    bash-language-server
    blas
    boost
    boost-libs
    cblas
    checkbashisms
    cmake
    colordiff
    cpio
    cppcheck
    cronie
    ctags
    devtools
    diffoscope
    docker
    dos2unix
    doxygen
    # eigen
    eigen2
    exa
    fd
    freeimage
    gist
    git
    git-lfs
    gnuplot
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
    lzip
    markdown
    mercurial
    mlocate
    mosh
    mpdecimal
    namcap
    netcdf
    netcdf-fortran
    obs-studio
    openbabel
    openmpi
    openssh
    pacman-contrib
    parallel
    pbzip2
    perl-term-readkey # git-svn
    pybind11
    python-language-server
    reflector
    rlwrap
    subversion
    swig
    tcsh
    # tmux
    tree
    unrar
    vlc
    wget
    xsel
    xclip
    zerotier-one
    zsh

    # GUI-based
    firefox
    firefox-developer-edition
    gimp
    gnome-system-monitor
    intellij-idea-community-edition
    jmol
    meld
    pycharm-community-edition
    pymol
    ristretto
    thunar-archive-plugin
    transmission-cli
    transmission-remote-gtk
)

packages_aur=(

    # Programming: C++
    armadillo
    blitz
    cpplint
    # pgi-compilers

    # Programming: Fortran
    fortran-language-server
    ftnchek

    # Programming: JVM
    kotlin-language-server
    ktlint

    # Programming: Lisp
    chez-scheme-git
    chibi-scheme-git
    hy-git
    roswell

    # Programming: Python
    # doc8
    mypy-git
    pjson
    proselint
    python-algopy
    python-ase
    python-deepdiff
    python-pyfiglet
    python-pylatex-git
    # python-llvmlite
    python-memory_profiler
    # python-numba
    python-ordered-set
    python-proselint
    python-pdbpp
    python-pythonpy
    # python-unp
    python-versioneer
    snakemake
    yamllint

    # Programming: Ruby
    ruby-mdl
    ruby-travis
    travis-lint

    # command-line tools
    grace
    multimarkdown
    pipman-git
    swig2
    watchman

    # GUI tools
    # avogadro-git
    discord-canary
    dropbox
    fftw2
    figlet-fonts
    haguichi
    # libgfortran6
    lmod
    logmein-hamachi
    # molden
    pandoc-bin
    shellcheck-static
    slack-desktop
    symlinks
    tmux-git
    ttf-ms-fonts
    visual-studio-code-bin
    yay
)
