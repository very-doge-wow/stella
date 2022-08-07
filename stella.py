import argparse
import logging
import os

import reader.chart_reader as chart_reader
import writer.doc_writer as doc_writer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Will create documentation for helm charts using metadata.")
    parser.add_argument("-hcp", "--helm-chart-path", help="Path to helm chart.", required=False, default=".")
    parser.add_argument("-o", "--output", help="Output file.", required=False, default="output.md")
    parser.add_argument("-t", "--template", help="Custom template file.", required=False, default="")
    parser.add_argument("-v", "--verbose", help="Activate debug logging.", required=False, action='store_true')
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
    logging.debug(f"--verbose: {args.verbose}")

    # actual logic
    try:
        result = chart_reader.read(args.helm_chart_path)
        doc_writer.write(output=args.output, input=result, template=args.template)
    except Exception as err:
        logging.exception("Error occured.")
        exit(1)

    logging.info("Done!")
