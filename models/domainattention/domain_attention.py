import tensorflow as tf

from databases import MiniImagenetDatabase, AirplaneDatabase, CUBDatabase, OmniglotDatabase, DTDDatabase, \
    FungiDatabase, VGGFlowerDatabase, EuroSatDatabase
from models.crossdomain.cdml import CombinedCrossDomainMetaLearning
from models.domainattention.domain_attention_models import DomainAttentionModel


class DomainAttention(CombinedCrossDomainMetaLearning):
    def __init__(self, train_databases, image_shape=(84, 84, 3), *args, **kwargs):
        self.train_databases = train_databases
        self.epochs_each_domain = [450, 50, 50, 50]
        self.image_shape = image_shape
        super(DomainAttention, self).__init__(*args, **kwargs)

    def get_network_name(self):
        return 'DomainAttentionModel'

    def initialize_network(self):
        da = DomainAttentionModel(
            train_dbs=self.train_databases,
            num_classes=self.n,
            root=self._root,
            db_encoder_epochs=self.epochs_each_domain,
            db_encoder_lr=0.001,
            image_shape=self.image_shape
        )
        da(tf.zeros(shape=(1, *self.image_shape)))

        return da

    def get_only_outer_loop_update_layers(self):
        only_outer_loop_update_layers = set()
        for layer_name in ('conv1', 'conv2', 'conv3', 'conv4', 'bn1', 'bn2', 'bn3', 'bn4', 'attention_network_dense'):
            only_outer_loop_update_layers.add(self.model.get_layer(layer_name))

        return only_outer_loop_update_layers


def run_domain_attention():
    train_domain_databases = [
        MiniImagenetDatabase(),
        OmniglotDatabase(random_seed=47, num_train_classes=1200, num_val_classes=100),
        DTDDatabase(),
        VGGFlowerDatabase()
    ]
    meta_train_domain_databases = [
        AirplaneDatabase(),
        FungiDatabase(),
        CUBDatabase(),
    ]

    test_database = EuroSatDatabase()

    da = DomainAttention(
        train_databases=train_domain_databases,
        meta_train_databases=meta_train_domain_databases,
        database=test_database,
        target_database=test_database,
        network_cls=None,
        image_shape=(84, 84, 3),
        n=5,
        k=1,
        k_val_ml=5,
        k_val_val=15,
        k_val_test=15,
        k_test=1,
        meta_batch_size=4,
        num_steps_ml=5,
        lr_inner_ml=0.05,
        num_steps_validation=5,
        save_after_iterations=15000,
        meta_learning_rate=0.001,
        report_validation_frequency=1000,
        log_train_images_after_iteration=1000,
        number_of_tasks_val=100,
        number_of_tasks_test=1000,
        clip_gradients=True,
        experiment_name='domain_attention_freeze_attention_instance',
        val_seed=42,
        val_test_batch_norm_momentum=0.0,
    )

    da.train(iterations=60000)
    da.evaluate(50, seed=14)


if __name__ == '__main__':
    # tf.config.experimental_run_functions_eagerly(True)

    # TODO Run experiments for VAE
    # TODO We do not need three fully connected layers
    # TODO We have to combine features in a better way
    # TODO Check whether attention is implemented correctly
    run_domain_attention()
