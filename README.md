## About

Simple hack to get vim register (clipboard) data from vim in your Linux VM to your Windows Clipboard on your Host.

## Usage

### Windows Host

On the windows host, clone this repository and run:

    pip install -r requirements.txt
    clipper.py ~/vimregister.txt
    
or as appropriate depending on what shell you're using.

### Linux VM

If you're using [Vundle](https://github.com/gmarik/Vundle.vim), add to your `.vimrc` on your Linux VM and run `:PluginInstall`

    Plugin 'frimik/vim-winclipper', {'rtp': 'vim/'}

Restart or reload your vimrc. (y)ank something into your default (") register (Just pressing 'yy'), followed by the command `:WriteRegister`. This should write what you yanked into `/vagrant/vimregister.txt` and the `clipper.py` process should pick it up ...

