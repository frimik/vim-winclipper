if exists('g:loaded_winclipper')
  finish
endif
let g:loaded_winclipper = 1

function! s:check_defined(variable, default)
  if !exists(a:variable)
    let {a:variable} = a:default
  endif
endfunction


call s:check_defined('g:winclipper_register_path', '/vagrant/vimregister.txt')

" writes the default register (") to a file
function! s:WriteRegister(path)
  " using expand here so path can use expansion on $HOME and ~ etc.
  call writefile(split(@", "\n"), expand(a:path))
endfunction

" use :WriteRegister to write out to the file, if the python file
" listener is running on the host side, it will pick it up automatically
com! -nargs=0 -bang WriteRegister
\ call s:WriteRegister(g:winclipper_register_path)
