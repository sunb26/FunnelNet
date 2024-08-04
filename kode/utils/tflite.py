import tensorflow as tf


def tf_lite_model(features, model_dir):
    features_cast = tf.cast(features, tf.float32)
    features_ds = tf.data.Dataset.from_tensor_slices(features_cast).batch(1)

    def _representative_data_gen():
        for input_value in features_ds.take(100):
            yield [input_value]

    converter = tf.lite.TFLiteConverter.from_saved_model(model_dir)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.representative_dataset = _representative_data_gen
    return converter.convert()
