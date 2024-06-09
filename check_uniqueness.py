from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
import os
import sys


# %time is_fs_case_sensitive()
# CPU times: user 752 μs, sys: 117 μs, total: 869 μs
# Wall time: 605 μs
#
# %timeit is_fs_case_sensitive()
# 97.7 ns ± 0.626 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)
def is_fs_case_sensitive(source_dir=None):
    if not hasattr(is_fs_case_sensitive, "case_sensitive"):
        with NamedTemporaryFile(prefix="TmP", dir=source_dir) as tmp_file:
            setattr(is_fs_case_sensitive, "case_sensitive", not os.path.exists(tmp_file.name.lower()))
    return is_fs_case_sensitive.case_sensitive


# %timeit assert_unique_1(fn_base, stub_upper)
# 9.41 μs ± 32.3 ns per loop (mean ± std. dev. of 7 runs, 100,000 loops each)
def assert_unique_1(parent_path: Path, name: str) -> bool:
    try:
        str(name)
    except UnicodeEncodeError:
        name = name.encode("utf-8")

    if (parent_path / name).exists():
        # raise RuntimeError(f"{name}' already exists in '{parent_path}")
        return True
    return False


# %timeit assert_unique_2(fn_base, stub_upper, stub_lower)
# 331 μs ± 1.11 μs per loop (mean ± std. dev. of 7 runs, 1,000 loops each)
def assert_unique_2(parent_path: Path, name: str, name_lower: str) -> bool:
    # os.listdir is much faster here than os.walk or parent_path.iterdir
    for item in os.listdir(str(parent_path)):
        if name_lower == item.lower():
            # raise RuntimeError(
            #     f"A directory with name (case independent) '{name}' already exists"
            #     " and cannot be made according to the naming rule 'thorough'."
            # )
            return True
    return False


def path_exists_with_different_case(parent_path: Path, name: str) -> bool:
    items = list(os.listdir(str(parent_path)))
    items_lower = [item.lower() for item in items]
    return name not in items and name.lower() in items_lower


if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        fn_base = Path(temp_dir)
        stub_upper = "DA662D55CB67136651BD3126D0C87BC4.JPG"
        stub_lower = stub_upper.lower()
        fn_upper = fn_base / stub_upper
        fn_lower = fn_base / stub_lower
        fn_upper.touch(mode=0o644, exist_ok=True)

        platform = sys.platform
        exists = path_exists_with_different_case(fn_base, stub_lower)
        print(f"platform: {platform}")
        if platform in ("win32", "darwin"):
            assert exists
        else:
            assert not exists
