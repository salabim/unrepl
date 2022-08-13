import sys
import unrepl
import argparse

__version__ = "1.0.4"


class IncorrectClipboardError(Exception):
    ...


Pythonista = sys.platform == "ios"
if Pythonista:
    import clipboard
    import console

else:
    try:
        from tkinter import messagebox
        from tkinter import Tk
        from tkinter import _tkinter

    except ModuleNotFoundError:
        raise ModuleNotFoundError("tkinter required.")


def _is_repl(text):
    lines = text.splitlines()
    return len(lines) != 0 and lines[0].startswith(">>> ")


def _has_output_lines(text):
    lines = text.splitlines()
    for line in lines:
        if not (line.startswith(">>> ") or line.startswith("... ") or line.strip() == ""):
            return True
    return False


def _get_clipboard():
    if Pythonista:
        contents = clipboard.get()
    else:
        r = Tk()
        r.withdraw()
        try:
            contents = r.clipboard_get()
        except _tkinter.TclError:
            contents = ""
        r.destroy()
    return contents


def _set_clipboard(contents):
    if Pythonista:
        clipboard.set(contents)
    else:
        r = Tk()
        r.withdraw()
        r.clipboard_clear()
        r.clipboard_append(contents)
        r.after(500, r.destroy)
        r.mainloop()


def _messagebox_showinfo(title, message):
    if Pythonista:
        console.alert(title, message)
    else:
        r = Tk()
        r.withdraw()
        messagebox.showinfo(title, message)
        r.destroy()


def _messagebox_askyesnocancel(title, message):
    if Pythonista:
        response = console.alert(title, message, "yes", "no")
        return response == 1
    else:
        r = Tk()
        r.withdraw()
        response = messagebox.askyesnocancel(title, message)
        r.destroy()
    return response


def unrepl(code, use_print_statements=False):
    """
    Cleans up a code fragment from a REPL, with output lines

    Parameters
    ----------
    code : str
        code to clean up

    use_print_statements : bool
        if True (default) use print statements for lines that generate output
        if False, use lines untranslated for lines that generate output

    Returns
    -------
    Cleaned up code

    Raises
    ------
    IncorrectClipboardError if code is not a proper REPL output
    """
    if not _is_repl(code):
        raise IncorrectClipboardError("no REPL output in clipboard")
    lines = code.splitlines()

    result_code = []
    last_line_code_index = None
    for line in lines:
        if line.startswith(">>>") or line.startswith("..."):
            result_code.append(line[4:])
            if line[4:].strip() != "" and not line[4:].strip().startswith("#"):
                last_line_code_index = len(result_code) - 1
        else:
            if use_print_statements:
                if line.strip() != "":
                    if last_line_code_index is not None:
                        last_line = result_code[last_line_code_index]
                        expression = last_line.strip()
                        indent_level = len(last_line) - len(last_line.lstrip())
                        if indent_level:
                            result_code[last_line_code_index] = f"{indent_level * ' '}print(repr({expression})) # {expression.strip()}"
                        else:
                            result_code[last_line_code_index] = f"_ = {expression}; print(repr(_)) # {expression.strip()}"
                        last_line_code_index = None
            result_code.append(f"#  {line}")

    return "\n".join(result_code)


def _main():
    parser = argparse.ArgumentParser(description="converts REPL output in clipboard.")
    parser.add_argument("-u", metavar="y|n", type=str, default="", help="use print statements")
    parsed = parser.parse_args()
    u = parsed.u
    if u == "":
        use_print_statements = None  # denotes that it should be queried
    elif u.lower().startswith("y"):
        use_print_statements = True
    elif u.lower().startswith("n"):
        use_print_statements = False
    else:
        raise AttributeError(f"-u should be followed by y or n, not {u}")

    contents = _get_clipboard()
    if _is_repl(contents):
        if use_print_statements is None:
            if _has_output_lines(contents):
                use_print_statements = _messagebox_askyesnocancel("unrepl", "Use print statements ?")
            else:
                use_print_statements = False

        if use_print_statements is not None:  # didn't press Cancel

            translated_contents = unrepl(contents, use_print_statements=use_print_statements)
            _set_clipboard(translated_contents)
    else:
        _messagebox_showinfo("unrepl", "Clipboard does not contain proper REPL output")


unrepl.IncorrectClipboardError = IncorrectClipboardError
unrepl.__version__ = __version__

if __name__ == "__main__":
    _main()
