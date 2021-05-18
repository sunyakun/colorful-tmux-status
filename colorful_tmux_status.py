#!/usr/bin/env python3
import os
from setting import *

get_mem_exec_pth = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'get_mem.py')

themes = {
    "default": {
        "left": {
            "format": ["#(date '+%m/%d %H:%M')", "session:#S", "win:#W", "n-panes:#{window_panes}",
                       f"MEM(used):#({get_mem_exec_pth}|jq .rate)%"],
            "color": ['#cd6839', '#ffff00', '#1e90ff', '#00cd66', '#b0a6cd']
        },
        "right": {
            "format": ["PID:#{pid}", "#(whoami)@#H"],
            "color": ['#ffff00', '#1e90ff']
        },
        "font": {
            "color": "#000000"
        }
    }
}


def execute_command(cmd):
    os.popen(cmd)


def execute_tmux_cmd(cmd, *args):
    cmd = ['tmux', cmd]
    cmd.extend(args)
    execute_command(' '.join(cmd))


def tmux_set_option(var, val, obj='window', is_global=True):
    obj_flag_map = {
        'window': '-w',
        'pane': '-p',
        'server': '-s',
        'none': '',
    }
    args = [obj_flag_map[obj]]
    if is_global:
        args.append('-g')

    args.append(var)
    args.append(f'"{val}"')
    execute_tmux_cmd('set-option', *args)


def tmux_get_color(fg, bg=None, attr=None):
    vals = [f'fg={fg}']
    if bg:
        vals.append(f'bg={bg}')
    if attr:
        vals.append(attr)
    return ','.join(vals)


def tmux_print(content='', fg='default', bg='default', attr='none'):
    return f'#[fg={fg},bg={bg},{attr}]{content}'


def tmux_print_powerline(contents, colors, font_color, direct='left'):
    res = []
    arrow = {
        'right': '\uE0B0',
        'left': '\uE0B2'
    }

    if len(contents) != len(colors):
        return ''

    for i, content in zip(range(len(colors)), contents):
        color = colors[i]
        content_color = f'#[fg={font_color},bg={color},none]'

        if direct == 'right':
            arrow_bg = colors[i+1] if i < len(colors)-1 else TMUX_THEME_STATUS_RIGHT_STYLE_BG
            arrow_color = f'#[fg={color},bg={arrow_bg},none]'
            res.append(f'{content_color} {content}{arrow_color}{arrow[direct]}')
        elif direct == 'left':
            arrow_bg = 'default' if i == 0 else colors[i - 1]
            arrow_color = f'#[fg={color},bg={arrow_bg},none]'
            res.append(f'{arrow_color}{arrow[direct]}{content_color}{content} ')
        else:
            return ''

    return ''.join(res)


def set_status_theme():
    tmux_set_option('window-status-separator', ' ')
    tmux_set_option('window-status-current-format', '')
    # Task status
    tmux_set_option('status-style', tmux_get_color(TMUX_THEME_STATUS_STYLE_FG, TMUX_THEME_STATUS_STYLE_BG))
    # Task status left
    tmux_set_option('status-left-style',
                    tmux_get_color(TMUX_THEME_STATUS_LEFT_STYLE_FG, TMUX_THEME_STATUS_LEFT_STYLE_BG))
    tmux_set_option('status-left-length', TMUX_THEME_STATUS_LEFT_LENGTH)
    tmux_set_option('status-left',
                    tmux_print_powerline(themes['default']['left']['format'],
                                         themes['default']['left']['color'],
                                         themes['default']['font']['color'],
                                         'right'))
    # Task status right
    tmux_set_option('status-right-style',
                    tmux_get_color(TMUX_THEME_STATUS_RIGHT_STYLE_FG, TMUX_THEME_STATUS_RIGHT_STYLE_BG))
    tmux_set_option('status-left-length', TMUX_THEME_STATUS_RIGHT_LENGTH)
    tmux_set_option('status-right',
                    tmux_print_powerline(themes['default']['right']['format'],
                                         themes['default']['right']['color'],
                                         themes['default']['font']['color'],
                                         'left'))

    tmux_set_option('status-interval', TMUX_STATUS_INTERVAL)


def apply_theme():
    tmux_set_option('window-style', tmux_get_color(TMUX_THEME_WINDOW_FG, TMUX_THEME_WINDOW_BG))
    tmux_set_option('window-active-style', tmux_get_color(TMUX_THEME_FOCUSED_PANE_FG, TMUX_THEME_FOCUSED_PANE_BG))

    tmux_set_option('pane-border-style', TMUX_THEME_PANE_BORDER_STYLE)
    tmux_set_option('pane-active-border-style', tmux_get_color(TMUX_THEME_PANE_ACTIVE_BORDER_STYLE))

    tmux_set_option('message-command-style',
                    tmux_get_color(TMUX_THEME_MESSAGE_COMMAND_STYLE_FG, TMUX_THEME_MESSAGE_COMMAND_STYLE_BG))
    tmux_set_option('message-style', tmux_get_color(TMUX_THEME_MESSAGE_STYLE_FG, TMUX_THEME_MESSAGE_STYLE_BG))
    set_status_theme()


def tmux_bind_key(key, cmd):
    execute_tmux_cmd('bind-key', key, cmd)


def tmux_enable_mouse():
    tmux_set_option('mouse', 'on')


def apply_bind_keys():
    tmux_bind_key('r', 'source-file ~/.tmux.conf')


def init():
    apply_theme()
    apply_bind_keys()
    tmux_enable_mouse()


if __name__ == '__main__':
    init()
