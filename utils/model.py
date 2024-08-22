import tensorflow as tf

def load_model():
    model_path = "models/1.tflite"
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    return interpreter
