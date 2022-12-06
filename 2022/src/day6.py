import helpers

def main() -> None:
    lines = helpers.read_input()
    print(lines)
    pkt = lines[0]
    for idx, chunk in enumerate(helpers.window(pkt, 14)):
        if len(set(chunk)) == 14:
            print(chunk, idx + 14)


main()
