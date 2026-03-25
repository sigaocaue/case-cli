# Bash completion for case-cli
# Source this file or add to .bashrc:
#   eval "$(case-cli --completion bash)"

_case_cli() {
    local cur prev styles
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    styles="upper lower snake kebab header camel pascal title random constant ada cobol train sentence dot"

    # Complete style name after --case or -c
    if [[ "${prev}" == "--case" || "${prev}" == "-c" ]]; then
        COMPREPLY=( $(compgen -W "${styles}" -- "${cur}") )
        return 0
    fi

    # Complete style name after "set" subcommand
    if [[ "${prev}" == "set" ]]; then
        COMPREPLY=( $(compgen -W "${styles}" -- "${cur}") )
        return 0
    fi

    # Complete flags and subcommands
    if [[ "${cur}" == -* ]]; then
        COMPREPLY=( $(compgen -W "--case -c --version -v --help -h --completion" -- "${cur}") )
        return 0
    fi

    # Complete "set" subcommand at first positional arg
    if [[ ${COMP_CWORD} -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "set" -- "${cur}") )
        return 0
    fi

    return 0
}

complete -F _case_cli case-cli
