import codecs

from clang import *
from clang.cindex import *
import sys
Config.set_library_file("C:\\Program Files\\LLVM\\bin\\libclang.dll")
hname="frida-core.h"
hcall="frida.def"

dep=[
    "__va_start",
    "_GLIB_",
    "json_",
    "g_",
    "gio_",
    "glib_",
    "G_",
    "gobject_",
    "_g_",
    "atexit",
]
funcs=[
    "g_bytes",
    "frida_init",
    "frida_device_manager_new",
    "frida_device_manager_close",
    "frida_shutdown",
    "frida_deinit",
    "g_main_loop_new",
    "frida_device_manager_enumerate_devices_sync",
    "frida_device_list_size",
    "frida_device_list_get",
    "frida_device_get_name",
    "frida_device_get_dtype",
    "frida_device_attach_sync",
    "frida_session_create_script_sync",
    "frida_script_load_sync",
    "g_main_loop_is_running",
    "g_signal_connect_data",
    "g_main_loop_run",
    "frida_script_unload_sync",
    "frida_session_detach_sync",
    "frida_device_manager_close_sync",
    "frida_unref",
    "frida_script_post_sync",
    "g_clear_object",
]

depstruct=[
    "Json",
]
def indep(_funcname:str):
    for it in dep:
        if _funcname.startswith(it)==True:
            return True
    return False
def infuncs(_funcname:str):
    for it in funcs:
        if _funcname.startswith(it)==True:
            return True
    return False

def main():
    index = Index.create()
    root = index.parse(hname)
    f = codecs.open(hcall, "w")
    genCallHead(root.cursor,f)
    genCalls(root.cursor,f)
    f.close()
    print("生成完成")


def genCalls(node:Cursor,_f):
    for it in node.get_children():#type:Cursor
        #or str(it.spelling) in funcs
        if infuncs(it.spelling)==True or (it.kind==CursorKind.FUNCTION_DECL and (indep(it.spelling)==False)  and str(it.location.file)==hname):
            print("正在生成函数:{} {}".format(it.spelling,it.type.spelling))
            _f.write("        {}\n".format(it.spelling))
        genCalls(it,_f)
def genCallHead(node,_f):
    _f.writelines("LIBRARY\n")
    _f.writelines("    EXPORTS\n")

if __name__ == '__main__':
    main()