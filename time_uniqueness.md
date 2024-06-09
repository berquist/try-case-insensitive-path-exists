# Timings

| platform | function | module    | mean (μs) | std. dev. (ns) |
|----------|----------|-----------|-----------|----------------|
| macOS    |          | `pathlib` | 20.6      | 69             |
| macOS    |          | `os.path` | 13.8      | 213            |
| macOS    |          | `pathlib` | 22.7      | 114            |
| macOS    |          | `os.path` | 10.3      | 210            |
| Ubuntu   |          | `pathlib` | 11.2      | 35.9           |
| Ubuntu   |          | `os.path` | 3.46      | 55.6           |
| Ubuntu   |          | `pathlib` | 44        | 24.5           |
| Ubuntu   |          | `os.path` | 12.4      | 185            |
| Windows  |          | `pathlib` | 83.2      | 780            |
| Windows  |          | `os.path` | 43.3      | 784            |
| Windows  |          | `pathlib` | 63.4      | 71.9           |
| Windows  |          | `os.path` | 28.8      | 93.2           |
