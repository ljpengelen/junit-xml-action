from dataclasses import dataclass
from operator import attrgetter
import os
import re
import sys
import xml.etree.ElementTree as ET


@dataclass
class TestResult:
    className: str
    name: str
    time: str
    stackTrace: str


def get_class_name(element):
    qualifiedClassName = element.attrib["classname"]
    return qualifiedClassName.split(".")[-1]


def parse_test_case(element):
    className = get_class_name(element)
    name = element.attrib["name"]
    time = element.attrib["time"]
    failure = element.find("failure")
    if failure is not None:
        return TestResult(className, name, time, failure.text)

    return TestResult(className, name, time, None)


def parse_junit_xml_file(file):
    tree = ET.parse(file)
    root = tree.getroot()
    return [parse_test_case(child) for child in root.iter("testcase")]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} FOLDER")
        sys.exit(1)

    folder = sys.argv[1]

    xml_files = [
        file
        for file in os.scandir(folder)
        if file.is_file() and re.match("TEST.*\\.xml$", file.name)
    ]
    results = [
        test_result
        for xml_file in xml_files
        for test_result in parse_junit_xml_file(xml_file)
    ]

    sorted_by_method_name = sorted(results, key=attrgetter("name"))
    sorted_by_class_and_method_name = sorted(
        sorted_by_method_name, key=attrgetter("className")
    )

    if "GITHUB_STEP_SUMMARY" in os.environ :
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as github_step_summary:
            for result in sorted_by_class_and_method_name:
                if result.stackTrace is None:
                    print(f"✅ {result.className} - {result.name} passed in {result.time}s", file=github_step_summary)

            for result in sorted_by_class_and_method_name:
                if result.stackTrace is not None:
                    print(f"<details>\n<summary>❌ {result.className} - {result.name} failed in {result.time}s</summary", file=github_step_summary)
                    print(f"```\n{result.stackTrace}```", file=github_step_summary)
                    print("</details>", file=github_step_summary)
