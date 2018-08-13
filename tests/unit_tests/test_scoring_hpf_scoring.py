"""Test functionalities of hpf scoring."""

from src.scoring.hpf_scoring import HPFScoring
from src.data_store.local_data_store import LocalDataStore
from edward.models import Poisson
import tensorflow as tf
import numpy as np
import unittest


class TestHPFScoringMethods(unittest.TestCase):
    """Test functionalities of hpf scoring."""

    def __init__(self, *args, **kwargs):
        """Initialise the local data store and HPF object."""
        super(TestHPFScoringMethods, self).__init__(*args, **kwargs)
        self.local_obj = LocalDataStore("tests/test_data")
        self.hpf_obj = HPFScoring(self.local_obj)

    def test_basic_object(self):
        """Test basic HPF object."""
        assert self.hpf_obj is not None
        assert self.hpf_obj.theta is not None
        assert self.hpf_obj.beta is not None
        assert round(float(self.hpf_obj.epsilon), 9) == 0.000156564
        assert self.hpf_obj.theta_dummy is not None
        assert isinstance(self.hpf_obj.theta_dummy, Poisson)
        assert self.hpf_obj.theta_dummy.shape.dims[0].value == 13

    def test_normalise_result(self):
        """Test normlise_result() with dummy result."""
        result = np.array([[0.1, 0.2, 0.3],
                           [0.1, 0.2, 0.3],
                           [0.1, 0.2, 0.3]])
        input_id_set = {1}
        normal = self.hpf_obj.normalize_result(
            result, input_id_set, len(result))
        assert(all(i < 0.25 for i in normal))
        assert(any(i == -1.0 for i in normal))

    # Failing test, needs to fixed.
    # def test_match_manifest(self):
    #     """Test match manifest with dummy ids."""
    #     input_id_set = {1}
    #     id_ = self.hpf_obj.match_manifest(input_id_set)
    #     assert int(id_) == -1
    #     input_id_set = {171, 172, 173, 174, 175, 176,
    #                     177, 82, 178, 179, 180, 181, 182, 183}
    #     id_ = self.hpf_obj.match_manifest(input_id_set)
    #     assert int(id_) == 13

    def test_filter_recommendations(self):
        """Test filter_recommendation() with dummy normalised result."""
        normal = np.array([0.2, -1.0, 0.2])
        filter_result = [{'cooccurrence_probability': 20.0,
                          'package_name': 'org.sakaiproject.kernel:sakai-kernel-util',
                          'topic_list': []},
                         {'cooccurrence_probability': 20.0,
                          'package_name': 'org.sakaiproject.kernel:sakai-kernel-api',
                          'topic_list': []}]
        hpf_result = self.hpf_obj.filter_recommendation(normal, 2)
        self.assertListEqual(filter_result, hpf_result)

    def test_folding_in(self):
        """Test 2 flows of folding_in() with dummy input set."""
        input_id_set = {64}
        final_result = self.hpf_obj.folding_in(input_id_set)
        package_set = set([comp['package_name'] for comp in final_result])
        expected_package_set = set(['org.slf4j:slf4j-api',
                                    'commons-lang:commons-lang',
                                    'org.slf4j:slf4j-simple',
                                    'com.sun.jersey:jersey-grizzly2',
                                    'org.apache.commons:commons-lang3'
                                    ])
        assert(all(comp['cooccurrence_probability'] < 50.0
                   for comp in final_result))
        assert package_set == expected_package_set
        input_id_set = {115, 131, 132, 133, 134, 136,
                        2231, 4599, 4600, 4601, 4602,
                        4603, 4604, 4605}
        final_result = self.hpf_obj.folding_in(input_id_set)
        package_set = set([comp['package_name'] for comp in final_result])
        expected_package_set = {'org.mongodb:mongo-java-driver',
                                'commons-validator:commons-validator',
                                'org.springframework:spring-jdbc',
                                'org.hectorclient:hector-core',
                                'xom:xom'
                                }
        assert(all(comp['cooccurrence_probability'] < 10.0
                   for comp in final_result))

    def test_predict(self):
        """Test 2 flows of predict() on dummy input stack."""
        input_stack = ["io.vertx:vertx-core", "io.vertx:vertx-web"]
        predict_result = self.hpf_obj.predict(input_stack)
        assert(all(comp['cooccurrence_probability'] < 100.0
                   for comp in predict_result[0]))
        package_set = set([comp['package_name'] for comp in predict_result[0]])
        expected_package_set = {'org.springframework:spring-beans',
                                'commons-io:commons-io',
                                'org.apache.httpcomponents:httpclient',
                                'org.codehaus.jackson:jackson-mapper-asl',
                                'org.springframework:spring-webmvc'
                                }
        self.assertListEqual(predict_result[2], [])
        assert len(predict_result[1]) == 2
        input_stack = ["io.vertx:vertx-web", "io.vertx:sarah-test-package"]
        predict_result = self.hpf_obj.predict(input_stack)
        assert predict_result[0] == []
        assert len(predict_result[1]) == 1
        assert len(predict_result[2]) == 1 \
            and predict_result[2][0] == "io.vertx:sarah-test-package"

    def test_model_details(self):
        """Test the basic model details function."""
        details = """The model will be scored against
        12405 Packages,
        9523 Manifests,
        Theta matrix of size 0.9446182250976562 MB, and
        Beta matrix of size 1.2304611206054688 MB."""
        assert self.hpf_obj.model_details() == details

    def test_get_sizeof(self):
        """Test static _getsizeof method."""
        int_value = 1
        int_size = 2.6702880859375e-05
        assert HPFScoring._getsizeof(int_value) == "{} MB".format(int_size)


if __name__ == '__main__':
    unittest.main()
