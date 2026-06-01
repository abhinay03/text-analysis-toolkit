import argparse
import sys
from text_analysis_toolkit.analyzer import TextAnalyzer


def main():
    parser = argparse.ArgumentParser(
        prog="text-analysis",
        description="Text Analysis Toolkit - Tokenization, Frequency, Sentiment, and Reports"
    )
    parser.add_argument("file", nargs="?", help="Path to the text file to analyze")
    parser.add_argument("-t", "--text", help="Text string to analyze (alternative to file)")
    parser.add_argument("-o", "--output", help="Output file path for the report")
    parser.add_argument("-f", "--format", choices=["text", "json"], default="text",
                        help="Report format (default: text)")
    parser.add_argument("--no-stopwords", action="store_true",
                        help="Remove common stopwords from analysis")
    parser.add_argument("--ngram-min", type=int, default=2,
                        help="Minimum n-gram size (default: 2)")
    parser.add_argument("--ngram-max", type=int, default=3,
                        help="Maximum n-gram size (default: 3)")

    args = parser.parse_args()

    if not args.file and not args.text:
        parser.print_help()
        sys.exit(1)

    ta = TextAnalyzer(
        remove_stopwords=args.no_stopwords,
        ngram_range=(args.ngram_min, args.ngram_max),
        report_title="Text Analysis Report",
    )

    if args.file:
        result = ta.analyze_file(args.file)
    else:
        result = ta.analyze(args.text)

    if args.format == "json":
        output = ta.report_json(result)
    else:
        output = ta.report_text(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report written to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
