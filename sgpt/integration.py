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
powershell_integration = """
# Shell-GPT integration PowerShell v0.2
# Define a function to handle integration
function Invoke-SGPT_PowerShell {
    if ($null -ne $Host.UI.RawUI) {
        $originalCursorPosition = $Host.UI.RawUI.CursorPosition
        $prompt = "PS> "
        $input = $null
        $output = $null
        $error = $null

        # Display the integration prompt
        Write-Host -NoNewline $prompt

        # Read user input
        $input = [Console]::ReadLine()

        if ($null -ne $input) {
            $output = Invoke-Expression -Command $input 2>&1

            # Display the output
            if ($null -ne $output) {
                $output | ForEach-Object { Write-Host $_ }
            }
        }

        # Restore the cursor position and prompt
        $Host.UI.RawUI.CursorPosition = $originalCursorPosition
        Write-Host -NoNewline "> "
    }
}
# Define a key binding to trigger the integration function
Set-PSReadlineKeyHandler -Key "Ctrl+L" -ScriptBlock { Invoke-SGPT_PowerShell }
"""