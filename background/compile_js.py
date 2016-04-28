# -*- coding: utf-8 -*-

"""
Housekeeping module to run to reduce the tediousness of having to compile/minify
the client-side js files after changing them
Requirement for using this script: Google Closure Compiler from
https://developers.google.com/closure/compiler/#what-is-the-closure-compiler
@author: Darren Vong
"""
import subprocess
import os

def minify_js_files(js_file_names, js_file_dir, compiler_path,
                    out_path="./", compiled_suffix=".min.js"):
    """Minifies the JavaScript files at the list of specified paths to them.
    @param js_file_names: a list of the js file names to be minified
    @param js_file_dir: the path to the directory of the original js files
    @param compiler_path: the path that points to where the Closure compiler jar file is
    @keyword out_path: the output directory for the minified js files
    @keyword compiled_suffix: the suffix naming convention for the minified js files
    """
    
    js_file_names = map(lambda f: js_file_dir+f, js_file_names)
    
    for single_js in js_file_names:
        file_name = os.path.split(single_js)[1].split(".")[0]
        command = ("java -jar %s --js_output_file %s%s %s"
                   %(compiler_path, out_path, file_name+compiled_suffix, single_js))
        subprocess.call(command, shell=True)
        print "%s has been minified!" % file_name

if __name__ == "__main__":
    my_js_files = ["accent_map.js", "h2h_home.js", "head_to_head_graph.js", "head_to_head.js",
                   "helpers.js", "player_filter.js", "polyfills.js", "profile_graph.js",
                   "profile_home.js", "profile_searchbar.js", "profile.js", "unstick_buttons.js"]
    minify_js_files(my_js_files, "../js/", "../../compiler.jar", "out/")