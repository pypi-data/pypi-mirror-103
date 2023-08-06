from zipfile import ZipFile
import os


def require_not_null(variable, name):
    if not variable:
        raise ValueError("variable '{name}' must not be None.".format(name=name))
    return variable


def zipdir(out_file: str, tmp_dir: str):
    with ZipFile(out_file, "w") as zipfile:
        for file in os.listdir(tmp_dir):
            zipfile.write(os.path.join(tmp_dir, file), file)
