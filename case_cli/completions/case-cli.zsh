#compdef case-cli
# Zsh completion for case-cli
# Source this file or add to .zshrc:
#   eval "$(case-cli --completion zsh)"

_case_cli() {
    local -a styles
    styles=(
        'upper:HELLO WORLD'
        'lower:hello world'
        'snake:hello_world'
        'kebab:hello-world'
        'header:Hello-World'
        'camel:helloWorld'
        'pascal:HelloWorld'
        'title:Hello World'
        'random:hElLo WoRlD'
        'constant:HELLO_WORLD'
        'ada:Hello_World'
        'cobol:HELLO-WORLD'
        'train:Hello-World'
        'sentence:Hello world'
        'dot:hello.world'
    )

    _arguments -s \
        '(-v --version)'{-v,--version}'[Show version]' \
        '(-h --help)'{-h,--help}'[Show help]' \
        '(-c --case)'{-c,--case}'[Target case style]:style:(( ${styles} ))' \
        '--completion[Generate shell completion script]:shell:(bash zsh)' \
        '1:command or input:->first_arg' \
        '*:input text:' \
    && return 0

    case "${state}" in
        first_arg)
            _alternative \
                'subcommands:subcommand:(set)' \
                'input:input text:'
            ;;
    esac
}

_case_cli "$@"
