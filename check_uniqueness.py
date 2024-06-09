import os
import sys
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory


# %time is_fs_case_sensitive()
# CPU times: user 752 μs, sys: 117 μs, total: 869 μs
# Wall time: 605 μs
#
# %timeit is_fs_case_sensitive()
# 97.7 ns ± 0.626 ns per loop (mean ± std. dev. of 7 runs, 10,000,000 loops each)

# darwin
# CPU times: user 24 μs, sys: 51 μs, total: 75 μs
# Wall time: 77 μs
# CPU times: user 1 μs, sys: 0 ns, total: 1 μs
# Wall time: 1.67 μs
# linux
# CPU times: user 97 μs, sys: 11 μs, total: 108 μs
# Wall time: 112 μs
# CPU times: user 3 μs, sys: 0 ns, total: 3 μs
# Wall time: 5.48 μs
# win32 (???)
# CPU times: total: 0 ns
# Wall time: 0 ns
# CPU times: total: 0 ns
# Wall time: 0 ns
def is_fs_case_sensitive(source_dir=None):
    if not hasattr(is_fs_case_sensitive, "case_sensitive"):
        with NamedTemporaryFile(prefix="TmP", dir=source_dir) as tmp_file:
            setattr(
                is_fs_case_sensitive,
                "case_sensitive",
                not os.path.exists(tmp_file.name.lower()),
            )
    return is_fs_case_sensitive.case_sensitive


def is_unique_1(parent_path: Path, name: str) -> bool:
    try:
        str(name)
    except UnicodeEncodeError:
        name = name.encode("utf-8")

    if (parent_path / name).exists():
        return True
    return False


def is_unique_2_pathlib(parent_path: Path, name_lower: str) -> bool:
    # os.listdir is much faster here than os.walk or parent_path.iterdir
    for item in os.listdir(str(parent_path)):
        if name_lower == item.lower():
            return True
    return False


def is_unique_2(parent_path: str, name_lower: str) -> bool:
    # os.listdir is much faster here than os.walk or parent_path.iterdir
    for item in os.listdir(parent_path):
        if name_lower == item.lower():
            return True
    return False


def path_exists_with_different_case(parent_path: str, name: str) -> bool:
    full_path = os.path.join(parent_path, name)
    if os.path.exists(full_path):
        return full_path not in [
            os.path.join(parent_path, item) for item in os.listdir(parent_path)
        ]
    return False


def path_exists_with_different_case_pathlib(parent_path: Path, name: str) -> bool:
    full_path = parent_path / name
    if full_path.exists():
        return str(full_path) not in [
            str(parent_path / item) for item in os.listdir(str(parent_path))
        ]
    return False


def path_exists_with_different_case_all_filesystems(
    parent_path: str, name: str
) -> bool:
    parent_path_lower = parent_path.lower()
    full_path = os.path.join(parent_path, name)
    dir_items = list(os.listdir(parent_path))
    return full_path not in [
        os.path.join(parent_path, item) for item in dir_items
    ] and full_path.lower() in [
        os.path.join(parent_path_lower, item.lower()) for item in dir_items
    ]


def path_exists_with_different_case_all_filesystems_pathlib(
    parent_path: Path, name: str
) -> bool:
    parent_path_lower = Path(str(parent_path).lower())
    dir_items = list(os.listdir(str(parent_path)))
    return str(parent_path / name) not in [
        str(parent_path / item) for item in dir_items
    ] and str(parent_path_lower / name.lower()) in [
        str(parent_path_lower / item.lower()) for item in dir_items
    ]


if __name__ == "__main__":
    with TemporaryDirectory() as temp_dir:
        fn_base = Path(temp_dir)
        assert os.path.exists(fn_base)
        assert os.path.isdir(fn_base)
        stub_upper = "DA662D55CB67136651BD3126D0C87BC4.JPG"
        stub_lower = stub_upper.lower()
        fn_upper = fn_base / stub_upper
        fn_lower = fn_base / stub_lower
        fn_upper.touch(mode=0o644, exist_ok=True)
        assert os.path.exists(fn_upper)
        assert os.path.isfile(fn_upper)

        platform = sys.platform
        case_sensitive = is_fs_case_sensitive(fn_base)
        exists_dont_ignore = path_exists_with_different_case(temp_dir, stub_lower)
        exists_ignore = path_exists_with_different_case_all_filesystems(
            temp_dir, stub_lower
        )
        assert (
            path_exists_with_different_case_pathlib(fn_base, stub_lower)
            == exists_dont_ignore
        )
        assert (
            path_exists_with_different_case_all_filesystems_pathlib(fn_base, stub_lower)
            == exists_ignore
        )
        print(f"platform: {platform}")
        print(f"is case sensitive fs: {case_sensitive}")
        print(
            f"file exists with different case (don't ignore fs case-sensitivity): {exists_dont_ignore}"
        )
        print(
            f"file exists with different case (ignore fs case-sensitivity): {exists_ignore}"
        )
        if platform in ("darwin", "win32"):
            assert not case_sensitive
        else:
            assert case_sensitive
        assert exists_ignore
        if not case_sensitive:
            assert exists_dont_ignore
        else:
            assert not exists_dont_ignore
        # darwin: false true true
        # linux: true false true
        # win32: false true true
        # These should also be platform-independent.
        assert not is_unique_1(fn_base, stub_lower)
        assert not is_unique_2_pathlib(fn_base, stub_lower)
        assert not is_unique_2(temp_dir, stub_lower)
