"""

core/event_bus.py
Summary:

Implements an event-driven architecture, managing the publish-subscribe pattern for decoupled component interactions.
Key Classes/Functions:

EventBus: A class responsible for managing event publication and subscription.
publish(event, data): Publishes an event to all subscribers.
subscribe(event, callback): Registers a callback for a specific event.
Design Patterns:

Publish-Subscribe Pattern: Facilitates event-driven communication between components, supporting decoupled and scalable interactions.

"""
