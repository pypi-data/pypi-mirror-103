#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Mounika Kotha (mounika.kotha@teradata.com)
# 
# Version: 1.2
# Function Version: 1.8
# 
# ################################################################## 

import inspect
import time
from teradataml.common.wrapper_utils import AnalyticsWrapperUtils
from teradataml.common.utils import UtilFuncs
from teradataml.context.context import *
from teradataml.dataframe.dataframe import DataFrame
from teradataml.common.aed_utils import AedUtils
from teradataml.analytics.analytic_query_generator import AnalyticQueryGenerator
from teradataml.common.exceptions import TeradataMlException
from teradataml.common.messages import Messages
from teradataml.common.messagecodes import MessageCodes
from teradataml.common.constants import TeradataConstants
from teradataml.dataframe.dataframe_utils import DataFrameUtils as df_utils
from teradataml.options.display import display
from teradataml.analytics.mle.ScaleMap  import ScaleMap 

class Scale:
    
    def __init__(self,
        object = None,
        data = None,
        method = None,
        scale_global = False,
        accumulate = None,
        multiplier = 1.0,
        intercept = "0",
        input_columns = None,
        object_sequence_column = None,
        data_sequence_column = None,
        object_order_column = None,
        data_order_column = None):
        """
        DESCRIPTION:
            The Scale function uses statistical information from the ScaleMap
            function to scale the input data set.


        PARAMETERS:
            object:
                Required Argument.
                Specifies the teradataml DataFrame containing statistic input
                generated by ScaleMap or instance of ScaleMap.

            object_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            data:
                Required Argument.
                Specifies the input teradataml DataFrame for scale function.

            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple
                columns are used for ordering.
                Types: str OR list of Strings (str)

            method:
                Required Argument.
                Specify one or more methods used to scale the dataset. If you specify multiple methods,
                the output teradataml DataFrame includes the column scalemethod
                (which contains the method name) and a row for each input-row/method combination.
                Permitted Values: MEAN, SUM, USTD, STD, RANGE, MIDRANGE, MAXABS.
                Types: str or list of Strings (str)

            scale_global:
                Optional Argument.
                Specifies whether all input columns are scaled to the same location
                and scale. (Each input column is scaled separately).
                Default Value: False
                Types: bool

            accumulate:
                Optional Argument.
                Specifies the input teradataml DataFrame columns to copy to the
                output table. By default, the function copies no input teradataml
                DataFrame columns to the output table.
                Types: str OR list of Strings (str)

            multiplier:
                Optional Argument.
                Specifies one or more multiplying factors to apply to the input
                variables-multiplier in the following formula:
                    X' = intercept + multiplier * (X - location)/scale
                If you specify only one multiplier, it applies to all columns specified
                by the input_columns argument. If you specify multiple multiplying factors,
                each multiplier applies to the corresponding input column. For example, the first multiplier
                applies to the first column specified by the input_columns argument,
                the second multiplier applies to the second input column, and so on.
                Default Value: 1.0
                Types: float OR list of floats

            intercept:
                Optional Argument.
                Specifies one or more addition factors incrementing the scaled
                results-intercept in the following formula:
                    X' = intercept + multiplier * (X - location)/scale
                If you specify only one intercept, it applies to all columns specified
                by the input_columns argument. If you specify multiple addition factors,
                each intercept applies to the corresponding input column.
                The syntax of intercept is:
                [-]{number | min | mean | max }
                where min, mean, and max are the scale_global minimum,
                maximum, mean values in the corresponding columns.
                The function scales the values of min, mean, and max.
                The formula for computing the scaled scale_global minimum is:
                    scaledmin = (minX - location)/scale
                The formulas for computing the scaled scale_global mean and maximum
                are analogous to the preceding formula.
                For example, if intercept is "- min" and multiplier is 1,
                the scaled result is transformed to a nonnegative sequence according
                to this formula, where scaledmin is the scaled value:
                    X' = -scaledmin + 1 * (X - location)/scale.
                Default Value: "0"
                Types: str or list of Strings (str)

            input_columns:
                Optional Argument.
                Specifies the input teradataml DataFrame columns that contain the
                attribute values of the samples. The attribute values must be numeric
                values between -1e308 and 1e308. If a value is outside this range,
                the function treats it as infinity.
                The default input columns are all columns of the statistic teradataml DataFrame
                (of the ScaleMap function) except stattype.
                Types: str OR list of Strings (str)

            object_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "object". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

        RETURNS:
            Instance of Scale.
            Output teradataml DataFrames can be accessed using attribute
            references, such as ScaleObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result


        RAISES:
            TeradataMlException

        EXAMPLES:
            # Load example data.
            # The table 'scale_housing' and 'scale_housing_test' contains house properties
            # like the number of bedrooms, lot size, the number of bathrooms, number of stories etc.
            # The table 'scale_stat' is the statistic data(genererated by ScaleMap function) of the scale_housing data.
            load_example_data("scalemap", "scale_housing")
            load_example_data("scale", ["scale_stat", "scale_housing_test"])

            # Create teradataml DataFrame objects.
            scale_housing = DataFrame.from_table("scale_housing")
            scale_housing_test = DataFrame.from_table("scale_housing_test")
            scale_stat = DataFrame.from_table("scale_stat")

            # Example 1 - This example scales (normalizes) input data using the
            # midrange method and the default values for the arguments Intercept
            # and Multiplier (0 and 1, respectively).
            scale_map_out = ScaleMap(data = scale_housing,
                                     input_columns = ['price','lotsize','bedrooms','bathrms','stories']
                                    )

            scale_out1 = Scale(object=scale_map_out,
                                      data=scale_housing,
                                      method="midrange",
                                      accumulate="id"
                                     )
            # Print the result DataFrame
            print(scale_out1)

            # Example 2 - This example uses a teradataml DataFrame as input for object argument and
            # the Intercept argument has the value "-min" (where min is the scale_global minimum value)
            # and we also specify different Multiplier values for corresponding columns.
            scale_out2 = Scale(object = scale_stat,
                              data = scale_housing,
                              method = "midrange",
                              accumulate = "id",
                              multiplier = [1.0,2.0,3.0,4.0,5.0],
                              intercept = "-min"
                             )

            # Print the result DataFrame
            print(scale_out2)

            # Example 3 - This example uses the statistics created by ScaleMap on a training data set
            # (scale_housing) and then uses these statistics to scale a similar
            # test data set(scale_housing_test).
            scale_out3 = Scale(object = scale_stat,
                                      data = scale_housing_test,
                                      method = "midrange",
                                      accumulate = "id"
                                     )

            # Example 4 - This example uses the Scale function to scale data (using
            # the maxabs method) before inputting it to the function KMeans, which
            # outputs the centroids of the clusters in the dataset.
            load_example_data("KMeans", "computers_train1")
            computers_train1 = DataFrame.from_table("computers_train1")

            scale_map_out4 = ScaleMap(data=computers_train1,
                                                    input_columns=['price','speed','hd','ram'],
                                                    miss_value='OMIT'
                                                   )

            scale_out4 = Scale(object=scale_map_out4,
                                             data=computers_train1,
                                             method="maxabs",
                                             accumulate="id"
                                            )
            # Use the scaled data as input to KMeans to get clusters
            kmeans_out = KMeans(data = scale_out4.result,
                                        centers = 8,
                                        iter_max = 10,
                                        threshold = 0.05
                                       )
            # Print the result DataFrame
            print(kmeans_out)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.object  = object 
        self.data  = data 
        self.method  = method 
        self.scale_global  = scale_global 
        self.accumulate  = accumulate 
        self.multiplier  = multiplier 
        self.intercept  = intercept 
        self.input_columns  = input_columns 
        self.object_sequence_column  = object_sequence_column 
        self.data_sequence_column  = data_sequence_column 
        self.object_order_column  = object_order_column 
        self.data_order_column  = data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["object", self.object, False, (DataFrame)])
        self.__arg_info_matrix.append(["object_order_column", self.object_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["method", self.method, False, (str,list)])
        self.__arg_info_matrix.append(["scale_global", self.scale_global, True, (bool)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["multiplier", self.multiplier, True, (float,list)])
        self.__arg_info_matrix.append(["intercept", self.intercept, True, (str,list)])
        self.__arg_info_matrix.append(["input_columns", self.input_columns, True, (str,list)])
        self.__arg_info_matrix.append(["object_sequence_column", self.object_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        
        if inspect.stack()[1][3] != '_from_model_catalog':
            # Perform the function validations
            self.__validate()
            # Generate the ML query
            self.__form_tdml_query()
            # Execute ML query
            self.__execute()
            # Get the prediction type
            self._prediction_type = self.__awu._get_function_prediction_type(self)
        
        # End the timer to get the build time
        _end_time = time.time()
        
        # Calculate the build time
        self._build_time = (int)(_end_time - _start_time)
        
    def __validate(self):
        """
        Function to validate sqlmr function arguments, which verifies missing 
        arguments, input argument and table types. Also processes the 
        argument values.
        """
        if isinstance(self.object, ScaleMap):
            self.object = self.object._mlresults[0]
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.object, "object", ScaleMap)
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        
        # Check for permitted values
        method_permitted_values = ["MEAN", "SUM", "USTD", "STD", "RANGE", "MIDRANGE", "MAXABS"]
        self.__awu._validate_permitted_values(self.method, method_permitted_values, "method")
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.input_columns, "input_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.input_columns, "input_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.object_sequence_column, "object_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_sequence_column, "object_sequence_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.object_order_column, "object_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_order_column, "object_order_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        
        # Output table arguments list
        self.__func_output_args_sql_names = []
        self.__func_output_args = []
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        if self.input_columns is not None:
            self.__func_other_arg_sql_names.append("TargetColumns")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.input_columns, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("ScaleMethod")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.method, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.scale_global is not None and self.scale_global != False:
            self.__func_other_arg_sql_names.append("GlobalScale")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.scale_global, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.multiplier is not None and self.multiplier != 1.0:
            self.__func_other_arg_sql_names.append("Multiplier")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.multiplier, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.intercept is not None and self.intercept != "0":
            self.__func_other_arg_sql_names.append("Intercept")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.intercept, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.object_sequence_column is not None:
            sequence_input_by_list.append("statistic:" + UtilFuncs._teradata_collapse_arglist(self.object_sequence_column, ""))
        
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("input:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if len(sequence_input_by_list) > 0:
            self.__func_other_arg_sql_names.append("SequenceInputBy")
            sequence_input_by_arg_value = UtilFuncs._teradata_collapse_arglist(sequence_input_by_list, "'")
            self.__func_other_args.append(sequence_input_by_arg_value)
            self.__func_other_arg_json_datatypes.append("STRING")
            self._sql_specific_attributes["SequenceInputBy"] = sequence_input_by_arg_value
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process object
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.object, False)
        self.__func_input_distribution.append("DIMENSION")
        self.__func_input_arg_sql_names.append("statistic")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.object_order_column, "\""))
        
        # Process data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("ANY")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "Scale"
        # Create instance to generate SQLMR.
        self.__aqg_obj = AnalyticQueryGenerator(function_name, 
                self.__func_input_arg_sql_names, 
                self.__func_input_table_view_query, 
                self.__func_input_dataframe_type, 
                self.__func_input_distribution, 
                self.__func_input_partition_by_cols, 
                self.__func_input_order_by_cols, 
                self.__func_other_arg_sql_names, 
                self.__func_other_args, 
                self.__func_other_arg_json_datatypes, 
                self.__func_output_args_sql_names, 
                self.__func_output_args, 
                engine="ENGINE_ML")
        # Invoke call to SQL-MR generation.
        self.sqlmr_query = self.__aqg_obj._gen_sqlmr_select_stmt_sql()
        
        # Print SQL-MR query if requested to do so.
        if display.print_sqlmr_query:
            print(self.sqlmr_query)
        
        # Set the algorithm name for Model Cataloging.
        self._algorithm_name = self.__aqg_obj._get_alias_name_for_function(function_name)
        
    def __execute(self):
        """
        Function to execute SQL-MR queries. 
        Create DataFrames for the required SQL-MR outputs.
        """
        # Generate STDOUT table name and add it to the output table list.
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False)
        try:
            # Generate the output.
            UtilFuncs._create_view(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)
        
        # Update output table data frames.
        self._mlresults = []
        self.result = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.result)
        
    def show_query(self):
        """
        Function to return the underlying SQL query.
        When model object is created using retrieve_model(), then None is returned.
        """
        return self.sqlmr_query

    def get_prediction_type(self):
        """
        Function to return the Prediction type of the algorithm.
        When model object is created using retrieve_model(), then the value returned is
        as saved in the Model Catalog.
        """
        return self._prediction_type

    def get_target_column(self):
        """
        Function to return the Target Column of the algorithm.
        When model object is created using retrieve_model(), then the value returned is
        as saved in the Model Catalog.
        """
        return self._target_column

    def get_build_time(self):
        """
        Function to return the build time of the algorithm in seconds.
        When model object is created using retrieve_model(), then the value returned is
        as saved in the Model Catalog.
        """
        return self._build_time

    def _get_algorithm_name(self):
        """
        Function to return the name of the algorithm.
        """
        return self._algorithm_name

    def _get_sql_specific_attributes(self):
        """
        Function to return the dictionary containing the SQL specific attributes of the algorithm.
        """
        return self._sql_specific_attributes

    @classmethod
    def _from_model_catalog(cls,
        result = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("result", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.result  = result 
        
        # Initialize the sqlmr_query class attribute.
        obj.sqlmr_query = None
        
        # Initialize the SQL specific Model Cataloging attributes.
        obj._sql_specific_attributes = None
        obj._target_column = target_column
        obj._prediction_type = prediction_type
        obj._algorithm_name = algorithm_name
        obj._build_time = build_time
        
        # Update output table data frames.
        obj._mlresults = []
        obj.result = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.result), source_type="table", database_name=UtilFuncs._extract_db_name(obj.result))
        obj._mlresults.append(obj.result)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a Scale class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
