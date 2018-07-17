# python imports

import re
from collections import defaultdict


class FormatIndex(object):

    def __init__(self):
        self.count_by_star = defaultdict(lambda: defaultdict(lambda: 0))
        self.index_count = 0

        # offset spacing config
        self.index_offset = 2
        self.nested_index_offset = 1

        self.nested_indices = list()

    def write_nested_indexes(self):
        temp_indexes = []
        dots_count = max(len(re.search("\.*", index).group()) for index in self.nested_indices) if self.nested_indices else 0
        for index_line in self.nested_indices[::-1]:
            dots = re.search("\.*", index_line).group()
            if dots:
                no_of_dots = len(dots)
                if dots_count == no_of_dots:
                    offset_var = "- "
                else:
                    dots_count -= 1
                    offset_var = "+ "

                offset = " " * (self.index_offset + no_of_dots - 1)
                nested_index = offset + offset_var + re.sub('\.*', '', index_line).strip()
                temp_indexes.append(nested_index)
            else:
                nested_index =  " " * dots_count + "  " +  index_line
                temp_indexes.append(nested_index)
        for x in temp_indexes[::-1]:
            print x
        self.nested_indices = list()


    def align_text(self):
        input_text = open("input.txt").read()
        formatted_text = re.sub(r'\n\s*\n','\n', input_text, re.MULTILINE).strip()
        # this has to be refactored
        lines = formatted_text.splitlines()
        for line in lines:
            line = line.strip()
            if line:
                stars = re.search("\**", line).group()
                if stars:
                    self.write_nested_indexes()
                    no_of_starts = len(stars)
                    if no_of_starts == 1:
                        self.index_count += 1
                        line.replace("*", str(self.index_count))
                        line = line.replace(stars, str(self.index_count))
                        print line
                    elif no_of_starts > 1:
                        self.count_by_star[self.index_count][stars] += 1
                        index_part_1 = str(self.index_count) + "." + str(self.count_by_star[self.index_count][stars])
                        index_part_2 = "".join([".1" for _ in range(no_of_starts-2)])
                        index = index_part_1 + index_part_2
                        line = line.replace(stars, index)
                        print line
                else:
                    self.nested_indices.append(line)
        self.write_nested_indexes()


def main():
    format_index = FormatIndex()
    format_index.align_text()


if __name__ == '__main__':
    main()