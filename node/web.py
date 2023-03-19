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

    @app.route('/api/status', methods=['GET'])
    def status():
        return {'online'}, 200

    @app.route('/api/config', methods=['GET'])
    def get_config() -> NodeConfig:
        return config, 200

    @app.route('/api/config', methods=['PUT'])
    def put_config(node_id: str):
        node_config = flask.request.json
        config.setkey('node_name', value=node_config.node_name)
        config.setkey('mic_index', value=node_config.mic_index)
        config.setkey('min_audio_sample_length', value=node_config.min_audio_sample_length)
        config.setkey('vad_sensitivity', value=node_config.vad_sensitivity)
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
    