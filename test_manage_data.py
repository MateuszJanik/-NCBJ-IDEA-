import pandas as pd
import pytest
from manage_data import PrepareData


branches = pd.DataFrame({"node_from": [1], "node_to": [2], "flow_[MW]": [-3]})
gens = pd.DataFrame({"node_id": [1], "generation_[MW]": [22], "cost_[zl]": [6]})
nodes = pd.DataFrame({"node_id": [1, 2], "node_type": [1, 2], "demand_[MW]": [16, 17]})
test_data = {}
for item in range(1, 25):
    test_data[f"hour_{item}"] = {"branches": branches, "gens": gens, "nodes": nodes}


def test_generate_nodes_and_branches():

    test = PrepareData.generate_nodes_and_branches(test_data)
    answer = [{'data': {'id': '1', 'label': '1'}}, {'data': {'id': '2', 'label': '2'}},
              {'data': {'source': '1', 'target': '2', 'label': '0'}}]
    assert test == answer


def test_nodes_bar_plot_data():

    test = PrepareData.nodes_bar_plot_data(test_data)
    answer = pd.read_csv('data/test_nodes_bar_plot_data.csv')
    assert test.equals(answer)


def test_branches_bar_plot_data():

    test = PrepareData.branches_bar_plot_data(test_data)
    answer = pd.read_csv('data/branches_bar_plot_data.csv')
    assert test.equals(answer)


def test_simple_cluster():
    test = PrepareData.simple_cluster(test_data, 1, 1)
    answer = pd.read_csv('"data/test_simple_cluster.csv"')
    assert test.equals(answer)