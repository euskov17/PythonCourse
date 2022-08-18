import typing as tp


def reformat_git_log(inp: tp.IO[str], out: tp.IO[str]) -> None:
    """Reads git log from `inp` stream, reformats it and prints to `out` stream

    Expected input format: `<sha-1>\t<date>\t<author>\t<email>\t<message>`
    Output format: `<first 7 symbols of sha-1>.....<message>`
    """
    lines = inp.readlines()
    for line in lines:
        message = line[line.rfind('\t') + 1:]
        out.write(line[:7] + '.' * (81 - 7 - len(message)) + message)
