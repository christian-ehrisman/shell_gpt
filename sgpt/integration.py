bash_integration = """
# Shell-GPT integration BASH v0.2
_sgpt_bash() {
if [[ -n "$READLINE_LINE" ]]; then
    READLINE_LINE=$(sgpt --shell <<< "$READLINE_LINE" --no-interaction)
    READLINE_POINT=${#READLINE_LINE}
fi
}
bind -x '"\\C-l": _sgpt_bash'
# Shell-GPT integration BASH v0.2
"""

zsh_integration = """
# Shell-GPT integration ZSH v0.2
_sgpt_zsh() {
if [[ -n "$BUFFER" ]]; then
    _sgpt_prev_cmd=$BUFFER
    BUFFER+="⌛"
    zle -I && zle redisplay
    BUFFER=$(sgpt --shell <<< "$_sgpt_prev_cmd" --no-interaction)
    zle end-of-line
fi
}
zle -N _sgpt_zsh
bindkey ^l _sgpt_zsh
# Shell-GPT integration ZSH v0.2
"""
fish_integration = """
# Shell-GPT integration FISH v0.1
function _sgpt_fish
    if test -n "$CMDLINE" -o -n "$cmdline"
        set CMDLINE (sgpt --shell <<< "$CMDLINE" --no-interaction)
        set_cursor -p (string length -c "$CMDLINE")
    end
end

bind \cl _sgpt_fish
"""