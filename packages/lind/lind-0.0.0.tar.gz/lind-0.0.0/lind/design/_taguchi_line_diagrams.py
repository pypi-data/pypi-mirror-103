"""
taguchi_line_diagrams: a utility module dedicated to code for graphing Taguchi line diagrams for
Taguchi orthogonal array interactions

The Taguchi method can be confusing to use. Less experienced users may want to review the details
of the method before trying to use this module.

"""

import logging
from typing import Optional

import networkx as nx
import matplotlib.pyplot as plt

# set logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


####################################################################################################


l4_2_3 = [{
    ('1', '2'): '3'
}]


l8_2_4_4_1 = []  # TODO: find line graph

l8_2_7 = [{
    ('1', '2'): '3',
    ('1', '4'): '5',
    ('2', '4'): '6'
}, {
    ('1', '2'): '3',
    ('1', '4'): '5',
    ('1', '7'): '6'
}]

l9_3_4 = [{
    ('1', '2'): '3,4',
}]

l12_2_11 = []  # no line graphs exist

l16_2_15 = []  # TODO: find line graph

l18_2_1_3_7 = []  # TODO: find line graph

l27_3_13 = []  # TODO: find line graph

l36_2_11_3_12 = []  # TODO: find line graph


####################################################################################################


library = {
    "l4_2_3": l4_2_3,
    "l8_2_7": l8_2_7,
    "l12_2_11": l12_2_11,
}


def plot_line_graph(design_name: str, save_path: Optional[str] = None,
                    file_name: Optional[str] = None) -> None:
    """
    plot_line_graph

    Parameters
    ----------
    design_name: str
        the name of the Taguchi design assocaited with the line graph(s); i.e. `L4_2_3`
    save_path: str, optional
        the name to use when saving the png of the line graph; should be an absolute path
    file_name: str, optional
        the name to use when saving the png of the line graph; if multiple line graphs are saved a
        number will be appended to the end of the name

    Returns
    -------
    None
        does not return anything

    """

    design_name = design_name.strip().lower()

    if design_name not in library.keys():
        raise Exception("Line graphs for this design are currently not available.")

    graphs = library[design_name]

    if len(graphs) == 0:
        raise Exception("No Taguchi line graph exists for this design.")

    # a single design may have multiple line graphs
    for i, g in enumerate(graphs):

        nx_graph = nx.Graph()

        for edge in g.keys():
            nx_graph.add_edge(*edge)

        pos = nx.spring_layout(nx_graph)
        nx.draw(nx_graph,
                pos=pos, with_labels=True,
                node_size=1000, node_color="b", alpha=1,
                edge_color="k", linewidths=5, width=5,
                font_color="w", font_weight=700, font_size=20)
        nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels=g, font_size=20, font_weight=700)
        plt.axis('off')
        plt.title("Line Graph {} for Design {} ".format(i, design_name.upper()))

        if save_path is not None:
            assert isinstance(save_path, str), "Input save_path must be None or a string."
            assert file_name is None or isinstance(file_name, str), \
                "Input file_name must be None or a string."
            plt.savefig(save_path + file_name + "_i.png")  # save as png
        plt.show()  # display
