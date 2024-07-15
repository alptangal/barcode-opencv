import logging
import os

import streamlit as st
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

logger = logging.getLogger(__name__)


def get_ice_servers():
    return [ { 'urls': 'stun:freeturn.net:3479' }, { 'urls': 'turn:freeturn.net:3479', 'username': 'free', 'credential': 'free' } ]
    return [{"urls":"stun:stun.relay.metered.ca:80"},{"urls":"turn:global.relay.metered.ca:80","username":"78f36f157b772e52ce9d6a43","credential":"ubUcdj11HN7FSrC2"},{"urls":"turn:global.relay.metered.ca:80?transport=tcp","username":"78f36f157b772e52ce9d6a43","credential":"ubUcdj11HN7FSrC2"},{"urls":"turn:global.relay.metered.ca:443","username":"78f36f157b772e52ce9d6a43","credential":"ubUcdj11HN7FSrC2"},{"urls":"turns:global.relay.metered.ca:443?transport=tcp","username":"78f36f157b772e52ce9d6a43","credential":"ubUcdj11HN7FSrC2"}]
