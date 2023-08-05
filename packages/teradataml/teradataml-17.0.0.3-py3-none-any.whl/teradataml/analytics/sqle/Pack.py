#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Mounika Kotha (mounika.kotha@teradata.com)
# 
# Version: 1.1
# Function Version: 1.0
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

class Pack:
    
    def __init__(self,
        data = None,
        input_columns = None,
        output_column = None,
        delimiter = ",",
        include_column_name = True,
        data_order_column = None):
        """
        DESCRIPTION:
            The Pack function packs data from multiple input columns into a 
            single column. The packed column has a virtual column for each input 
            column. By default, virtual columns are separated by commas and each 
            virtual column value is labeled with its column name.

            Note: This function is only available when teradataml is connected
                  to Vantage 1.1 or later versions.
        
        
        PARAMETERS:
             data:
                Required Argument.
                Specifies the teradataml DataFrame containing the input attributes.
                
            data_order_column:
                Optional Argument.
                Specifies Order By columns for data.
                Values to this argument can be provided as a list, if multiple 
                columns are used for ordering.
                Types: str OR list of Strings (str)
            
            input_columns:
                Optional Argument.
                Specifies the names of the input columns to pack into a single output 
                column. These names become the column names of the virtual columns. 
                By default, all input teradataml DataFrame columns are packed into a 
                single output column. If you specify this argument, but do not 
                specify all input teradataml DataFrame columns, the function copies 
                the unspecified input teradataml DataFrame columns to the output 
                teradataml DataFrame.
                Types: str OR list of Strings (str)
            
            output_column:
                Required Argument.
                Specifies the name to give to the packed output column.
                Types: str
            
            delimiter:
                Optional Argument.
                Specifies the delimiter (a string) that separates the virtual columns 
                in the packed data.
                Default Value: ","
                Types: str
            
            include_column_name:
                Optional Argument.
                Specifies whether to label each virtual column value with its column 
                name (making the virtual column "input_column:value"). 
                Default Value: True
                Types: bool
        
        RETURNS:
            Instance of Pack.
            Output teradataml DataFrames can be accessed using attribute 
            references, such as PackObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                result
        
        
        RAISES:
            TeradataMlException
        
        
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("Pack", "ville_temperature")
            
            # Create teradataml DataFrame objects.
            # The input, ville_temperature contains temperature readings for the 
            # cities Nashville and Knoxville, in the state of Tennessee.
            ville_temperature = DataFrame.from_table("ville_temperature")

            # Example1 - Default Argument Values.
            # Default values used for arguments "delimiter" and "include_column_name".
            pack_out1 = Pack(data=ville_temperature,
                            input_columns=['city','state','period','temp_f'],
                            output_column='packed_data',
                            delimiter=',',
                            include_column_name=True)
            
            # Print the results
            print(pack_out1.result)
            
            # Example2 - Nondefault Argument Values.
            # This example uses nondefault values for arguments "delimiter" and "include_column_name".
            pack_out2 = Pack(data=ville_temperature,
                            input_columns=['city','state','period','temp_f'],
                            output_column='packed_data',
                            delimiter='|',
                            include_column_name=False)
            
            # Print the results
            print(pack_out2)

        """
        # Start the timer to get the build time
        _start_time = time.time()

        self.data  = data 
        self.input_columns  = input_columns
        self.output_column  = output_column 
        self.delimiter  = delimiter
        self.include_column_name  = include_column_name
        self.data_order_column  = data_order_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["data_order_column", self.data_order_column, True, (str,list)])
        self.__arg_info_matrix.append(["input_columns", self.input_columns, True, (str,list)])
        self.__arg_info_matrix.append(["output_column", self.output_column, False, (str)])
        self.__arg_info_matrix.append(["delimiter", self.delimiter, True, (str)])
        self.__arg_info_matrix.append(["include_column_name", self.include_column_name, True, (bool)])
        
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
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.input_columns, "input_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.input_columns, "input_columns", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_order_column, "data_order_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_order_column, "data_order_column", self.data, "data", False)
        
        # Validate that value passed to the output column argument is not empty.
        self.__awu._validate_input_columns_not_empty(self.output_column, "output_column")
        
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
            self.__func_other_arg_sql_names.append("TargetColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.input_columns, "'"))
            self.__func_other_arg_json_datatypes.append("COLUMNS")
        
        self.__func_other_arg_sql_names.append("OutputColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.output_column, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.delimiter is not None and self.delimiter != ",":
            self.__func_other_arg_sql_names.append("Delimiter")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.delimiter, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.include_column_name is not None and self.include_column_name != True:
            self.__func_other_arg_sql_names.append("IncludeColumnName")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.include_column_name, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        
        # Declare empty lists to hold input table information.
        self.__func_input_arg_sql_names = []
        self.__func_input_table_view_query = []
        self.__func_input_dataframe_type = []
        self.__func_input_distribution = []
        self.__func_input_partition_by_cols = []
        self.__func_input_order_by_cols = []
        
        # Process data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("FACT")
        self.__func_input_arg_sql_names.append("input")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("ANY")
        self.__func_input_order_by_cols.append(UtilFuncs._teradata_collapse_arglist(self.data_order_column, "\""))
        
        function_name = "Pack"
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
                engine="ENGINE_SQL")
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
        Returns the string representation for a Pack class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.result)
        return repr_string
        
