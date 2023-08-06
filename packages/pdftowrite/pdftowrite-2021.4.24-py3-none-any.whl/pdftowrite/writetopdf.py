import argparse, tempfile, shutil, subprocess, asyncio, sys, os
from pathlib import Path
import pdftowrite.utils as utils
import pdftowrite.docs
from pdftowrite.docs import SVG_NS, Page, Document
from pdftowrite import __version__

WK_SCALE = 1.333333333

def arg_parser():
    parser = argparse.ArgumentParser(description='Convert Stylus Labs Write document to PDF')
    parser.add_argument('file', metavar='FILE', type=str, nargs=1,
                        help='A Write document')
    parser.add_argument('-v', '--version', action='version', version=__version__)
    parser.add_argument('-o', '--output', action='store', type=str, default='',
                        help='Specify output filename')
    parser.add_argument('-f', '--force', action='store_true',
                        help='Overwrite existing files without asking')
    parser.add_argument('-g', '--pages', action='store', type=str, default='all',
                        help='Specify pages to convert (e.g. "1 2 3", "1-3") (default: all)')
    parser.add_argument('-s', '--scale', action='store', type=float, default=1.0,
                        help='Scale page size (default: 1.0)')
    return parser

def read_svg(filename: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdir:
        ext = Path(filename).suffix
        if ext == '.svgz':
            new_filename = str(Path(tmpdir) / Path(filename).name)
            shutil.copy(filename, new_filename)
            subprocess.check_call(['gzip', '-S', 'z', '-df', new_filename])
            filename = str(Path(new_filename).with_suffix('.svg'))
        elif ext != '.svg':
            raise ValueError(f'Invalid file extension: {ext} (Use .svg or .svgz)')
        with open(filename, 'r') as f:
            return f.read()

def process_page(page: Page, output_dir: str, ns: argparse.Namespace) -> str:
    if utils.unit(page.width) == '%' or utils.unit(page.height) == '%':
        raise Exception(f'Percentage(%) is not supported for page size')

    page.viewbox = f'0 0 {utils.val(page.width)} {utils.val(page.height)}'
    page.x = '0px'
    page.y = '0px'
    page.width = f'{utils.px(page.width) * ns.scale}px'
    page.height = f'{utils.px(page.height) * ns.scale}px'

    width = page.width
    height = page.height

    page.width = f'{utils.val(width) * WK_SCALE}{utils.unit(width)}'
    page.height = f'{utils.val(height) * WK_SCALE}{utils.unit(height)}'

    els = page.tree.getroot().findall('.//{%s}svg' % SVG_NS)
    els += utils.find_elements_by_class(page.tree, 'pagerect')
    for el in els:
        if 'width' in el.attrib:
            el.set( 'width', str(utils.val(el.get('width'))) )
        if 'height' in el.attrib:
            el.set( 'height', str(utils.val(el.get('height'))) )

    filename = str(Path(output_dir) / f'page-{page.page_num}.svg')
    output = str(Path(output_dir) / f'page-{page.page_num}.pdf')
    page_output = str(Path(output_dir) / f'page-{page.page_num}-1.pdf')

    with open(filename, 'w') as f:
        f.write(page.svg)

    subprocess.check_call(['wkhtmltopdf',
            '--page-width', f'{width}', '--page-height', f'{height}',
            '-T', '0', '-R', '0', '-B', '0', '-L', '0',
            filename, output
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if utils.cmd_exists(['pdftk', '--help']):
        subprocess.check_call(['pdftk', output, 'cat', '1', 'output', page_output])
    else:
        page_output_pattern = str(Path(output_dir) / f'page-{page.page_num}-%d.pdf')
        subprocess.check_call(['pdfseparate', '-f', '1', '-l', '1', output, page_output_pattern])
    os.remove(filename)
    os.remove(output)
    return page_output

async def generate_pdf(doc: Document, output: str, ns: argparse.Namespace) -> None:
    with tempfile.TemporaryDirectory() as tmpdir:
        loop = asyncio.get_running_loop()
        tasks = []
        for page in doc.pages:
            task = loop.run_in_executor(None, process_page, page, tmpdir, ns)
            tasks.append(task)
        pages = await asyncio.gather(*tasks)
        if utils.cmd_exists(['pdftk', '--help']):
            subprocess.check_call(['pdftk', *pages, 'cat', 'output', output])
        else:
            subprocess.check_call(['pdfunite', *pages, output])

def run(args):
    parser = arg_parser()
    ns = parser.parse_args(args)
    filename = ns.file[0]

    svg = read_svg(filename)
    num_pages = pdftowrite.docs.num_pages(svg)
    if num_pages <= 0: raise Exception('Document has no pages')
    page_nums = utils.parse_range(ns.pages, num_pages)
    doc = Document(svg, page_nums)
    output = ns.output if ns.output else str(Path(filename).with_suffix('.pdf'))

    if not ns.force and Path(output).exists():
        if not utils.query_yn(f'Overwrite?: {output}'): return

    loop = asyncio.get_event_loop()
    loop.run_until_complete( generate_pdf(doc, output, ns) )
    loop.close()

def main():
    run(sys.argv[1:])
