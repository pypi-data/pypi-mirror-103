from smot.version import __version__
import click
import os
import signal
import sys
from smot.util import die
import smot.format as sf

INT_SENTINEL = 9999


class MaybeStringType(click.ParamType):
    name = "?str"

    def convert(self, value, param, ctx):
        if value is None:
            return None
        if value == "":
            return None
        try:
            return str(value)
        except TypeError:
            self.fail(
                "expected a string, got " f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )


MaybeString = MaybeStringType()


class MaybeNatType(click.ParamType):
    name = "?nat"

    def convert(self, value, param, ctx):
        if value is None:
            return None
        if value == INT_SENTINEL:
            return None
        try:
            value = int(value)
        except TypeError:
            self.fail(
                "expected a int, got " f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )
        if value < 1:
            self.fail(f"expected an integer greater than 1, got {value}")
        return value


MaybeNat = MaybeNatType()


class ListOfStringsType(click.ParamType):
    name = "[str]"

    def convert(self, value, param, ctx):
        try:
            if value is None:
                return []
            else:
                return [s.strip() for s in str(value).split(",")]
        except TypeError:
            self.fail(
                "expected a comma delimited string, got "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )


ListOfStrings = ListOfStringsType()


def factorTree(
    node,
    factor_by_capture=None,
    factor_by_field=None,
    factor_by_table=None,
    default=None,
):
    import smot.algorithm as alg

    if factor_by_field is not None:
        try:
            field = int(factor_by_field)
        except ValueError:
            die(
                f"""Expected a positive integer for field --factor-by-field, got '{factor_by_field}'"""
            )
        nodes = alg.factorByField(node, field, default=default)
    elif factor_by_capture is not None:
        node = alg.factorByCapture(node, pat=factor_by_capture, default=default)
    elif factor_by_table is not None:
        node = alg.factorByTable(node, filename=factor_by_table, default=default)
    node = alg.setFactorCounts(node)
    return node


def read_tree(treefile):
    from smot.parser import p_tree

    rawtree = treefile.readlines()
    rawtree = "".join(rawtree)
    tree = p_tree.parse(rawtree)
    return tree


dec_tree = click.argument("TREE", default=sys.stdin, type=click.File())


#      smot tips [<filename>]
@click.command(help="Print the tree tip labels")
@dec_tree
def tips(tree):
    import smot.algorithm as alg

    tree = read_tree(tree)
    tree.tree = alg.setNLeafs(tree.tree)

    def _fun(b, x):
        if x.isLeaf:
            b.append(x.label)
        return b

    for tip in alg.treefold(tree.tree, _fun, []):
        print(tip)


def factoring(function):
    function = click.option(
        "--factor-by-capture",
        type=MaybeString,
        help="A regular expression with a capture for determining factors from labels",
    )(function)

    function = click.option(
        "--factor-by-field",
        type=MaybeNat,
        default=INT_SENTINEL,
        help="Factor by 1-based field index (with '|' delimiters, for now)",
    )(function)

    function = click.option(
        "--factor-by-table", type=MaybeString, help="I don't even know what this is"
    )(function)

    return function


dec_proportion = click.option(
    "-p",
    "--proportion",
    type=click.FloatRange(min=0, max=1),
    help="The proportion of tips in a clade to keep",
)

dec_newick = click.option(
    "--newick",
    is_flag=True,
    help="Write output in simple newick format (tip colors and metadata will be lost)",
)

dec_scale = click.option(
    "-s",
    "--scale",
    type=click.FloatRange(min=0, max=1),
    help="Scale the size of the clade to this power (if there are n tips in a group, it will scale down to n^r)",
)

dec_max_tips = click.option(
    "--max-tips",
    type=click.IntRange(min=0),
    default=5,
    help="Maximum number of tips to keep per unkept factor",
)

dec_min_tips = click.option(
    "--min-tips",
    type=click.IntRange(min=0),
    default=1,
    help="Minimum number of tips to keep per sampling group",
)

dec_seed = click.option("--seed", type=click.IntRange(min=1), help="Random seed")

dec_keep = click.option(
    "-k", "--keep", default=[], type=ListOfStrings, help="Factors to keep"
)

dec_keep_regex = click.option(
    "-r",
    "--keep-regex",
    default="",
    type=str,
    help="Keep all tips that match this pattern, these tips do not count towards downsampling quotas.",
)


@click.command(
    help="Equal sampling. Descend from root to tip. At each node, determine if each subtree contains a single factor. If a subtree is not monophyletic, recurse into the subtree. If the subtree is monophyletic, then select up to N tips (from the --max-tips argument) from the subtree. The selection of tips is deterministic but dependent on the ordering of leaves. To sample a subtree, an equal number of tips is sampled from each descendent subtree, and so on recursively down to the tips. The resulting downsampled subtree captures the depth of the tree, but is not representative of the tree's breadth. That is, if N=6 and a tree splits into two subtrees, one with 3 tips and one with 300 tips, still 3 tips will be sampled from each branch."
)
@factoring
@dec_keep
@click.option(
    "--default", type=str, help="The name to assign to tips that do not match a factor"
)
@dec_max_tips
@click.option("--zero", is_flag=True, help="Set branches without lengths to 0")
@dec_newick
@dec_tree
def equal(
    factor_by_capture,
    factor_by_field,
    factor_by_table,
    keep,
    default,
    max_tips,
    zero,
    newick,
    tree,
):
    import smot.algorithm as alg

    tree = read_tree(tree)
    tree.tree = factorTree(
        node=tree.tree,
        factor_by_capture=factor_by_capture,
        factor_by_field=factor_by_field,
        factor_by_table=factor_by_table,
        default=default,
    )
    tree.tree = alg.sampleContext(tree.tree, keep=keep, maxTips=max_tips)

    if newick:
        print(sf.newick(tree))
    else:
        print(sf.nexus(tree))


@click.command(
    help="Proportional sampling. Randomly sample p (0 to 1, from --proportion) tips from each monophyletic (relative to factors) subtree. Retain at least N tips in each branch (--min-tips)."
)
@factoring
@dec_keep
@dec_keep_regex
@click.option(
    "--default", type=str, help="The name to assign to tips that do not match a factor"
)
@dec_min_tips
@dec_proportion
@dec_scale
@dec_seed
@dec_newick
@click.option("--zero", is_flag=True, help="Set branches without lengths to 0")
@dec_tree
def prop(
    factor_by_capture,
    factor_by_field,
    factor_by_table,
    keep,
    keep_regex,
    default,
    min_tips,
    proportion,
    scale,
    seed,
    newick,
    zero,
    tree,
):
    import smot.algorithm as alg

    if not proportion and not scale:
        die("Please add either a --proportion or --scale option")

    tree = read_tree(tree)
    tree.tree = factorTree(
        node=tree.tree,
        factor_by_capture=factor_by_capture,
        factor_by_field=factor_by_field,
        factor_by_table=factor_by_table,
        default=default,
    )
    tree.tree = alg.sampleProportional(
        tree.tree,
        keep=keep,
        keep_regex=keep_regex,
        proportion=proportion,
        scale=scale,
        minTips=min_tips,
        seed=seed,
    )

    if newick:
        print(sf.newick(tree))
    else:
        print(sf.nexus(tree))


@click.command(
    help="Paraphyletic sampling. The sampling algorithm starts at the root and descends to the tips. At each node, we store monophyletic subtrees in a list and descend into polyphyletic ones (whose leaves have multiple factors). If we reach a tip or encounter a monophyletic child of a different factor than the stored subtrees, then we stop and sample from all tips in the stored trees and initialize a new list with the new monophyletic child."
)
@factoring
@dec_keep
@dec_keep_regex
@click.option(
    "--default", type=str, help="The name to assign to tips that do not match a factor"
)
@dec_min_tips
@dec_proportion
@dec_scale
@dec_seed
@dec_newick
@click.option("--zero", is_flag=True, help="Set branches without lengths to 0")
@dec_tree
def para(
    factor_by_capture,
    factor_by_field,
    factor_by_table,
    keep,
    keep_regex,
    default,
    min_tips,
    proportion,
    scale,
    seed,
    newick,
    zero,
    tree,
):
    import smot.algorithm as alg

    if not proportion and not scale:
        die("Please add either a --proportion or --scale option")

    tree = read_tree(tree)
    tree.tree = factorTree(
        node=tree.tree,
        factor_by_capture=factor_by_capture,
        factor_by_field=factor_by_field,
        factor_by_table=factor_by_table,
        default=default,
    )
    tree.tree = alg.sampleParaphyletic(
        tree.tree,
        keep=keep,
        keep_regex=keep_regex,
        proportion=proportion,
        scale=scale,
        minTips=min_tips,
        seed=seed,
    )

    if newick:
        print(sf.newick(tree))
    else:
        print(sf.nexus(tree))


@click.command(
    help="Impute, annotate with, and/or tabulate factors. The --impute option will fill in missing factors in monophyletic branches. This is useful, for example, for inferring clades given a few references in a tree. There are three modes: 'table' prints a TAB-delimited table of tip names and factors, 'prepend' adds the factor to the beginning of the tiplabel (delimited with '|'), 'append' adds it to the end."
)
@click.argument(
    "method", type=click.Choice(["table", "prepend", "append"], case_sensitive=False)
)
@factoring
@click.option(
    "--default",
    type=str,
    default=None,
    help="The name to assign to tips that do not match a factor",
)
@click.option(
    "--impute",
    is_flag=True,
    default=False,
    help="Infer the monophyletic factor from context, if possible",
)
@click.option(
    "--patristic",
    is_flag=True,
    default=False,
    help="Infer factors by distance on the tree to the nearest label",
)
@dec_newick
@dec_tree
def factor(
    method,
    factor_by_capture,
    factor_by_field,
    factor_by_table,
    default,
    impute,
    patristic,
    newick,
    tree,
):
    import smot.algorithm as alg

    tree = read_tree(tree)
    tree.tree = factorTree(
        node=tree.tree,
        factor_by_capture=factor_by_capture,
        factor_by_field=factor_by_field,
        factor_by_table=factor_by_table,
        default=default,
    )

    if patristic:
        tree.tree = alg.imputePatristicFactors(tree.tree)
    elif impute:
        tree.tree = alg.imputeFactors(tree.tree)

    # create TAB-delimited, table with columns for the tip labels and the
    # (possibly imputed) factor
    if method.lower() == "table":

        def _fun(b, x):
            if x.isLeaf:
                if x.factor is None:
                    factor = default
                else:
                    factor = x.factor
                b.append(f"{x.label}\t{factor}")
            return b

        for row in alg.treefold(tree.tree, _fun, []):
            print(row)

    # prepend or append the factor to the tip labels and print the resulting tree
    else:

        def _fun(x):
            if x.isLeaf:
                if x.factor is None:
                    x.factor = default
                if method.lower() == "prepend":
                    x.label = f"{x.factor}|{x.label}"
                else:
                    x.label = f"{x.label}|{x.factor}"
            return x

        tree.tree = alg.treemap(tree.tree, _fun)

        if newick:
            print(sf.newick(tree))
        else:
            print(sf.nexus(tree))


#      smot tipsed <pattern> <replacement> [<filename>]
@click.command(help="Search and replace patterns in tip labels")
@click.argument("PATTERN", type=str)
@click.argument("REPLACEMENT", type=str)
@dec_newick
@dec_tree
def tipsed(pattern, replacement, newick, tree):
    import smot.algorithm as alg
    import re

    pat = re.compile(pattern)

    def fun_(nodeData):
        if nodeData.label:
            nodeData.label = re.sub(pat, replacement, nodeData.label)
        return nodeData

    tree = read_tree(tree)
    tree.tree = alg.treemap(tree.tree, fun_)

    if newick:
        print(sf.newick(tree))
    else:
        print(sf.nexus(tree))


@click.command(help="Prune a tree to preserve only the tips with that match a pattern")
@click.argument("PATTERN", type=str)
@click.option(
    "-v", "--invert-match", is_flag=True, help="Keep all leafs NOT matching the pattern"
)
@click.option(
    "-P", "--perl", is_flag=True, help="Interpret the pattern as a regular expression"
)
@click.option(
    "-f",
    "--file",
    is_flag=True,
    help="Read patterns from a file instead of a set string",
)
@dec_newick
@dec_tree
def grep(pattern, tree, invert_match, perl, newick, file):
    import smot.algorithm as alg
    import re

    if file:
        with open(pattern, "r") as f:
            patterns = [p.strip() for p in f.readlines()]
            matcher = lambda s: any([p in s for p in patterns])
    elif perl:
        regex = re.compile(pattern)
        if invert_match:
            matcher = lambda s: not re.search(regex, s)
        else:
            matcher = lambda s: re.search(regex, s)
    else:
        if invert_match:
            matcher = lambda s: not pattern in s
        else:
            matcher = lambda s: pattern in s

    def fun_(node):
        return [
            kid for kid in node.kids if (not kid.data.isLeaf or matcher(kid.data.label))
        ]

    tree = read_tree(tree)
    tree.tree = alg.clean(alg.treecut(tree.tree, fun_))

    if newick:
        print(sf.newick(tree))
    else:
        print(sf.nexus(tree))


@click.command()
@click.option("-p", "--pattern", nargs=2, multiple=True)
@click.option(
    "-P", "--perl", is_flag=True, help="Interpret the pattern as a regular expression"
)
@dec_tree
def leaf(pattern, perl, tree):
    """
    Color the tips on a tree.

    smot color -p "swine" "#FFA500" -p "2020-" "#00FF00" my.tre > color.tre
    """
    import smot.algorithm as alg
    import re

    tree = read_tree(tree)

    def _fun(b, x):
        if x.isLeaf:
            b.append(x.label)
        return b

    tips = alg.treefold(tree.tree, _fun, [])

    for (pat_str, col) in pattern:
        if perl:
            pat = re.compile(pat_str)
            matcher = lambda x: re.search(pat, x)
        else:
            matcher = lambda x: pat_str in x
        for tip in tips:
            if matcher(tip):
                tree.colmap[tip] = col

    print(sf.nexus(tree))


colormap_arg = click.option(
    "-c",
    "--colormap",
    type=click.Path(exists=True),
    help="A TAB-delimited, headless table with columns for factor names and hexadecimal colors",
)


def chooseColorScheme(factors):
    # these colors are adapted from Paul Tol's notes here: https://personal.sron.nl/~pault/#sec:qualitative
    if len(factors) == 2:
        # orange and blue
        colors = ["#FFA000", "#0000FF"]
    elif len(factors) == 3:
        # Paul's three
        colors = ["#004488", "#DDAA33", "#BB5566"]
    elif len(factors) <= 6:
        # Paul's medium-contrast 6
        colors = ["#5486C0", "#053275", "#E9C353", "#866503", "#E7849A", "#863144"]
    elif len(factors) <= 11:
        # Paul's sunset
        colors = [
            "#2A3789",
            "#3A65A8",
            "#5C95C2",
            "#87BEDA",
            "#E5E8C0",
            "#FCD17A",
            "#FAA353",
            "#F1693C",
            "#D32623",
            "#91001C",
        ]
    else:
        die("I can't handle more than 11 colors yet")

    colormap = {f : c for (f,c) in  zip(factors, colors)}

    return colormap


def colorBranches(
    is_para, factor_by_capture, factor_by_field, factor_by_table, colormap, tree
):
    import smot.algorithm as alg

    tree = read_tree(tree)

    tree.tree = factorTree(
        node=tree.tree,
        factor_by_capture=factor_by_capture,
        factor_by_field=factor_by_field,
        factor_by_table=factor_by_table,
    )
    tree.tree = alg.setFactorCounts(tree.tree)

    factors = sorted(list(tree.tree.data.factorCount.keys()))

    _colormap = dict()
    if colormap:
        with open(colormap, "r") as f:
            try:
                _colormap = {f: c for (f, c) in [p.split("\t") for p in f.readlines()]}
            except ValueError:
                die("Invalid color map: expected TAB-delimited, two-column file")
    else:
        _colormap = chooseColorScheme(factors)

    if is_para:
        tree.tree = alg.colorPara(tree.tree, colormap=_colormap)
    else:
        tree.tree = alg.colorMono(tree.tree, colormap=_colormap)

    print(sf.nexus(tree))


@click.command(name="mono")
@factoring
@colormap_arg
@dec_tree
def mono_color_cmd(**kwargs):
    """
    Color a tree by monophyletic factor.

    smot color branch mono --factor-by-capture="(1B\.[^|]*)" 1B.tre
    """
    colorBranches(is_para=False, **kwargs)


@click.command(name="para")
@factoring
@colormap_arg
@dec_tree
def para_color_cmd(**kwargs):
    """
    Color a tree by paraphyletic factor.

    smot color branch para --factor-by-capture="(1B.[^|]*)" 1B.tre
    """
    colorBranches(is_para=True, **kwargs)


CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


@click.group(help="Simple Manipulation Of Trees", context_settings=CONTEXT_SETTINGS)
def cli():
    pass


@click.group(
    help="Subsample the tree using various methods. The details of the sampling algorithms differ, but they all start by adding 0 or 1 labels (or factors) to each tip in the tree. These factors are assigned in 1 of 3 ways, described in the --factor-by-capture, --factor-by-field, and --factor-by-table options. Once the factors have been determined, we ascend from tip to root recording the set of all descendent factors in each node. Thus the ancestral node of a monophyletic subtree, where all leaves have the same factor (or no factor), will store a set of exactly one factor. The resulting factored tree is the starting data structure for each of the sampling algorithms.",
    context_settings=CONTEXT_SETTINGS,
)
def sample():
    pass


sample.add_command(equal)
sample.add_command(prop)
sample.add_command(para)


@click.group()
def branch():
    "Color the branches of a tree. You may provide a color map; if you do not, smot will automatically map factors to colors from a color-blind friendly palette."
    pass


branch.add_command(mono_color_cmd)
branch.add_command(para_color_cmd)


@click.group(
    help="Color the tips or branches. The coloring options are highly opinionated. Leaf colors are based on patterns inferred from leaf labels. They are generally independent of the leaf context within the tree. There is no direct way to color leafs by clade (and I don't think there should be). Group coloring should be done at the branch color level. Branch coloring is explicitly phylogenetic - you may color branches that monophyletic or paraphyletic for a given factor. There is no simple way to color a particular branch (and why would you want to do that anyway). So, follow my tree coloring dogma and everything will be fine.",
    context_settings=CONTEXT_SETTINGS,
)
def color():
    pass


color.add_command(leaf)
color.add_command(branch)

cli.add_command(tips)
cli.add_command(sample)
cli.add_command(factor)
cli.add_command(tipsed)
cli.add_command(grep)
cli.add_command(color)


def main():
    sys.setrecursionlimit(1000000)
    cli()


if __name__ == "__main__":
    if os.name is "posix":
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    main()
