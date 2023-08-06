import io
import time
import pandas as pd
import zmq
from IPython.core.display import display, HTML, clear_output

from nespy.exceptions import *
from nespy.format import *
import nespy.grpc.SerializableOperator_pb2 as pb


class Operators:
    """
    This class manages all the operators and translates the query into NebulaStream's Query API syntax.
    """

    def __init__(self):
        self.operator_list = list()
        self.strategy = "BottomUp"

        self.current_window = None

    def from_stream(self, logical_stream_name):
        """
        Identifies on which data stream the user wants to work on.
        This function just adds "Query::from(stream)" to the operator_list.

        Parameters
        ----------
        logical_stream_name : str
                              Name of the logical stream we are working on.

        Returns
        -------
        Operators

        """
        self.operator_list.append("Query::from(\"{}\")".format(logical_stream_name))
        return self

    def filter(self, predicate):
        """
        Filters according to a filter predicate.
        This function adds ".filter(Attribute(a)" to the operator_list. "a" is the filter predicate.

        Parameters
        ----------
        predicate : str
                    Is then added to the fitting string to send a filter query. This string is then added to the list of
                    operators.

        Returns
        -------
        Operators

        """
        self.operator_list.append(".filter({})".format(predicate))
        return self

    def map(self, arg):
        """
        Maps a certain value of the data stream to a new defined value.
        This function adds ".map(a)" whereas a is the mapping expression.
        For example "Attribute("a") = Attribute("a") + 1".

        Parameters
        ----------
        arg : str
              Python map operator already translated into the NebulaStream syntax.

        Returns
        -------
        Operators

        """
        self.operator_list.append(".map({})".format(arg))
        return self

    def select(self, arg):
        """
        Selects an attribute. Like SELECT in SQl or projection in relational algebra.
        This function adds ".project(a)" to the operator_list. The value a is the attribute to project on.

        Parameters
        ----------
        arg : str or list
              List of attributes or Wrapper (if it's just one attribute we want to filter).

        Returns
        -------
        Operators

        """
        if isinstance(arg, Wrapper):
            self.operator_list.append(".project(Attribute(\"{}\"))".format(arg.key[0]))
        elif isinstance(arg, list) & (len(arg) > 0):
            attributes = ""
            for a in arg:
                attributes += "Attribute(\"{}\"), ".format(a)
            attributes = attributes[:-2]  # remove comma and whitespace at the end
            self.operator_list.append(".project({})".format(attributes))

        return self

    def rename(self, arg):
        """
        Renames the columns after a projection.
        This function adds ".rename(a)" to the operator_list after a projection. This a is the new name for the
        projected attribute.

        Parameters
        ----------
        arg : dict
              Keys are the old names of the data stream and the value the new names for this column.

        Returns
        -------
        Operators

        """
        if self.operator_list[-1].startswith(".project"):
            current_project = self.operator_list[-1]
            self.operator_list = self.operator_list[:-1]
            if isinstance(arg, dict):
                for key in arg:
                    new_name = ".rename(\"{}\")".format(arg[key])
                    key_start_index = current_project.index(key)
                    key_end_index = key_start_index + len(key) + 2
                    insert_rename_into_string = current_project[:key_end_index]
                    insert_rename_into_string += new_name
                    insert_rename_into_string += current_project[key_end_index:]
                    current_project = insert_rename_into_string
                self.operator_list.append(current_project)
        return self

    def zmq_sink(self, host, port):
        """
        ZMQ Sink for NES.
        This function adds the zmq sink to the operator_list.

        Parameters
        ----------
        host : str
               Destination host (probably localhost for now).
        port : int
               Destination port.

        Returns
        -------
        Operators

        """
        self.operator_list.append(".sink(ZmqSinkDescriptor::create(\"{}\", {}))".format(host, port))
        return self

    def print_sink(self):
        """
        This function adds the a print sink into the operator_list of this class.
        A print sink prints data in terminal.

        Returns
        -------
        Operators

        """
        self.operator_list.append(".sink(PrintSinkDescriptor::create())")
        return self

    def window(self, window):
        """
        Adds query to create any window.

        Parameters
        ----------
        window :  Windows
                  Window object that manages window type, parameters of window, aggregation function and create query
                  for the window.

        Returns
        -------
        Operators

        """
        self.current_window = window
        self.operator_list.append(self.current_window.create_window_query())
        return self

    def aggr_func(self, aggr_type, on, name=""):
        """
        Adds aggregation functions to operators.
        Only works if a window has been selected or the window was the last one.

        Parameters
        ----------
        aggr_type : str
                    Type of aggregation function.
        on : str
             On which attribute to aggregate.
        name : str, optional
               Name of the new column.

        Returns
        -------
        Operators

        """
        if self.operator_list[-1].startswith('.window'):
            self.current_window.aggr_func(aggr_type, on=on, name=name)
            self.operator_list = self.operator_list[:-1]
            self.operator_list.append(self.current_window.create_window_query())
        else:
            raise InvalidSyntaxError("The syntax is incorrect")
        return self

    def union(self, left_stream_name, right_stream):
        """
        This function adds the union operator into the operator_list of this class.

        Parameters
        ----------
        left_stream_name : str
        right_stream : DataStream

        Returns
        -------
        Operators

        """
        complete_query = ""
        left_query = ''.join(self.operator_list)
        # auto cars = Query::from("cars").project(Attribute("f1"));
        complete_query += "auto " + left_stream_name + " = " + left_query + ";\n"
        right_query = ''.join(right_stream.operator.operator_list)
        # auto bikes = Query::from("bikes").project(Attribute("f1"));
        complete_query += "auto " + right_stream.name + " = " + right_query + ";\n"
        # cars.unionWith(bikes)
        complete_query += left_stream_name + ".unionWith(" + right_stream.name + ")"
        self.operator_list = []
        self.operator_list.append(complete_query)
        return self

    def join(self, left_stream_name, right_stream, on=None, left_on=None, right_on=None):
        """
        This function adds the join operator into the operator_list of this class.
        Join works just like JOIN in SQL or the theta join in relational algebra.
        If both of the data streams have an attribute with the same name, we can set the parameter "on".
        Otherwise, we have to set the parameter "left_on" and "right_on".

        Parameters
        ----------
        left_stream_name : str
                           Name of the left stream.
        right_stream : DataStream
                Stream on the right side of the join.
        on : str, optional
             Parameter to join on if they are both the same.
        left_on : str, optional
                  Parameter on the left side to join on in case the parameters to join on are named differently.
        right_on : str, optional
                   Parameter on the right side to join on in case the parameters to join on are named differently.
        Returns
        -------
        Operators

        """
        complete_query = ""
        left_query = ''.join(self.operator_list)
        # auto purchases = Query::from("purchases");
        complete_query += "auto " + left_stream_name + " = " + left_query + ";\n"
        right_query = ''.join(right_stream.operator.operator_list)
        # auto tweets = Query::from("tweets");
        complete_query += "auto " + right_stream.name + " = " + right_query + ";\n"
        # purchases.joinWith(tweets)
        complete_query += left_stream_name + ".joinWith(" + right_stream.name + ")"

        if on is not None:
            complete_query += ".where(Attribute(\"{}${}\")).equalsTo(Attribute(\"{}${}\"))".format(left_stream_name,
                                                                                                   on,
                                                                                                   right_stream.name,
                                                                                                   on)
        elif (left_on is not None) and (right_on is not None):
            complete_query += ".where(Attribute(\"{}${}\")).equalsTo(Attribute(\"{}${}\"))".format(left_stream_name,
                                                                                                   left_on,
                                                                                                   right_stream.name,
                                                                                                   right_on)
        else:
            raise InvalidSyntaxError("No attribute to join on")
        self.operator_list = []
        self.operator_list.append(complete_query)
        return self

    def create_query(self, host, port):
        """
        Creates query by joining all operators and finishing the string with the zmq sink.

        Parameters
        ----------
        host : str
        port : int

        Returns
        -------
        query : str

        """
        query = ''.join(self.operator_list)
        query += ".sink(ZmqSinkDescriptor::create(\"{}\", {}))".format(host, port) + ";"
        return query


class DataStream:
    """
    This class manages the communication with the user and data processing functions.
    """

    def __init__(self, name, connection):
        self.connection = connection
        self.name = name
        self.operator = Operators()
        self.operator.from_stream(name)
        self.key = list()
        self.executed = False
        self.query_id = None

        self.running = False

        self.function = None
        self.process_again = False

        # configs
        self.timeout = 30000
        self.zmq_host = '127.0.0.1'
        self.zmq_port = 8081

    def set_timeout(self, timeout=30000):
        """
        Sets a max timeout for how long the user wants to wait.
        This timeout is the time where not a single record arrives in the python client.

        Parameters
        ----------
        timeout : int

        Returns
        -------

        """
        self.timeout = timeout

    def set_zmq_configs(self, host='127.0.0.1', port=8081):
        """
        This function sets the ZMQ host and port if the default values are different from what the user needs.
        Parameters
        ----------
        host : str
        port : int

        Returns
        -------

        """
        self.zmq_host = host
        self.zmq_port = port

    def __getitem__(self, *args):
        """
        Filter and select in one function.

        Parameters
        ----------
        args :
               If args a list or just one string it will result in select.
               Otherwise when we enter a predicate the filter operator gets called.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> sensor = c.get_logical_stream("sensor")
        >>>
        >>> # Filter
        >>> sensor[sensor["temperature"] > 3]
        >>> sensor[sensor["temperature"] < 3]
        >>> sensor[sensor["temperature"] <= 3]
        >>> sensor[sensor["temperature"] >= 3]
        >>> sensor[sensor["temperature"] == 3]
        >>> sensor[sensor["temperature"] != 3]
        >>> sensor[sensor["temperature"] > sensor["humidity"]
        >>> sensor[(sensor["temperature"] > 3) & (sensor["temperature"] < 15)]
        >>> sensor[(sensor["temperature"] < 3) | (sensor["temperature"] == 10)]

        >>> # Select
        >>> cars["car_id"]
        >>> # or
        >>> cars[["cars_id"]]
        >>> cars[["car_id", "speed", "lat", "lon"]]

        """
        for arg in args:
            if isinstance(arg, tuple) and len(arg) > 1:
                arg = list(arg)
                for a in arg:
                    self.key.append(a)
            elif isinstance(arg, Logical_Operator):
                self.operator.filter(arg)
                return self
            elif isinstance(arg, Wrapper) or isinstance(arg, list):
                self.operator.select(arg)
                return self
            else:
                key = list()
                key.append(arg)
                return Wrapper(key)

        return self

    def __setitem__(self, index, value):
        """
        Map function for the user.

        Parameters
        ----------
        index : str
                Attribute name.
        value : str or int or float
                New value that we want to set the attribute to.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> sensor = c.get_logical_stream("sensor")
        >>>
        >>> sensor["temperature"] = sensor["temperature"] + 0.01
        >>> sensor["temperature"] = sensor["temperature"] - 0.01
        >>> sensor["temperature"] = sensor["temperature"] * 0.01
        >>> sensor["temperature"] = sensor["temperature"] / 0.01
        >>> sensor["temperature"] = (sensor["sensor_a"] + sensor["sensor_b"]) / 2
        >>> sensor["temperature"] = 0.01 * sensor["temperature"]

        """
        if isinstance(value, int) or isinstance(value, float):
            self.operator.map('Attribute(\"{}\") = {}'.format(index, value))
        elif isinstance(value, str) and value.startswith('Attribute'):
            self.operator.map('Attribute(\"{}\") = {}'.format(index, value))
        elif isinstance(value, str):
            self.operator.map('Attribute(\"{}\") = \"{}\"'.format(index, value))
        return self

    def rename(self, columns):
        """
        Renames the attribute name temporarily for the projection.

        Parameters
        ----------
        columns : dict
                  Columns that are renamed.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> cars = c.get_logical_stream("cars")
        >>>
        >>> cars["car_id"]
        >>> cars.rename("id")
        """
        self.operator.rename(columns)
        return self

    # WINDOWS
    def tumbling(self, on=None, event='timestamp', event_unit=None, size=0, size_unit='sec', lateness=0,
                 lateness_unit='sec'):
        """
        Tumbling window. The tumbling window has a length that is determined by the user. The length can
        either be a specific amount of time or a number of tuples. The tumbling window first fills itself up
        until the time or the number of tuples is reached. Then the window omit every tuple and starts filling up
        again. This technique allows to compute aggregation functions continuously on a small section of a
        data stream and in a disjoint fashion.

        Parameters
        ----------
        on : str
             Key for keyed window.
        event : str
                Declares event time (default value is 'timestamp').
        event_unit : str
                     Unit of size, can be min, sec, ms, and count.
        size : int
               Size of the window
        size_unit : str
                    Unit of size, can be min, sec, ms, and count.
        lateness : int
                   Lateness of window
        lateness_unit : str
                        Unit of lateness, can be min, sec, ms, and count.

        Returns
        -------
        DataStream

        Example
        ----------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> shop = c.get_logical_stream("shop")
        >>>
        >>> # keyed window
        >>> shop.tumbling(on="value", size=10, size_unit="sec").sum(on="sales")

        >>> # global window
        >>> shop.tumbling(size=10, size_unit="sec").sum(on="sales")
        """
        w = Windows(name='TumblingWindow', on=on, event=event, event_unit=event_unit, size=size, size_unit=size_unit,
                    lateness=lateness, lateness_unit=lateness_unit)
        self.operator.window(w)
        return self

    def sliding(self, on=None, event='timestamp', event_unit=None, size=0, size_unit='sec', slide=0, slide_unit='sec',
                lateness=0,
                lateness_unit='sec'):
        """
        Sliding window. A sliding window has a fixed length that is determined by the user. This length can either
        be an amount of time or a number of tuples. Furthermore, the sliding window has a slide value. This slide
        value is also determined by the user and tells the window how often it should update the window, in
        particular when the sliding window slides over the data stream.

        Parameters
        ----------

        on : str
             Key for keyed window.
        event : str
                Declares event time (default value is 'timestamp').
        event_unit : str
                     Unit of event. Can be min, sec, ms, and count.
        size : int
               Size of the window.
        size_unit : str
                    Unit of size. Can be min, sec, ms, and count.
        slide : int
                Update frequency of sliding window.
        slide_unit : str
                     Unit of slide, same as size_unit.
        lateness : int
                   Lateness of window.
        lateness_unit : str
                        Unit of lateness. Can be min, sec, ms, and count.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> shop = c.get_logical_stream("shop")
        >>>
        >>> # keyed window
        >>> shop.sliding(on="sales", size=10, size_unit="sec", slide=5, slide_unit="sec").sum(on="sales")

        >>> # global window
        >>> shop.sliding(size=10, size_unit="sec", slide=5, slide_unit="sec").sum(on="sales")

        """
        w = Windows(name='SlidingWindow', on=on, event=event, event_unit=event_unit, size=size, size_unit=size_unit,
                    slide=slide,
                    slide_unit=slide_unit, lateness=lateness, lateness_unit=lateness_unit)
        self.operator.window(w)
        return self

    def sum(self, on="", name=""):
        """
        Aggregation function sum for the window.

        Parameters
        ----------
        on : str
             On which attribute to sum.
        name : str
               How to call the column.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> shop = c.get_logical_stream("shop")
        >>>
        >>> shop.sliding(on="purchases", size=10, size_unit="sec", slide=5, slide_unit="sec")
        >>>     .sum(on="purchases", name="")


        """
        self.operator.aggr_func('Sum', on=on, name=name)
        return self

    def div(self, on="", name=""):
        """
        Aggregation function div for the window.

        Parameters
        ----------
         on : str
              On which attribute to div.
        name : str
              How to call the column.

        Returns
        -------
        DataStream

        """
        self.operator.aggr_func('Div', on=on, name=name)
        return self

    def count(self, on="", name=""):
        """
        Aggregation function count for the window.

        Parameters
        ----------
        on : str
             On which attribute to count.
        name : str, optional
               How to call the column.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> cars = c.get_logical_stream("cars")
        >>>
        >>> cars.sliding(on="color", size=10, size_unit="sec", slide=5, slide_unit="sec").max(on="color", name="")


        """
        self.operator.aggr_func('Count', on=on, name=name)
        return self

    def avg(self, on="", name=""):
        """
        Aggregation function avg for the window.

        Parameters
        ----------
        on : str
             On which attribute to avg.
        name : str, optional
               How to call the column.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> sensor = c.get_logical_stream("sensor")
        >>>
        >>> sensor.sliding(on="temperature", size=10, size_unit="sec", slide=5, slide_unit="sec").avg(on="temperature")


        """
        self.operator.aggr_func('Avg', on=on, name=name)
        return self

    def min(self, on="", name=""):
        """
        Aggregation function min for the window.

        Parameters
        ----------
        on : str
             On which attribute to min.
        name : str, optional
               How to call the column.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> sensor = c.get_logical_stream("sensor")
        >>>
        >>> sensor.sliding(on="temperature", size=10, size_unit="sec", slide=5, slide_unit="sec").min(on="temperature")

        """
        self.operator.aggr_func('Min', on=on, name=name)
        return self

    def max(self, on="", name=""):
        """
        Aggregation function max for the window.

        Parameters
        ----------
        on : str
             On which attribute to max.
        name : str, optional
               How to call the column.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> sensor = c.get_logical_stream("sensor")
        >>>
        >>> sensor.sliding(on="temperature", size=10, size_unit="sec", slide=5, slide_unit="sec").max(on="temperature")

        """
        self.operator.aggr_func('Max', on=on, name=name)
        return self

    def union(self, other_stream):
        """
        Union unites two data streams with the same schema.

        Parameters
        ----------
        other_stream : DataStream

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>>
        >>> bus = c.get_logical_stream("bus")
        >>> cars = c.get_logical_stream("car")
        >>> bus.union(car)

        """
        if isinstance(other_stream, DataStream):
            self.operator.union(self.name, other_stream)
        else:
            raise InvalidSyntaxError("The syntax is incorrect")
        return self

    def join(self, other_stream, on=None, left_on=None, right_on=None):
        """
        Join works just like JOIN in SQL or the theta join in relational algebra.
        If both of the data streams have an attribute with the same name, we can set the parameter "on".
        Otherwise, we have to set the parameter "left_on" and "right_on".

        Parameters
        ----------
        other_stream : DataStream
        on : str, optional
             Common attribute to join on.
        left_on : str, optinal
                  Attribute of the left data stream to join the right attribute with.
        right_on : str, optional
                   Attribute of the right data stream to join the left attribute with.

        Returns
        -------
        DataStream

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> position = c.get_logical_stream("car_position")
        >>> details = c.get_logical_stream("car_details")
        >>> position.join(details, left_on="id", right_on="car_id")

        >>> purchases = get_logical_stream("purchases")
        >>> products = c.get_logical_stream("products")
        >>> purchases.join(products, on="product_id")


        """
        if isinstance(other_stream, DataStream):
            self.operator.join(self.name, other_stream, on, left_on, right_on)
        else:
            raise InvalidSyntaxError("The syntax is incorrect")
        return self

    def create_query(self):
        """
        Creates query string for NebulaStream.

        Returns
        -------
        str

        """
        return self.operator.create_query(self.zmq_host, self.zmq_port)

    def reset_operators(self):
        """
        Deletes all operators that have been called and deletes the current running query.

        Returns
        -------

        """
        self.operator = Operators()
        self.operator.from_stream(self.name)
        self.executed = False
        self.connection.stop_query(self.query_id)
        self.query_id = None

    def execute_query(self, query):
        """
        Executes query in NebulaStream.

        Parameters
        ----------
        query : str
                Translated query for NebulaStream.

        Returns
        -------

        """
        try:
            self.executed = True
            self.query_id = self.connection.execute_query(query, self.operator.strategy)["queryId"]
        except WrongQueryError as e:
            print(e)

    def zmq_sink(self, host, port):
        """
        Zmq sink for NebulaStream.

        Parameters
        ----------
        host : str
               Host where zmq is running
        port : int
               Port of ZMQ. This is not the same as connection with NebulaStream.

        Returns
        -------
        DataStream

        """
        self.zmq_host = host
        self.zmq_port = port
        self.operator.zmq_sink(host, port)
        return self

    def print_sink(self):
        """
        Prints the data in your terminal where NebulaStream is running.

        Returns
        -------
        DataStream

        """
        self.operator.print_sink()
        return self

    def __str__(self):
        """
        Creates a string of the object DataStream.

        Returns
        -------
        str

        """
        query = self.create_query()
        return str(self.execute_query(query))

    def _repr_html_(self):
        """
        Sends query and creates the output.

        Returns
        -------
        str
            This string is a table in HTML.

        """
        stringio = io.StringIO()
        stringio.write('<table border=\"1\" class=\"dataframe\">      <tr style=\"text-align: right;\"> <th></th>')
        return self.get_data_from_nes(stringio=stringio)

    def get_data_from_nes(self, stringio=None, batch_mode=False, timeframe=0, timeframe_unit='sec', on_time_over=False,
                          batch_function=None):
        """
        This function requests data from NebulaStream

        Parameters
        ----------
        stringio : stringio
                   This is a stringio to write the results as an HTML table into it.
        batch_mode : bool
                     Whether this function is called in the batch mode or not.
        timeframe : int
                    Timeframe for when the batch mode is activated.
        timeframe_unit : str
                         Unit for the timeframe. Only accept 'sec', 'min', and 'h'.
        on_time_over : bool
                       When to trigger the batch function. If True then only after the timeframe is reached. Otherwise,
                       every time a tuple enters the buffer in the batch mode.
        batch_function : function
                         The user defined batch function.

        Returns
        -------
        str
            Depending on what was chosen in the parameters it returns the data stream as an HTMl or the result
            of the buffer funtion.


        Notes
        -------
        The response of NebulaStream consists of four messages:
        1 (is when counter == 1) length of 2nd message
        2 schema of data
        3 length of 4th message
        4 data

        Then message 3 and 4 repeat until someone stops the query.

        """
        context = zmq.Context()
        url = "tcp://{}:{}".format(self.zmq_host, self.zmq_port)
        socket = context.socket(zmq.PULL)
        socket.bind(url)

        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)

        query = self.create_query()
        self.execute_query(query)
        self.running = True
        counter = 0

        serializable_schema = pb.SerializableSchema()
        number = 0
        rows = 0
        col = 0
        details = list()
        details_dict = dict()
        batch_buffer = pd.DataFrame()
        batch_result = pd.DataFrame()

        accepted_timeframe_unit = {
            'sec': 1000,
            'min': 60 * 1000,
            'h': 60 * 60 * 1000
        }

        transformed_timeframe = timeframe * accepted_timeframe_unit[timeframe_unit]  # transforms into milliseconds
        start = time.perf_counter()  # measures time in milliseconds

        no_of_elements_arriving = 0

        while self.running:
            try:
                timeout = dict(poller.poll(self.timeout))
                if not timeout:
                    raise KeyboardInterrupt

                else:
                    message = socket.recv()

                    if len(message) > 0:
                        counter += 1
                    if counter == 1:

                        number = int.from_bytes(message[0:4], byteorder='little', signed=True)
                    elif counter == 2:
                        message = message[0:number]
                        serializable_schema.ParseFromString(message)

                        col = len(serializable_schema.fields)  # wie viele Spalten die Tabelle haben wird

                        for i in range(col):
                            if stringio is not None:
                                write_header(stringio, serializable_schema.fields[i].name)

                            det = types_details(serializable_schema.fields[i].type.details.type_url,
                                                serializable_schema.fields[i].type.details.value)
                            details.append(det)

                            details_dict[serializable_schema.fields[i].name] = det
                        if stringio is not None:
                            stringio.write('</tr>')
                            stringio.write('</table>')
                    elif counter == 3 or counter % 2 == 1:
                        if stringio is not None:
                            current_value = stringio.getvalue()
                            current_value = current_value[:-8]  # removes </table>

                            stringio = io.StringIO()
                            stringio.write(current_value)
                        rows = int.from_bytes(message[0:4], byteorder='little', signed=True)

                    else:
                        cols = col + 1  # 2+1
                        byte_length = cols * 4

                        bytes_per_row = how_many_bytes_per_row(details_dict.items())

                        for i in range(rows):
                            one_row_byte = message[i * bytes_per_row:(i + 1) * bytes_per_row]
                            data, dictionary = byte_row_to_string(details, one_row_byte, list(details_dict.keys()))

                            if batch_mode:
                                # adding to batch buffer and assuming order variables don't change
                                batch_buffer = batch_buffer.append(dictionary, ignore_index=True)
                                current_time = time.perf_counter()
                                if on_time_over:
                                    if current_time - start < transformed_timeframe:
                                        continue
                                    else:
                                        batch_result = self.process_in_batches_with_dataframe(
                                            batch_function=batch_function, data_frame=batch_buffer,
                                            batch_result=batch_result)
                                        # remove this line if we don't want want to compute over one batch only
                                        start = time.perf_counter()
                                        batch_buffer = pd.DataFrame()
                                else:
                                    batch_result = self.process_in_batches_with_dataframe(
                                        batch_function=batch_function, data_frame=batch_buffer,
                                        batch_result=batch_result)
                                    if current_time - start >= transformed_timeframe:
                                        start = time.perf_counter()
                                        batch_buffer = pd.DataFrame()
                            elif not (self.function is None):
                                result = self.function(dictionary)
                                if result is not None:
                                    data = list(result.values())
                                else:
                                    continue
                            if stringio is not None:
                                write_data(stringio, data, (i + no_of_elements_arriving))
                        if stringio is not None:
                            stringio.write('</table>')
                            no_of_elements_arriving += rows
                            display(HTML(stringio.getvalue()))
                            clear_output(wait=True)
            except KeyboardInterrupt:
                if batch_mode:
                    batch_result = self.process_in_batches_with_dataframe(batch_function=batch_function,
                                                                           data_frame=batch_buffer,
                                                                           batch_result=batch_result)
                self.stop_query()
                socket.close(0)
                context.destroy(0)
                context.term()
        if stringio is not None:
            return stringio.getvalue()
        elif batch_mode:
            return batch_result

    def process_in_batches_with_dataframe(self, batch_function, data_frame, batch_result):
        """
        This function computes the batch function on the created batch.

        Parameters
        ----------
        batch_function : function
        data_frame : DataFrame
        batch_result : pandas dataframe

        Returns
        -------
        DataFrame
        """
        result_from_this_batch = batch_function(data_frame)
        if isinstance(result_from_this_batch, pd.DataFrame):
            batch_result = batch_result.append(result_from_this_batch)
            return batch_result
        elif isinstance(result_from_this_batch, pd.Series):
            batch_result = batch_result.append(result_from_this_batch, ignore_index=True)
            return batch_result
        else:
            raise InvalidSyntaxError("There is no return in the batch function or the type of the function is not a "
                                     "DataFrame or Series.")


    def stop_query(self):
        """
        This function stops a query. Once a query is stopped it cannot rerun again. The user has to run a new
        query.

        Returns
        -------

        """
        self.running = False
        self.connection.stop_query(self.query_id)

    def process(self, function):
        """
        This function enables user to compute their own defined python function (one tuple at a time).

        Parameters
        ----------
        function : function
                   Function that can process one tuple at a time.

        Returns
        -------

        Examples
        -------
        >>> c = nes.Connection("127.0.0.1", 8081)
        >>> data_stream = c.get_logical_stream("data_stream")
        >>>
        >>> def myfunction(data):
        >>>     #do something with a single tuple
        >>>     return data
        >>> data_stream.process(myfunction)

        """
        self.function = function

    def batch(self, batch_function, timeframe=10, timeframe_unit='min', on_time_over=True):
        """

        Parameters
        ----------
        batch_function : function
                         User defined batch function. This function has to return the desired results.
        timeframe : int
                    Defines the timeframe over which the stream is buffered.
        timeframe_unit : str
                         Unit of the timeframe.
        on_time_over : bool
                       Defines when the batch function is called.
                       If this value is True we call the batch function once the time is up.
                       Otherwise, is this value is False we call the batch function when a new record is
                       added to the buffer onChange.

        Returns
        -------

        Examples
        -------
        >>> def calculate_mean_for_all_columns(data_frame):
        >>>     return data_frame.mean()
        >>> cars.batch(calculate_mean_for_all_columns, timeframe=10, timeframe_unit='min', on_time_over=True)

        """
        all_timeframe_units = ['sec', 'min', 'h']
        if timeframe_unit in all_timeframe_units:
            return self.get_data_from_nes(batch_mode=True,
                                          timeframe=timeframe,
                                          timeframe_unit=timeframe_unit,
                                          on_time_over=on_time_over,
                                          batch_function=batch_function)
        else:
            raise InvalidSyntaxError("Invalid Syntax! This unit does not exist. ")


class Wrapper:
    """
    Wrapper has all the necessary functions to perform mathematical and logical operators
    it therefore wraps the values into LogicalOperator, which creates the correct string.
    This class is mainly needed to distinguish between filter and select.
    """

    def __init__(self, key):
        self.key = key

    def __lt__(self, other):
        """
        Manages '<' of DataStream.

        Parameters
        ----------
        other : int or float or DataStream
                If we have, e.g., DataStream["attribute"] < 1 then other is the 1. It is just the data type that is not
                DataStream.

        Returns
        -------
        str

        """
        if len(self.key) == 1 and isinstance(self.key[0], str):
            if isinstance(other, int):
                return Logical_Operator(self.key[0]) < Logical_Operator(str(other))
            elif isinstance(other, float):
                return Logical_Operator(self.key[0]) < Logical_Operator(str(other))
            elif isinstance(other, DataStream):
                return Logical_Operator(self.key[0]) < Logical_Operator(other.key[0])
            else:
                raise InvalidSyntaxError("The syntax is incorrect")

    def __le__(self, other):
        """
        Manages '<=' of DataStream.

        Parameters
        ----------
        other : int or float or DataStream
                If we have, e.g., DataStream["attribute"] <= 1 then other is the 1. Itis just the data type that is not
                DataStream.

        Returns
        -------
        str

        """
        if len(self.key) == 1 and isinstance(self.key[0], str):
            if isinstance(other, int):
                return Logical_Operator(self.key[0]) <= Logical_Operator(str(other))
            elif isinstance(other, DataStream):
                return Logical_Operator(self.key[0]) <= Logical_Operator(other.key[0])
            else:
                raise InvalidSyntaxError("The syntax is incorrect")

    def __eq__(self, other):
        """
        Manages '==' of DataStream.

        Parameters
        ----------
        other : int or float or DataStream
                If we have, e.g., DataStream["attribute"] == 1 then other is the 1. It is just the data type that is not
                DataStream.

        Returns
        -------
        str

        """
        if len(self.key) == 1 and isinstance(self.key[0], str):
            if isinstance(other, int):
                return Logical_Operator(self.key[0]) == Logical_Operator(str(other))
            elif isinstance(other, DataStream):
                return Logical_Operator(self.key[0]) == Logical_Operator(other.key[0])
            else:
                raise InvalidSyntaxError("The syntax is incorrect")

    def __ne__(self, other):
        """
        Manages '!=' of DataStream.

        Parameters
        ----------
        other : int or float or DataStream
                If we have, e.g., DataStream["attribute"] != 1 then other is the 1. It is just the data type that is not
                DataStream.

        Returns
        -------
        str

        """
        if len(self.key) == 1 and isinstance(self.key[0], str):
            if isinstance(other, int):
                return Logical_Operator(self.key[0]) != Logical_Operator(str(other))
            elif isinstance(other, DataStream):
                return Logical_Operator(self.key[0]) != Logical_Operator(other.key[0])
            else:
                raise InvalidSyntaxError("The syntax is incorrect")

    def __ge__(self, other):
        """
        Manages '>=' of DataStream.

        Parameters
        ----------
        other: int or float or DataStream
               If we have, e.g., DataStream["attribute"] >= 1 then other is the 1. It is just the data type that is not
               DataStream.


        Returns
        -------
        str

        """
        if len(self.key) == 1 and isinstance(self.key[0], str):
            if isinstance(other, int):
                return Logical_Operator(self.key[0]) >= Logical_Operator(str(other))
            elif isinstance(other, DataStream):
                return Logical_Operator(self.key[0]) >= Logical_Operator(other.key[0])
            else:
                raise InvalidSyntaxError("The syntax is incorrect")

    def __gt__(self, other):
        """
        Manages '>' of DataStream.

        Parameters
        ----------
        other : int or float or DataStream
                If we have, e.g., DataStream["attribute"] > 1 then other is the 1. It is just the data type that is not
                DataStream.


        Returns
        -------
        str

        """
        if len(self.key) == 1 and isinstance(self.key[0], str):
            if isinstance(other, int):
                return Logical_Operator(self.key[0]) > Logical_Operator(str(other))
            elif isinstance(other, DataStream):
                return Logical_Operator(self.key[0]) > Logical_Operator(other.key[0])
            else:
                raise InvalidSyntaxError("The syntax is incorrect")

    def __add__(self, other):
        """
        Manages '+' of DataStream.

        Parameters
        ----------
        other :
                If we have, e.g., DataStream["attribute"] + 1 then other is the 1. It is just the data type that is not DataStream
                other is always on the right hand side.

        Returns
        -------
        str

        """
        if isinstance(other, Wrapper) and (isinstance(other.key, list)) and len(other.key) == 1:
            other = "Attribute(\"" + other.key[0] + "\")"
        return self.map_to_string() + " + " + str(other)

    def __radd__(self, other):
        """
        Opposite of __add__.
        Whenever other is on the left hand side.

        Parameters
        ----------
        other

        Returns
        -------
        Wrapper

        """
        return self.__add__(other)

    def __sub__(self, other):
        """
        Manages '-' of DataStream.

        Parameters
        ----------
        other :
                If we have, e.g., DataStream["attribute"] - 1 then other is the 1. Iis just the data type that is not DataStream
                other is always on the right hand side.

        Returns
        -------
        str

        """
        if isinstance(other, Wrapper) and (isinstance(other.key, list)) and len(other.key) == 1:
            other = "Attribute(\"" + other.key[0] + "\")"
        return self.map_to_string() + " - " + str(other)

    def __rsub__(self, other):
        """
        Opposite of __sub__.
        Whenever other is on the left hand side.

        Parameters
        ----------
        other

        Returns
        -------
        Wrapper

        """
        return self.__sub__(other)

    def __mul__(self, other):
        """
        Manages '*' of DataStream.

        Parameters
        ----------
        other :
                If we have, e.g., DataStream["attribute"] * 1 then other is the 1. It is just the data type that is not DataStream
                other is always on the right hand side.

        Returns
        -------
        str

        """
        if isinstance(other, Wrapper) and (isinstance(other.key, list)) and len(other.key) == 1:
            other = "Attribute(\"" + other.key[0] + "\")"
        return self.map_to_string() + " * " + str(other)

    def __rmul__(self, other):
        """
        Opposite of __mul__.
        Whenever other is on the left hand side.

        Parameters
        ----------
        other

        Returns
        -------
        Wrapper

        """
        return self.__mul__(other)

    def __truediv__(self, other):
        """
        Manages '/' of DataStream.

        Parameters
        ----------
        other :
                If we have, e.g., DataStream["attribute"] / 1 then other is the 1. It is just the data type that is not DataStream
                other is always on the right hand side.

        Returns
        -------
        str

        """
        if isinstance(other, Wrapper) and (isinstance(other.key, list)) and len(other.key) == 1:
            other = "Attribute(\"" + other.key[0] + "\")"
        return self.map_to_string() + " / " + str(other)

    def __rtruediv__(self, other):
        """
        Opposite of __truediv__.
        Whenever other is on the left hand side.

        Parameters
        ----------
        other

        Returns
        -------
        Wrapper

        """
        return self.__truediv__(other)

    def __mod__(self, other):
        """
        Manages '%' of DataStream.

        Parameters
        ----------
        other :
                If we have, e.g., DataStream["attribute"] % 10 then other is the 10. It is just the data type that is not DataStream
                other is always on the right hand side.

        Returns
        -------
        str

        """
        if isinstance(other, Wrapper) and (isinstance(other.key, list)) and len(other.key) == 1:
            other = "Attribute(\"" + other.key[0] + "\")"
        return self.map_to_string() + " % " + str(other)

    def __rmod__(self, other):
        """
        Opposite of __mod__.
        Whenever other is on the left hand side.

        Parameters
        ----------
        other

        Returns
        -------
        Wrapper

        """
        return self.__mod__(other)

    def map_to_string(self):
        """
        This function just creates "Attribute("attribute") && Attribute("attribute2")" string.

        Returns
        -------
        s : str

        """
        s = ""
        for k in self.key:
            s += "Attribute(\"" + k + "\") && "
        s = s[:-4]
        return s


class Logical_Operator:
    """
    Creates the strings of the logical operators.
    """

    def __init__(self, value):
        self.value = value

    def __lt__(self, other):
        """
        Creates a string that looks the following: current_value < other_value.

        Parameters
        ----------
        other : str

        Returns
        -------
        str

        """
        return self.create_string(self.value, other, "<")

    def __gt__(self, other):
        """
        Creates a string that looks the following: current_value > other_value.

        Parameters
        ----------
        other : str

        Returns
        -------
        str

        """
        return self.create_string(self.value, other, ">")

    def __le__(self, other):
        """
        Creates a string that looks the following: current_value <= other_value.

        Parameters
        ----------
        other : str

        Returns
        -------
        str

        """
        return self.create_string(self.value, other, "<=")

    def __eq__(self, other):
        """
        Creates a string that looks the following: current_value == other_value.

        Parameters
        ----------
        other : str

        Returns
        -------
        str

        """
        return self.create_string(self.value, other, "==")

    def __ne__(self, other):
        """
        Creates a string that looks the following: current_value != other_value.

        Parameters
        ----------
        other : str

        Returns
        -------
        str

        """
        return self.create_string(self.value, other, "!=")

    def __ge__(self, other):
        """
        Creates a string that looks the following: current_value >= other_value.

        Parameters
        ----------
        other : str

        Returns
        -------
        str

        """
        return self.create_string(self.value, other, ">=")

    def __and__(self, other):
        """
        Creates a string that looks the following: current_value && other_value.

        Parameters
        ----------
        other : str

        Returns
        -------
        lo : Logical_Operator

        """
        # both are Logical operators
        value = self.value + " && " + other.value
        lo = Logical_Operator(value)
        return lo

    def __or__(self, other):
        """
        Creates a string that looks the following: current_value || other_value.

        Parameters
        ----------
        other : str

        Returns
        -------
        lo : Logical_Operator

        """
        # both are Logical operators
        value = self.value + " || " + other.value
        lo = Logical_Operator(value)
        return lo

    def __str__(self):
        """
        String representation of Logical_Operator.

        Returns
        -------
        self.value : str

        """
        return self.value

    def create_string(self, value, other, operator):
        """
        Creates a string that looks the following: current_value operator other_value.
        Operator can be any logical operator.

        Parameters
        ----------
        value : str
        other : str
        operator : str

        Returns
        -------
        logical_operator : Logical_Operator

        """
        if isinstance(other, Logical_Operator):
            value = "(Attribute(\"" + value + "\") " + operator + " " + other.value + ")"
            logical_operator = Logical_Operator(value)
            return logical_operator
        elif isinstance(other, int):
            value = "(Attribute(\"" + value + "\") " + operator + " " + str(other) + ")"
            logical_operator = Logical_Operator(value)
            return logical_operator


class Windows:
    """
    manages the strings we create in DataStream.
    """

    def __init__(self, name, on=None, event='timestamp', event_unit='sec', size=0, size_unit='sec', slide=0,
                 slide_unit='sec', lateness=0,
                 lateness_unit='sec'):
        self.name = name
        self.on = on
        self.event = event
        self.event_unit = event_unit
        self.size = size
        self.size_unit = size_unit
        self.slide = slide
        self.slide_unit = slide_unit
        self.lateness = lateness
        self.lateness_unit = lateness_unit
        self.aggregation = list()

    def aggr_func(self, agg_type, on, name=""):
        """
        Creates the string for any aggregation function.

        Parameters
        ----------
        agg_type : str
                   Name of aggregation.
        on : str
             On which attribute to aggregate.
        name : str
               How to call the aggregation column.

        Returns
        -------
        self

        """
        # Sum(Attribute("f2")
        agg_query = ".apply({}())".format(agg_type)
        if len(on) > 0:
            agg_query = ".apply({}(Attribute(\"{}\")))".format(agg_type, on)
        if len(name) != 0:
            agg_query += ".as(Attribute(\"{}\"))".format(name)
        self.aggregation.append(agg_query)
        return self

    def create_window_query(self):
        """
        Creates all different string representation of windows.

        Returns
        -------
        query : str
                This is the window operator as a string.

        Notes
        -------
        From the NebulaStream documentation:

        Global Window
        stream.window(TumblingWindow::of(EventTime(Attribute("timestamp")), Seconds(10)))
                        .apply(Sum(Attribute("f2")));

        Tumbling window
        stream.window(TumblingWindow::of(EventTime(Attribute("timestamp")), Seconds(10)))
                        .byKey(Attribute("f2"))
                        .apply(Sum(Attribute("f2")));

        Sliding window with window size of 10 ms and slide size 5 ms
        stream.window(SlidingWindow::of(EventTime(Attribute("timestamp")), Milliseconds(10), Milliseconds(5)))
                        .byKey(Attribute("f2"))
                        .apply(Sum(Attribute("f2")));

        Aggregation field naming
        stream.window(TumblingWindow::of(EventTime(Attribute("timestamp")), Seconds(10)))
                        .byKey(Attribute("f2"))
                        .apply(Sum(Attribute("f2")))
                        .as(Attribute("sum_f2"));
        stream.window(TumblingWindow::of(EventTime(Attribute("timestamp")), Seconds(10)))
                        .byKey(Attribute("f2"))
                        .apply(Max(Attribute("f2")))
                        .as(Attribute("max_f2"));
        stream.window(TumblingWindow::of(EventTime(Attribute("timestamp")), Seconds(10)))
                        .byKey(Attribute("f2"))
                        .apply(Min(Attribute("f2")))
                        .as(Attribute("min_f2"));
        stream.window(TumblingWindow::of(EventTime(Attribute("timestamp")), Seconds(10)))
                        .byKey(Attribute("f2"))
                        .apply(Count())
                        .as(Attribute("count_f2"));

        Keyed window
        stream.window(TumblingWindow::of(EventTime(Attribute("timestamp")), Seconds(10)))
                        .byKey(Attribute("f2"))
                        .apply(Sum(Attribute("f2")));

        Specify timestamp unit
        stream.window(TumblingWindow::of(EventTime(Attribute("timestamp"), Seconds()), Seconds(10)))
                        .byKey(Attribute("f2"))
                        .apply(Sum(Attribute("f2")));

        """
        size_units_options = {
            "count": "Count",
            "sec": "Seconds",
            "ms": "Milliseconds",
            "min": "Minutes"
        }
        transformed_event_unit = ""
        if self.event_unit is not None:
            transformed_event_unit = ', ' + size_units_options[self.event_unit] + '()'

        # window.(TumblingWindow::of(
        query = '.window({}::of(EventTime(Attribute(\"{}\"){}), '.format(self.name, self.event, transformed_event_unit)
        if self.size >= 0:
            # Seconds(10)
            query += '{}({})'.format(size_units_options[self.size_unit], self.size)
        if self.name == "SlidingWindow" and self.slide > 0:
            # , Milliseconds(5)
            query += ', {}({})'.format(size_units_options[self.slide_unit], self.slide)
        if self.lateness > 0:
            # Lateness(Seconds(10))
            query += ', Lateness({}({}))'.format(size_units_options[self.lateness_unit], self.lateness)
        query += '))'  # end ) of "WindowType::of()

        if (self.on is not None) and isinstance(self.on, str):
            # .windowByKey(Attribute("f2"), TumblingWindow::of(EventTime(Attribute("timestamp")),
            query += '.byKey(Attribute(\"{}\"))'.format(self.on)

        query += ' '.join(self.aggregation)
        return query
