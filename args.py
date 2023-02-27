from argparse import ArgumentParser, Namespace

name: str = "PTMDataProcessor"
authors: list = ["Erik Pautsch"]


def globus_mass() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Just-In-Time Mass Transfer Tool",
        description="A tool for processing large datasets from the PTMTorrent dataset",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "--source_path",
        help=f'Path of transfer source. DEFAULT: "/~/huggingface/"',
        type=str,
        required=False,
        default='/~/huggingface/'
    )
    parser.add_argument(
        "--dest_path",
        help=f'Path of transfer destination. DEFAULT: "/~/PTM-Torrent/globus_api_test/"',
        type=str,
        required=False,
        default='/~/PTM-Torrent/globus_api_test/'
    )
    parser.add_argument(
        "--source_endpoint",
        help=f'Globus endpoint for transfer source. DEFAULT: is provided',
        type=str,
        required=False,
        default='55e17a6e-9d8f-11ed-a2a2-8383522b48d9'
    )
    parser.add_argument(
        "--dest_endpoint",
        help=f'Globus endpoint for transfer destination. DEFAULT: is provided',
        type=str,
        required=False,
        default='e8d61c7a-ac81-11ed-adfd-bfc1a406350a'
    )
    return parser.parse_args()


def JIT_batch() -> Namespace:
    parser: ArgumentParser = ArgumentParser(
        prog=f"{name} Just-In-Time Listener",
        description=f"A listener used for processing data from the PTMTorrent dataset",
        epilog=f"Author(s): {', '.join(authors)}",
    )

    parser.add_argument(
        "--output_json",
        help=f"Output directory for writing json files. DEFAULT: ./output_dir",
        type=str,
        required=False,
        default="./output_dir",
    )
    parser.add_argument(
        "--output_unzip",
        help="Output directory for unzipping transfer files. DEFAULT: ./unzip_dir",
        type=str,
        required=False,
        default="./unzip_dir",
    )
    parser.add_argument(
        "-i",
        "--incoming",
        help="Directory of expected incoming transfer files. DEFAULT: is provided",
        type=str,
        required=False,
        default='/home/epautsch/PTM-Torrent/globus_api_test/',
    )
    parser.add_argument(
        "-p",
        "--process_single",
        help="Variable to determine if you want to process one file at a time or listen for multiple.\n" +
             "DEFAULT: False",
        type=bool,
        required=False,
        default=True
    )

    return parser.parse_args()
