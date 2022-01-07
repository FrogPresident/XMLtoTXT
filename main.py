import argparse
from pathlib import Path
from xml.etree import ElementTree

from tqdm import tqdm


def main():
    args = get_arg_parser().parse_args()
    src: Path = args.src
    out: Path = args.out
    if not src.is_dir():
        raise NotADirectoryError()
    if (exists := out.exists()) and out.is_file():
        raise NotADirectoryError()
    elif not exists:
        out.mkdir(parents=True)

    # loop iterate over a directory
    progress = tqdm(list(src.glob("**/*.xml")))
    for xml_file in progress:
        progress.set_postfix(file=xml_file)
        # read and parse a xml file
        root = ElementTree.parse(xml_file)

        # convert xml element to object
        results = xml_to_yolor(root)

        # store converted object to text file
        with (out / f'{xml_file.stem}.txt').open("w") as fp:
            for yolor_obj in results:
                print(' '.join(yolor_obj), file=fp)


data_tag_names = ['cx', 'cy', 'w', 'h', 'angle']
class_names = {'shrimp': 0, 'eat_shrimp': 1}


def xml_to_yolor(root: ElementTree.ElementTree) -> list[list[str]]:
    """
    convert xml element to yolor object
    """
    results = []
    # loop iterate on root to get all object
    for obj in root.iter('object'):
        box = obj.find('robndbox')
        yolor_obj = [box.find(tag_name).text for tag_name in data_tag_names]
        class_name = obj.find('name').text
        if class_name not in class_names:
            raise ValueError(f"Class `{class_name}` does not in {list(class_names)}.")
        yolor_obj.append(str(class_names[class_name]))

        results.append(yolor_obj)

    return results


def get_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=Path)
    parser.add_argument("-o", "--out", default="out", type=Path)
    return parser


if __name__ == '__main__':
    main()
