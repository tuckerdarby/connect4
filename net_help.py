from sklearn.neural_network import MLPRegressor
from model_help import batch_train, test_score_net
import pickle


def save_net(mdl, name='net', directory='trained_nets/'):
    pickle.dump(mdl, open(directory+name+'.pkl', 'wb'))


def load_net(name='net', directory='trained_nets/'):
    mdl = pickle.load(open(directory+name+'.pkl', 'rb'))
    return mdl


def _map_name(arr):
    # Helper function for naming nets
    return 'x'.join(map(str, arr))


def name_net(type, layers, dims):
    # Creates a name for a net based on net type (e.g. "mlp_net"), hidden layers, and input shape
    l_name = 'L' + _map_name(layers)
    d_name = 'D' + _map_name(dims)
    net_name = '_'.join([d_name, type, l_name])
    return net_name


def get_net(net_name, hidden_layers):
    # Attempt to load a net if one exists, else create a new one. Then return
    try:
        clf = load_net(net_name)
        print 'Loading net:', net_name
    except Exception as inst:
        print 'Creating new net:', net_name
        clf = MLPRegressor(hidden_layer_sizes=hidden_layers, warm_start=True)
    return clf


def net_trial(realistic=True, batches=10, n_test=1000, net_params=None):
    # Determine Net Parameters
    if net_params is None:
        hidden_layers = (16, 16, 4)
        input_size = (4, 4)
    else:
        hidden_layers = net_params['hidden_layers']
        input_size = net_params['input_size']
    # Get net based on inputs
    net_name = name_net('mlp_net', hidden_layers, input_size)
    clf = get_net(net_name, hidden_layers)
    # Run Training - Batch size limited to 1000
    n_train = 1000 * batches
    batch_train(clf, n_train, sample_shape=input_size, realistic=realistic)
    # Run Test and Score
    score = test_score_net(clf, amount=n_test, sample_shape=input_size, realistic=realistic)
    print 'score', score
    # Save Net
    save_net(clf, net_name)


# net_trial(realistic=True, batches=100)