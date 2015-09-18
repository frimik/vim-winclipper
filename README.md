## About

Simple hack to get vim register (clipboard) data from vim in your Linux VM to your Windows Clipboard on your Host.

## How it works

After you yank something in vim, you can use the command `:WriteRegister` to write a file to your `/vagrant` share as `/vagrant/vimregister.txt` ..., then a persistant python process on your windows host (that you need to start yourself) like `python clipper.py ~/vimregister.txt` listens to filesystem events on that particular file and smashes it into your windows clipboard...

## Usage

If you're on a *Windows Host* and you use a *Vagrant VM* with Linux on it, this might be for you... any other setup? All bets are off ...

### Windows Host

On the windows host, clone this repository and run:

    pip install -r requirements.txt
    clipper.py ~/vimregister.txt
    
or as appropriate depending on what shell you're using.

Obviously, this requires python on your Windows host...

Oh, and it might fail or just not be as "informative" unless you install [Growl for Windows](http://www.growlforwindows.com/gfw/). If you try this without Growl, Let me know, will ya?
If you do use Growl you will get a desktop notification telling you how many characters were just copied to your clipboard ...

### Linux VM

If you're using [Vundle](https://github.com/gmarik/Vundle.vim), add to your `.vimrc` on your Linux VM and run `:PluginInstall`

    Plugin 'frimik/vim-winclipper', {'rtp': 'vim/'}

Restart or reload your vimrc. (y)ank something into your default (") register (Just pressing 'yy'), followed by the command `:WriteRegister`. This should write what you yanked into `/vagrant/vimregister.txt` and the `clipper.py` process should pick it up ...

