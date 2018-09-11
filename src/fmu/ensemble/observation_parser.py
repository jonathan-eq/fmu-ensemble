from collections import defaultdict
import pandas as pd
import yaml


def observations_parser(path):
    """ Function to parse the observation yaml file

    Args:
    path: string. file path the observation yaml file

    Returns:
        dictionary containing a dataframe for each observation type
    """

    def read_obs_yaml(path):
        """ Function returns the contents of the observation yaml """
        with open(path, 'r') as stream:
            observations = yaml.load(stream)
        return observations

    def summary_observations(obs_data):
        """ Function returns summary observations in a dataframe  """
        data = defaultdict(list)
        for obs_group in obs_data:
            for obs in obs_group['observations']:
                data['id'].append(obs_group['key']+'_'+
                                  obs['date'].strftime('%d_%m_%Y'))
                data['key'].append(obs_group['key'])
                data['date'].append(obs['date'])
                data['value'].append(obs['value'])
                data['error'].append(obs['error'])
                data['comments_key'].append(
                    obs_group['comment'] if 'comment' in obs_group.keys(
                        ) else None)
                data['comments_value'].append(
                    obs['comment'] if 'comment' in obs.keys() else None)
        columns = ['id', 'key', 'date', 'value', 'error',
                   'comments_value', 'comments_key']
        dframe = pd.DataFrame(data)
        dframe = dframe[columns]
        return dframe

    def rft_observations(rfts):
        """ Function returns RFT observations in a dataframe  """
        data = defaultdict(list)
        for rft in rfts:
            for index, obs in enumerate(rft['observations']):
                data['id'].append(rft['well'] +
                                  rft['date'].strftime('%d_%m_%Y') +
                                  str(index))
                data['rft_index'].append(index)
                data['well'].append(rft['well'])
                data['date'].append(rft['date'])
                data['value'].append(obs['value'])
                data['error'].append(obs['error'])
                data['zone'].append(obs['zone'])
                data['MDmsl'].append(obs['MDmsl'])
                data['x'].append(obs['x'])
                data['y'].append(obs['y'])
                data['z'].append(obs['z'])
                data['comments_key'].append(
                    rft['comment'] if 'comment' in rft.keys() else None)
                data['comments_value'].append(
                    obs['comment'] if 'comment' in obs.keys() else None)
        columns = ['id', 'rft_index', 'well', 'date', 'value', 'error', 'x',
                   'y', 'z', 'MDmsl', 'zone', 'comments_value', 'comments_key']
        dframe = pd.DataFrame(data)
        dframe = dframe[columns]
        return dframe

    # main
    observations_yaml = read_obs_yaml(path)
    data = {}
    for obs_type, obs_data in observations_yaml.iteritems():
        if obs_type == 'summary_vectors':
            data['summary_vectors'] = summary_observations(obs_data)

        if obs_type == 'general_observations':
            for gen_type, gen_data in obs_data.iteritems():
                if gen_type == 'rft_pressure':
                    data['rft_observations'] = rft_observations(gen_data)
                if gen_type == 'gravity':
                    raise NotImplementedError
                if gen_type == 'some_random_other_obserbations':
                    raise NotImplementedError

    return data