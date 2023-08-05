"""
Unpublished work.
Copyright (c) 2021 by Teradata Corporation. All rights reserved.
TERADATA CORPORATION CONFIDENTIAL AND TRADE SECRET

Primary Owner: pradeep.garre@teradata.com
Secondary Owner: PankajVinod.Purandare@teradata.com

This file implements the core framework that allows user to execute any Vantage Window Functions.
"""

from teradataml.utils.validators import _Validators
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes


class Window:
    """ A class for executing window functions. """
    def __init__(self,
                 object,
                 partition_columns=None,
                 order_columns=None,
                 sort_ascending=True,
                 nulls_first=None,
                 window_start_point=None,
                 window_end_point=None,
                 ignore_window=False):
        """
        DESCRIPTION:
            Constructor for Window class.

        PARAMETERS:
            object:
                Required Argument.
                Specifies where the window object is initiated from.
                Window object can be initiated from either teradataml DataFrame
                or a column in a teradataml DataFrame.
                Types: teradataml DataFrame, _SQLColumnExpression

            partition_columns:
                Optional Argument.
                Specifies the name(s) of the column(s) over which the ordered
                aggregate function executes by partitioning the rows.
                Such a grouping is static.
                Note:
                    If this argument is not specified, then the entire data
                    from teradataml DataFrame, constitutes a single partition,
                    over which the ordered aggregate function executes.
                Types: str OR list of Strings (str)

            order_columns:
                Optional Argument.
                Specifies the name(s) of the column(s) to order the rows in a
                partition, which determines the sort order of the rows over
                which the function is applied.
                Types: str OR list of Strings (str)

            sort_ascending:
                Optional Argument.
                Specifies whether column ordering should be in ascending or
                descending order.
                Default Value: True (ascending)
                Note:
                    When "order_columns" argument is not specified, argument
                    is ignored.
                Types: bool

            nulls_first:
                Optional Argument.
                Specifies whether null results are to be listed first or last
                or scattered.
                Default Value: None
                Note:
                    When "order_columns" argument is not specified, argument is
                    ignored.
                Types: bool

            window_start_point:
                Optional Argument.
                Specifies a starting point for a window. Based on the integer
                value, n, starting point of the window is decided.
                    * If 'n' is negative, window start point is n rows
                      preceding the current row/data point.
                    * If 'n' is positive, window start point is n rows
                      following the current row/data point.
                    * If 'n' is 0, window start at current row itself.
                    * If 'n' is None, window start as Unbounded preceding,
                      i.e., all rows before current row/data point are
                      considered.
                Note:
                    Value passed to this should always satisfy following condition:
                    window_start_point <= window_end_point
                Default Value: None
                Types: int

            window_end_point:
                Optional Argument.
                Specifies an end point for a window. Based on the integer value,
                n, starting point of the window is decided.
                    * If 'n' is negative, window end point is n rows preceding
                      the current row/data point.
                    * If 'n' is positive, window end point is n rows following
                      the current row/data point.
                    * If 'n' is 0, window end's at current row itself.
                    * If 'n' is None, window end's at Unbounded following,
                      i.e., all rows before current row/data point are
                      considered.
                Note:
                    Value passed to this should always satisfy following condition:
                    window_start_point <= window_end_point
                Default Value: None
                Types: int

            ignore_window:
                Optional Argument.
                Specifies a flag to ignore parameters related to creating
                window ("window_start_point", "window_end_point") and use other
                arguments, if specified.
                When set to True, window is ignored, i.e., ROWS clause is not
                included.
                When set to False, window will be created, which is specified
                by "window_start_point" and "window_end_point" parameters.
                Default Value: False
                Types: bool

        RAISES:
            TypeError OR ValueError

        EXAMPLES:
            # Create a Window from a teradataml DataFrame.
            from teradataml import *
            load_example_data("dataframe","sales")
            df = DataFrame.from_table('sales')
            window = Window(object = df)

            # Create a window from a teradataml DataFrame column.
            window = Window(object = df.Feb)
        """
        self.__object = object
        self.__partition_columns = partition_columns
        self.__order_columns = order_columns
        self.__sort_ascending = sort_ascending
        self.__nulls_first = nulls_first
        self.__window_start_point = window_start_point
        self.__window_end_point = window_end_point
        self.__ignore_window = ignore_window

        from teradataml.dataframe.dataframe import DataFrame
        from teradataml.dataframe.sql import _SQLColumnExpression

        awu_matrix = []
        awu_matrix.append(["object", object, False, (DataFrame, _SQLColumnExpression)])
        awu_matrix.append(["partition_columns", partition_columns, True, (str, list), True])
        awu_matrix.append(["order_columns", order_columns, True, (str, list), True])
        awu_matrix.append(["sort_ascending", sort_ascending, True, bool])
        awu_matrix.append(["nulls_first", nulls_first, True, (bool, type(None))])
        awu_matrix.append(["window_start_point", window_start_point, True, int])
        awu_matrix.append(["window_end_point", window_end_point, True, int])
        awu_matrix.append(["ignore_window", ignore_window, True, bool])

        # Validate argument types
        _Validators._validate_function_arguments(awu_matrix)

        # Check "window_end_point" is always greater than or equal to "window_start_point".
        if window_start_point is not None and window_end_point is not None and\
                window_start_point > window_end_point:
            raise ValueError(Messages.get_message(MessageCodes.INT_ARGUMENT_COMPARISON,
                                                  "window_end_point",
                                                  "greater than or equal",
                                                  "window_start_point"))

        self.__is_window_on_tdml_column = isinstance(self.__object, _SQLColumnExpression)

        # Check whether columns mentioned in "partition_columns" are existed in
        # teradataml DataFrame or not.
        if partition_columns:
            self.__validate_window_columns(partition_columns, "partition_columns")

        # Check whether columns mentioned in "order_columns" are existed in
        # teradataml DataFrame or not.
        if order_columns:
            self.__validate_window_columns(order_columns, "order_columns")

    def __repr__(self):
        """
        DESCRIPTION:
            String representation of Window Object.

        RETURNS:
            str.

        RAISES:
            None.

        EXAMPLES:
            # Create a Window from a teradataml DataFrame.
            from teradataml import *
            load_example_data("dataframe","sales")
            df = DataFrame.from_table('sales')
            window = Window(object = df)
            print(window)

        """
        return "Window [partition_columns={}, order_columns={}, sort_ascending={}, nulls_first={}, " \
               "window_start_point={}, window_end_point={}, ignore_window={}]".format(self.__partition_columns,
                                                                                      self.__order_columns,
                                                                                      self.__sort_ascending,
                                                                                      self.__nulls_first,
                                                                                      self.__window_start_point,
                                                                                      self.__window_end_point,
                                                                                      self.__ignore_window)

    def __getattr__(self, item):
        """
        DESCRIPTION:
            Magic Method to call the corresponding window function.
            Window class do not implement the exact methods but whenever any attribute
            is referred by Window Object, this function gets triggered.
            Based on the input method, corresponding expression is processed.

        PARAMETERS:
            item:
                Required Argument.
                Name of the window function.
                Types: str

        RETURNS:
            A function, which actually process the corresponding SQL window function.

        EXAMPLES:
            # Create a window from a teradataml DataFrame.
            from teradataml import *
            load_example_data("dataframe","sales")
            df = DataFrame.from_table('sales')
            window = Window(object = df)
            window.mean()
        """
        # TODO: validations will be implemented with ELE-3834 .
        return lambda *args, **kwargs: \
            self.__process_window_aggregates(item, args, kwargs)

    def __process_window_aggregates(self, func_name, *args, **kwargs):
        """
        Description:
            Function to process the window expression. All window functions are actually
            processed in this function and generates a DataFrame or _SQLColumnExpression
            according to the Window class.

        PARAMETERS:
            func_name:
                Required Argument.
                Specifies the name of the window function.
                Types: str

            args:
                Optional Argument.
                Specifies the positional arguments to be passed to the window function.
                Types: Tuple

            kwargs:
                Optional Argument.
                Specifies the keyword arguments to be passed to the window function.
                Types: Dictionary

        RETURNS:
            Either a new teradataml DataFrame or an _SQLColumnExpression, according to Window class.

        EXAMPLES:
            # Create a Window from a teradataml DataFrame.
            from teradataml import *
            load_example_data("dataframe","sales")
            df = DataFrame.from_table('sales')
            window = Window(object = df)
            window.__process_window_aggregates("mean")
        """

        # TODO: this method will be implemented with ELE-3014 .

        pass

    def __validate_window_columns(self, columns_in_window, window_arg_name):
        """
        DESCRIPTION:
            Validates, whether the columns mentioned in Window class is
            available in teradataml DataFrame or not.

        PARAMETERS:
            columns_in_window:
                Required Argument.
                Specifies the column names mentioned in either
                "partition_columns" or "order_columns".
                Types: str OR list of Strings (str)

            window_arg_name:
                Required Argument.
                Specifies the name of the argument which is being validated.
                Types: str

        RAISES:
            ValueError

        RETURNS:
            None

        EXAMPLES:
            # Create a Window from a teradataml DataFrame.
            from teradataml import *
            load_example_data("dataframe","sales")
            df = DataFrame.from_table('sales')
            window = Window(object = df)
            window.__validate_window_columns("Feb", "partition_columns")
            window.__validate_window_columns("Feb", "order_columns")
        """
        if self.__is_window_on_tdml_column:
            _Validators._validate_columnexpression_dataframe_has_columns(columns_in_window,
                                                                         window_arg_name,
                                                                         self.__object
                                                                         )
        else:
            _Validators._validate_dataframe_has_argument_columns(columns_in_window,
                                                                 window_arg_name,
                                                                 self.__object,
                                                                 'teradataml'
                                                                 )
