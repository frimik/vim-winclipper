## About

Simple hack to get vim register (clipboard) data from vim in your Linux VM to your Windows Clipboard on your Host.

## How it works

After you yank something in vim, you can use the command `:WriteRegister` to write a file to your `/vagrant` share ..., then a persistant python process on your windows host (that you need to start yourself) listens to filesystem events on that particular file and smashes it into your windows clipboard...

## Usage

### Windows Host

On the windows host, clone this repository and run:

    pip install -r requirements.txt
    clipper.py ~/vimregister.txt
    
or as appropriate depending on what shell you're using.

Oh, and it might fail or just not be as "informative" unless you install [Growl for Windows](http://www.growlforwindows.com/gfw/)

### Linux VM

If you're using [Vundle](https://github.com/gmarik/Vundle.vim), add to your `.vimrc` on your Linux VM and run `:PluginInstall`

    Plugin 'frimik/vim-winclipper', {'rtp': 'vim/'}

Restart or reload your vimrc. (y)ank something into your default (") register (Just pressing 'yy'), followed by the command `:WriteRegister`. This should write what you yanked into `/vagrant/vimregister.txt` and the `clipper.py` process should pick it up ...

