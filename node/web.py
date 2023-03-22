import click
import requests
import flask
import threading
import uuid

from node import config
from node.node import Node
from node.utils.hardware import list_microphones
from node.schemas import NodeConfig

def create_app(node: Node):

    app = flask.Flask('Node')

    @app.route('/api/', methods=['GET'])
    def index():
        return {}, 200

    @app.route('/api/config', methods=['GET'])
    def get_config() -> NodeConfig:
        return config.config, 200

    @app.route('/api/config', methods=['PUT'])
    def put_config(node_id: str):
        node_config = flask.request.json
        config.set('node_name', node_config.node_name)
        config.set('mic_index', node_config.mic_index)
        config.set('min_audio_sample_length', node_config.min_audio_sample_length)
        config.set('vad_sensitivity', node_config.vad_sensitivity)
        node.restart()
        return node_config, 200

    @app.route('/api/config', methods=['GET'])
    def get_microphones():
        return list_microphones(), 200

    @app.route('/api/restart', methods=['GET'])
    def restart():
        node.restart()
        return {}, 200

    return app
    