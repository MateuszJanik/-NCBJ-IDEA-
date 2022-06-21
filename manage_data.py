"""
A file to prepare data.

"""
import h5py
import pandas as pd
import numpy as np

from sklearn import cluster

FILE_NAME = "task_data.hdf5"


class PrepareData:
    """
    A class to prepare data.

    """

    @classmethod
    def extract_data(cls, file_name):
        """
        The method extracts data from hdf5 file.

                Parameters:
                        file_name (Str): path to hdf5 file

                Returns:
                        test_data (pd.Dataframe): processed data
        """
        test_data = {}
        data_frame = pd.DataFrame(np.array(h5py.File(file_name)['results']))

        for hour in range(1, len(data_frame) + 1):
            branches = pd.DataFrame(np.array(h5py.File(file_name)['results'][f"hour_{hour}"]["branches"]))
            branches.columns = ['node_from', 'node_to', 'flow_[MW]']
            gens = pd.DataFrame(np.array(h5py.File(file_name)['results'][f"hour_{hour}"]["gens"]))
            gens.columns = ['node_id', 'generation_[MW]', 'cost_[zl]']
            nodes = pd.DataFrame(np.array(h5py.File(file_name)['results'][f"hour_{hour}"]["nodes"]))
            nodes.columns = ['node_id', 'node_type', 'demand_[MW]']
            test_data[f"hour_{hour}"] = {"branches": branches, "gens": gens, "nodes": nodes}
        return test_data

    @classmethod
    def generate_nodes_and_branches(cls, test_data):
        """
        The method returns the data needed to generate a network graph.
                Parameters:
                        test_data (pd.Dataframe): raw data

                Returns:
                        elements (dict): dictionary with data to generate a chart
        """
        elements = []
        for item in test_data["hour_1"]["nodes"]["node_id"]:
            node = {'data': {'id': str(item), 'label': str(item)}}
            elements.append(node)

        branch_dataframe = test_data["hour_1"]["branches"]
        branch_dataframe["branch_id"] = [x for x in range(len(branch_dataframe))]
        for i in range(len(branch_dataframe)):
            branch = {'data': {'source': str(branch_dataframe.loc[i, "node_from"]),
                               'target': str(branch_dataframe.loc[i, "node_to"]),
                               'label': str(branch_dataframe.loc[i, "branch_id"])}}
            elements.append(branch)

        return elements

    @classmethod
    def nodes_bar_plot_data(cls, test_data):
        """
        The method returns a dataframe with data needed to generate a bar chart for nodes.

                Parameters:
                        test_data (pd.Dataframe): raw data

                Returns:
                        final_data_frame (pd.Dataframe): dataframe with the data needed to generate the chart
        """

        nodes_helper_data_frame = pd.DataFrame()
        nodes_helper_data_frame["hour"] = np.nan
        for iterate in range(1, 25):
            nodes = test_data[f"hour_{iterate}"]["nodes"]

            nodes["hour"] = [iterate for x in range(len(nodes))]
            nodes_helper_data_frame = pd.concat([nodes_helper_data_frame, nodes[["node_id", "demand_[MW]", "hour"]]],
                                                axis=0)

        gens = test_data["hour_1"]["gens"]
        nodes_helper_data_frame = pd.merge(nodes_helper_data_frame, gens, on='node_id', how='left')
        nodes_helper_data_frame[["generation_[MW]", "cost_[zl]"]] = nodes_helper_data_frame[
            ["generation_[MW]", "cost_[zl]"]].replace(np.nan, 0)
        final_data_frame = nodes_helper_data_frame.sort_values(["node_id", "hour"])
        return final_data_frame

    @classmethod
    def branches_bar_plot_data(cls, test_data):
        """
        The method returns a dataframe with data needed to generate a bar chart for branches.

                Parameters:
                        test_data (pd.Dataframe): raw data

                Returns:
                        final_data_frame (pd.Dataframe): dataframe with the data needed to generate the chart
        """
        helper_data_frame = pd.DataFrame()
        helper_data_frame["hour"] = np.nan
        for iterate in range(1, 25):
            branches = test_data[f"hour_{iterate}"]["branches"]
            branches["hour"] = [iterate for x in range(len(branches))]
            branches["branch_id"] = [x for x in range(len(branches))]
            helper_data_frame = pd.concat(
                [helper_data_frame, branches[["node_from", "node_to", "hour", "flow_[MW]", "branch_id"]]],
                axis=0)

        final_data_frame = helper_data_frame.sort_values(["node_from", "hour"])
        return final_data_frame

    @classmethod
    def simple_cluster(cls, data, hour, cluster_number):
        """
        The function to create a subdivision into clusters.

                Parameters:
                        data (dataframe): pd.Dataframe
                        hour (int): integer
                        cluster_number (int): integer

                Returns:
                        branches (pd.Dataframe): returns a dataframe with a cluster column
        """
        branches = data[f"hour_{hour}"]["branches"]
        branches["branch_id"] = [x for x in range(len(branches))]
        k_means = cluster.KMeans(n_clusters=cluster_number)
        example_data = np.asarray(branches["flow_[MW]"])[:, None]
        k_means.fit(example_data)
        branches["cluster"] = k_means.labels_
        return branches
