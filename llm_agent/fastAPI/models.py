"""
This module contains Pydantic models for handling webhook messages in a FastAPI application.
"""

from pydantic import BaseModel


class Message(BaseModel):
    """
    This class represents a message model.
    """

    message: str


class AlertAnnotations(BaseModel):
    """
    This class represents the annotations of an alert.
    """

    summary: str


class Alert(BaseModel):
    """
    This class represents an alert.
    """

    status: str
    annotations: AlertAnnotations
    startsAt: str
    endsAt: str
    dashboardURL: str
    panelURL: str


class GrafanaWebhookMessage(BaseModel):
    """
    This class represents a Grafana webhook message.
    """

    alerts: list[Alert]
    commonAnnotations: dict
    title: str
    status: str
    state: str
    message: str
