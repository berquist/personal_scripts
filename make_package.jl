# TOOD put this in REPL config

using PkgTemplates

t = Template(;
             dir="~/development/julia",
             plugins=[
                 License(; name="BSD3"),
                 Git(; ssh=true),
                 GitHubActions(),
                 Codecov(),
                 Coveralls(),
                 Documenter{GitHubActions}(),
             ],
             )
