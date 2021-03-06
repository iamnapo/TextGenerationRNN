import argparse
import os
import pickle
from six import text_type
import tensorflow as tf

from model import Model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir',
                        type=str,
                        default='save',
                        help='model directory to store checkpointed models')
    parser.add_argument('-n',
                        type=int,
                        default=500,
                        help='number of characters to sample')
    parser.add_argument('--prime',
                        type=text_type,
                        default=u' ',
                        help='prime text')
    parser.add_argument(
        '--sample',
        type=int,
        default=1,
        help=
        '0 to use max at each timestep, 1 to sample at each timestep, 2 to sample on spaces'
    )

    args = parser.parse_args()
    sample(args)


def sample(args):
    with open(os.path.join(args.save_dir, 'config.pkl'), 'rb') as f:
        saved_args = pickle.load(f)
    with open(os.path.join(args.save_dir, 'chars_vocab.pkl'), 'rb') as f:
        chars, vocab = pickle.load(f)
    model = Model(saved_args, True)
    with tf.Session() as sess:
        tf.global_variables_initializer().run()
        saver = tf.train.Saver(tf.global_variables())
        ckpt = tf.train.get_checkpoint_state(args.save_dir)
        if ckpt and ckpt.model_checkpoint_path:
            saver.restore(sess, ckpt.model_checkpoint_path)
            print(
                model.sample(sess, chars, vocab, args.n, args.prime,
                             args.sample))


if __name__ == '__main__':
    main()
