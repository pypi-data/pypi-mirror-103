# -*- coding: utf-8 -*-
"""
@author: Thomas Bitsky Jr
(C) Copyright 2020-2021 Automated Design Corp. All Rights Reserved.

A one-to-many pub/sub class for supporting global events
and loose coupling of APIs. Uses asyncio for non-blocking publication
of events.

Topics can be subscribed to either onchange (default) to save
bandwidth, or ALL so that the event is always received.

"""


"""
Important!
Disable ctrl-c causing an exception and blocking graceful shutdown.
"""
from typing import AnyStr, Callable
import time
import logging
import asyncio
import os
os.environ['FOR_DISABLE_CONSOLE_CTRL_HANDLER'] = '1'


# Create a named logger instance
log = logging.getLogger(__name__)


class Events(object):
    """A simple one-to-many pub/sub class for supporting global events.
    Requires asyncio

    Usage
    -----

        Asynchronous:

        @Events.subscribe("hello")
        async def example(*args, **kwargs):
            print ("recv signal, values:", args, kwargs)

        @Events.subscribe("hello")
        async def moreexample(*args, **kwargs):
            print ("I also recv signal, values:", args, kwargs)

        Events.publish("hello", "There")

        >>> recv signal, values: ("There",) {}
        >> I also recv signal, values: ("There",) {}


        Blocking:
        @Events.subscribe("hello")
        def example(*args, **kwargs):
            print ("recv signal, values:", args, kwargs)

        @Events.subscribe("hello")
        def moreexample(*args, **kwargs):
            print ("I also recv signal, values:", args, kwargs)

        Events.publish_sync("hello", "There")

        >>> recv signal, values: ("There",) {}
        >> I also recv signal, values: ("There",) {}


    """

    subs = {}

    SUBSCRIBE_ALL_EVENTS = 0
    SUBSCRIBE_ONCHANGE = 1

    @staticmethod
    def add_subscribe(
        event: str,
        func,
        subscription_type: int = SUBSCRIBE_ONCHANGE,
        include_topic: bool = False
    ):
        """Subscribe the method of a class instance to an event id.
        Can't use a decororator for this because 'self' won't be created.

        Not required for static methods. In that case, use the subscribe decorator.

        Parameters
        ----------
        event : str
            ID of the event

        func : function
            The method/slot to call back.

        subscription_type : int
            Specify whether to receive a signal only when the value
            has changed (default) or every time the value is published.

        include_topic : bool
            Included the published topic as an argument. Requires that
            the target method accepts the topic string as the first parameter.
            i.e.  my_target_method(topic:str, value:Any)
        """

        should_publish = False
        value = None

        if event not in Events.subs:
            Events.subs[event] = []
        else:
            if subscription_type == Events.SUBSCRIBE_ONCHANGE:
                value = Events.subs[event][0]["last_value"]

                if value != None:
                    should_publish = True

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        ev = {
            "func": func,
            "loop": loop,
            "topic" : event,
            "subscription_type": subscription_type,
            "last_value": value,
            "include_topic" : include_topic
        }

        Events.subs[event].append(ev)

        if should_publish:
            Events._publish_event(ev, *value)

    @staticmethod
    def unsubscribe_method(event: str, func: Callable) -> None:
        """Remove the subscription on a topic for a particular
        function.
        """
        if event in Events.subs:

            newlist = []

            for item in Events.subs[event][:]:
                if "func" in item:
                    if item["func"] != func:
                        newlist.append(item)

            Events.subs[event] = newlist

    @staticmethod
    def subscribe_method(event: str,
                         func: Callable,
                         subscription_type: int = SUBSCRIBE_ONCHANGE,
                         include_topic: bool = False
                         ) -> None:
        """Subscribe the method of a class instance to an event id.
        Can't use a decororator for this because 'self' won't be created.

        Not required for static methods. In that case, use the subscribe decorator.

        Parameters
        ----------
        event: str
            ID of the event

        func: function
            The method/slot to call back.

        subscription_type: int
            Specify whether to receive a signal only when the value
            has changed(default) or every time the value is published.

        include_topic: bool
            Included the published topic as an argument. Requires that
            the target method accepts the topic string as the first parameter.
            i.e.  my_target_method(topic: str, value: Any)

        """
        Events.add_subscribe(
            event, 
            func, 
            subscription_type=subscription_type,
            include_topic=include_topic
        )

    @staticmethod
    def subscribe(event: str, subscription_type: int = SUBSCRIBE_ONCHANGE) -> None:
        """Subscribe a function  to an event ID.

        Parameters
        ----------
        event: str
            ID of the event

        """

        def wrap_function(func: Callable):

            Events.add_subscribe(event, func, subscription_type)
            return func
        return wrap_function

    @staticmethod
    def _publish_event(ev, *args, **kwargs):

        if asyncio.iscoroutinefunction(ev["func"]):

            loop = ev["loop"]  
            asyncio.run_coroutine_threadsafe(ev["func"](*args, **kwargs), loop)
            
        else:

            ev["func"](*args, **kwargs)


    @staticmethod
    def publish(event: str, *args, **kwargs):
        """Signal or publish values to all subscribers of the specified
        event ID.

        For coroutine functions defined with async, returns immediately. The
            callback is scheduled into the event loop.
        Synchronous functions are executed in order and block untile done.
        """

        if event in Events.subs:

            try:
                for ev in Events.subs[event]:

                    should_publish = False
                    if ev["subscription_type"] == Events.SUBSCRIBE_ALL_EVENTS:
                        should_publish = True
                    elif ev["subscription_type"] == Events.SUBSCRIBE_ONCHANGE:
                        if args != ev["last_value"] or ev["last_value"] == None:
                            should_publish = True

                    if should_publish:

                        if not ev["include_topic"]:
                            Events._publish_event(ev, *args, **kwargs)
                        else:
                            # in this case, we include the topic name as the first argument
                            Events._publish_event(ev, event, *args)

                        ev["last_value"] = args

            except Exception as e:
                logging.warning(f"Exception processing event {event} :\n {e}")

    @staticmethod
    def publish_sync(event: str, *args, **kwargs):
        """Signal or publish values to all subscribers of the specified
        event ID. SYNCHRNOUS AND BLOCKING.

        """
        try:
            for ev in Events.subs[event]:
                try:
                    ev["func"](*args, **kwargs)
                except Exception as e:
                    Events.logger(f"{e}")
        except:
            pass


"""


# avoids having to import Events
add_subscribe = Events.add_subscribe
subscribe = Events.subscribe
send = Events.send
send_queue = Events.send_queue
send_thread = Events.send_thread
send_blocking = Events.send_blocking
"""


if __name__ == '__main__':
    """ If this script is executed as the "main" file .

    Used only for testing. Not very useful.
    """

    logging.basicConfig(level="DEBUG")

    @Events.subscribe("testsig")
    async def testsig_decorator(data):
        print(f"\t\tDecorator Test signal received! {data}")

    async def testsig_method(data):
        print(f"\t\tMethod test signal received! {data}")

    async def later_method(data):
        print(f"\t\tLater method test signal received! {data}")

    async def method_with_topic(topic, data):
        print(f"\t\tMethod with topic {topic} received! {data}")        

    async def test_basic():

        print("Test signal to multiple methods.")
        Events.subscribe_method("testsig", testsig_method)

        await asyncio.sleep(delay=0.5)

        Events.publish("testsig", "First")

        await asyncio.sleep(delay=0.5)

        print("Test removing method.")
        Events.unsubscribe_method("testsig", testsig_method)
        Events.publish("testsig", "Second")

    async def test_onchange():

        print("Test OnChange.\n------------------\n")

        Events.subscribe_method("testsig", testsig_method)

        await asyncio.sleep(delay=0.25)

        # The first event should be posted.
        print("An event should be received by the two listeners....")
        Events.publish("testsig", "Third")

        print("I will now publish the same value again...")

        for x in range(0, 3):
            print("Publishing... (should not see event)")
            await asyncio.sleep(delay=1)
            Events.publish("testsig", "Third")

        await asyncio.sleep(delay=1)

        print("I will now publish a new value. It should be received.")

        Events.publish("testsig", "Fourth")

        await asyncio.sleep(delay=1)
        print("I will now subscribe a new method to the topic. It should get the last value published.")

        Events.subscribe_method("testsig", later_method)

        await asyncio.sleep(delay=1)

        print("I will now publish a repeat value. It should not be received.")

        Events.publish("testsig", "Fourth")

        await asyncio.sleep(delay=1)

        print("I will now publish a new value. It should be received.")
        Events.publish("testsig", "Fifth")

        await asyncio.sleep(delay=1)

        print("test_onchange complete")

    async def test_include_topic():

        print("I will now subscribe a method with a topic parameter... ")
        Events.subscribe_method("meth_topic", method_with_topic, include_topic=True)

        await asyncio.sleep(delay=1)

        print("I will now publish a value on that topic. Both the topic name value should appear.")

        Events.publish("meth_topic", "Gyro")

        await asyncio.sleep(delay=2)

        print("test_include_topic complete")


    async def run_tests():

        await test_basic()
        await test_onchange()

        await test_include_topic()

        print("\n\n--- All done. ---")

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    try:

        asyncio.run_coroutine_threadsafe(run_tests(), loop)

        print("Press CTRL-C to stop.")

        loop.run_forever()

    except KeyboardInterrupt:

        print("Closing from keyboard request.")

    except Exception as ex:

        print(f"Exception: {ex}")

    finally:

        loop.stop()

        print("Goodbye.")
