import pytest
from remote_config.base import RemoteConfig
from jsonschema.exceptions import ValidationError
import mock_data as mock

def test_feature_disable():
    RemoteConfig().features = {u'google-merchant': {u'default': False, u'enable': False, 'stores': set()}}
    assert RemoteConfig().get_feature('google-merchant', 0) == False
        
def test_feature_in_cluster():
    RemoteConfig().features = {u'google-merchant': {u'default': False, u'enable': True, 'stores': set([456, 123])}}
    assert RemoteConfig().get_feature('google-merchant', 123) == True
        
def test_feature_default_false():
    RemoteConfig().features = {u'google-merchant': {u'default': False, u'enable': True, 'stores': set([456])}}
    assert RemoteConfig().get_feature('google-merchant', 123) == False

def test_feature_default_true():
    RemoteConfig().features = {u'google-merchant': {u'default': True, u'enable': True, u'clusters': [u'general/clusters/cluster-google-merchant'], 'stores': set([456])}}
    assert RemoteConfig().get_feature('google-merchant', 123) == True
        
def test_feature_not_exist():
    assert RemoteConfig().get_feature('feature-not-exist', 123) == False

def test_invalid_cluster_consumer():
    RemoteConfig().clusters = None
    RemoteConfig.__list_folders__ = mock.cluster_list
    RemoteConfig.__get_value__ = mock.invalid_cluster_data
    with pytest.raises(ValidationError):
        RemoteConfig().__load_clusters__()

def test_invalid_feature_consumer():
    RemoteConfig().clusters = None
    RemoteConfig.__list_folders__ = mock.cluster_list
    RemoteConfig.__get_value__ = mock.cluster_data
    RemoteConfig().__load_clusters__()
    RemoteConfig.__list_folders__ = mock.feature_list
    RemoteConfig.__get_value__ = mock.invalid_feature_data
    with pytest.raises(ValidationError):
        RemoteConfig().__load_features__()

def test_cluster_feature_consumer():
    RemoteConfig().clusters = None
    RemoteConfig.__list_folders__ = mock.cluster_list
    RemoteConfig.__get_value__ = mock.cluster_data
    RemoteConfig().__load_clusters__()
    RemoteConfig.__list_folders__ = mock.feature_list
    RemoteConfig.__get_value__ = mock.feature_data
    RemoteConfig().__load_features__()

def test_validate_cluster_cache():
    rc = RemoteConfig()
    rc.cluster_minute = 0.02
    RemoteConfig.__list_folders__ = mock.cache_init_list
    RemoteConfig.__get_value__ = mock.cache_init_data
    rc.start()
    assert rc.get_feature('google-merchant', 123) == True
    RemoteConfig.__get_value__ = mock.cache_update_cluster_data
    import time
    time.sleep(2)
    assert rc.get_feature('google-merchant', 123) == False
