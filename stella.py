#! /usr/local/bin/python3
import argparse
import logging
import os

import reader.chart_reader as chart_reader
import writer.doc_writer as doc_writer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Will create documentation for helm charts using metadata.")
    parser.add_argument("-hcp", "--helm-chart-path", help="Path to helm chart (default `.`).", required=False, default=".")
    parser.add_argument("-o", "--output", help="Output file (default `output.md`).", required=False, default="output.md")
    parser.add_argument("-t", "--template", help="Custom template file.", required=False, default="")
    parser.add_argument("-fh", "--format-html", help="Output using html instead of md.", required=False, action="store_true")
    parser.add_argument("-ah", "--advanced-html", help="Output using html instead of md with additional features.", required=False,
                        action="store_true")
    parser.add_argument("-css", "--css", help="Path to optional css file to use for html generation (use in "
                                              "conjunction with -fh).", required=False, default="")
    parser.add_argument("-v", "--verbose", help="Activate debug logging.", required=False, action="store_true")
    args = parser.parse_args()

    # set logging level
    STELLA_DEBUG = args.verbose
    if STELLA_DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("💫️ stella")
    logging.debug("stella was called with the following arguments:")
    logging.debug(f"--helm-chart-path: {args.helm_chart_path}")
    logging.debug(f"--output: {args.output}")
    logging.debug(f"--template: {args.template}")
    logging.debug(f"--format-html: {args.format_html}")
    logging.debug(f"--format-html: {args.advanced_html}")
    logging.debug(f"--css: {args.css}")
    logging.debug(f"--verbose: {args.verbose}")

    # actual logic
    try:
        # read all necessary metadata
        result = chart_reader.read(args.helm_chart_path)
        
        # fix file ending for case format html
        if args.format_html and args.output.endswith(".md"):
            args.output = args.output.replace(".md", ".html")

        # write doc from gathered data
        doc_writer.write(output=args.output, doc=result, template=args.template, format_html=args.format_html, advanced_html=args.advanced_html, css=args.css)
    except Exception as err:
        logging.exception("Error occurred.")
        exit(1)

    logging.info("Done!")
