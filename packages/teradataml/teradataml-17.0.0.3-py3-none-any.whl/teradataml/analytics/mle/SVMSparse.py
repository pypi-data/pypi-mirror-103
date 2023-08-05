#!/usr/bin/python
# ################################################################## 
# 
# Copyright 2018 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
# 
# Primary Owner: Pankaj Purandare (pankajvinod.purandare@teradata.com)
# Secondary Owner: Rohit Agrawal (rohit.agrawal@teradata.com)
# 
# Version: 1.2
# Function Version: 1.7
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
from teradataml.options.configure import configure

class SVMSparse:
    
    def __init__(self,
        data = None,
        sample_id_column = None,
        attribute_column = None,
        value_column = None,
        label_column = None,
        cost = 1.0,
        bias = 0.0,
        hash = False,
        hash_buckets = None,
        class_weights = None,
        max_step = 100,
        epsilon = 0.01,
        seed = 0,
        data_sequence_column = None,
        force_mapreduce = False):
        """
        DESCRIPTION:
            The SVMSparse function takes training data (in sparse format) and
            outputs a predictive model in binary format, which is input to the
            functions SVMSparsePredict and SVMSparseSummary.
         
         
        PARAMETERS:
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains 
                the training samples.
            
            sample_id_column:
                Required Argument.
                Specifies the name of the column in data, teradataml DataFrame
                that contains the identifiers of the training samples.
                Types: str
            
            attribute_column:
                Required Argument.
                Specifies the name of the column in data, teradataml DataFrame 
                that contains the attributes of the samples.
                Types: str
            
            value_column:
                Optional Argument. Required when teradataml is connected to
                Vantage 1.3 version.
                Specifies the name of the column in data, teradataml DataFrame
                that contains the attribute values.
                Types: str
            
            label_column:
                Required Argument.
                Specifies the name of the column in data, teradataml DataFrame
                that contains the classes of the samples.
                Types: str
            
            cost:
                Optional Argument.
                Specifies the regularization parameter in the SVM soft-margin loss function:
                Cost must be greater than 0.0.
                Default Value: 1.0
                Types: float
            
            bias:
                Optional Argument.
                Specifies a non-negative value. If the value is greater than zero, each sample
                x in the training set will be converted to (x, b); that is, it will
                add another dimension containing the bias value b. This argument
                addresses situations where not all samples center at 0.
                Default Value: 0.0
                Types: float
            
            hash:
                Optional Argument.
                Specifies whether to use hash projection on attributes. hash
                projection can accelerate processing speed but can slightly decrease
                accuracy.
                Note: You must use hash projection if the dataset has more
                      features than fit into memory.
                Default Value: False
                Types: bool
            
            hash_buckets:
                Optional Argument.
                Valid only if hash is True. Specifies the number of buckets for
                hash projection. In most cases, the function can determine the
                appropriate number of buckets from the scale of the input data set.
                However, if the dataset has a very large number of features, you
                might have to specify buckets_number to accelerate the function.
                Types: int
            
            class_weights:
                Optional Argument.
                Specifies the weights for different classes. The format is:
                "classlabel m:weight m, classlabel n:weight n". If weight for a class
                is given, the cost parameter for this class is weight * cost. A
                weight larger than 1 often increases the accuracy of the
                corresponding class; however, it may decrease global accuracy.
                Classes not assigned a weight in this argument is assigned a weight
                of 1.0.
                Types: str OR list of Strings (str)
            
            max_step:
                Optional Argument.
                Specifies a positive integer value that specifies the maximum number of
                iterations of the training process. One step means that each sample
                is seen once by the trainer. The input value must be in the range (0,
                10000].
                Default Value: 100
                Types: int
            
            epsilon:
                Optional Argument.
                Specifies the termination criterion. When the difference between the values of the
                loss function in two sequential iterations is less than this number,
                the function stops. epsilon must be greater than 0.0.
                Default Value: 0.01
                Types: float
            
            seed:
                Optional Argument.
                A long integer value used to order the training set randomly and
                consistently. This value can be used to ensure that the same model
                will be generated if the function is run multiple times in a given
                database with the same arguments. The input value must be in the
                range [0, 9223372036854775807].
                Default Value: 0
                Types: int
            
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)

            force_mapreduce:
                Optional Argument.
                Specifies whether the function is to use MapReduce. If set to
                'False', a lighter version of the function runs for faster results.
                Note:
                    1. The model may be different with "force_mapreduce" set to 'True' and
                       "force_mapreduce" set to 'False'.
                    2. "force_mapreduce" argument support is only available when teradataml
                       is connected to Vantage 1.3 version.
                Default Value: False
                Types: bool
         
        RETURNS:
            Instance of SVMSparse.
            Output teradataml DataFrames can be accessed using attribute
            references, such as SVMSparseObj.<attribute_name>.
            Output teradataml DataFrame attribute names are:
                1. model_table
                2. output
         
         
        RAISES:
            TeradataMlException, TypeError, ValueError
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("SVMSparse","svm_iris_input_train")

            # Create teradataml DataFrame
            svm_iris_input_train = DataFrame.from_table("svm_iris_input_train")

            # Example 1
            svm_sparse_out = SVMSparse(data=svm_iris_input_train,
                                       sample_id_column='id',
                                       attribute_column='attribute',
                                       label_column='species',
                                       value_column='value1',
                                       max_step=150,
                                       seed=0,
                                       )
            # Print the result DataFrame
            print(svm_sparse_out.model_table)
            print(svm_sparse_out.output)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.data  = data 
        self.sample_id_column  = sample_id_column 
        self.attribute_column  = attribute_column 
        self.value_column  = value_column 
        self.label_column  = label_column 
        self.cost  = cost 
        self.bias  = bias 
        self.hash  = hash 
        self.hash_buckets  = hash_buckets 
        self.class_weights  = class_weights 
        self.max_step  = max_step 
        self.epsilon  = epsilon 
        self.seed  = seed 
        self.force_mapreduce  = force_mapreduce
        self.data_sequence_column  = data_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["sample_id_column", self.sample_id_column, False, (str)])
        self.__arg_info_matrix.append(["attribute_column", self.attribute_column, False, (str)])
        self.__arg_info_matrix.append(["value_column", self.value_column, configure._vantage_version != "vantage1.3", (str)])
        self.__arg_info_matrix.append(["label_column", self.label_column, False, (str)])
        self.__arg_info_matrix.append(["cost", self.cost, True, (float)])
        self.__arg_info_matrix.append(["bias", self.bias, True, (float)])
        self.__arg_info_matrix.append(["hash", self.hash, True, (bool)])
        self.__arg_info_matrix.append(["hash_buckets", self.hash_buckets, True, (int)])
        self.__arg_info_matrix.append(["class_weights", self.class_weights, True, (str,list)])
        self.__arg_info_matrix.append(["max_step", self.max_step, True, (int)])
        self.__arg_info_matrix.append(["epsilon", self.epsilon, True, (float)])
        self.__arg_info_matrix.append(["seed", self.seed, True, (int)])
        self.__arg_info_matrix.append(["force_mapreduce", self.force_mapreduce, True, (bool)])
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
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.sample_id_column, "sample_id_column")
        self.__awu._validate_dataframe_has_argument_columns(self.sample_id_column, "sample_id_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.attribute_column, "attribute_column")
        self.__awu._validate_dataframe_has_argument_columns(self.attribute_column, "attribute_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.label_column, "label_column")
        self.__awu._validate_dataframe_has_argument_columns(self.label_column, "label_column", self.data, "data", False)
        self.__awu._validate_input_columns_not_empty(self.value_column, "value_column")
        self.__awu._validate_dataframe_has_argument_columns(self.value_column, "value_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__model_table_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_svmsparse0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["ModelTable"]
        self.__func_output_args = [self.__model_table_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("IDColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.sample_id_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("AttributeNameColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.attribute_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")

        self.__func_other_arg_sql_names.append("ResponseColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.label_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")

        if self.value_column is not None:
            self.__func_other_arg_sql_names.append("AttributeValueColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.value_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.hash is not None and self.hash != False:
            self.__func_other_arg_sql_names.append("HashProjection")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.hash, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.hash_buckets is not None:
            self.__func_other_arg_sql_names.append("HashBuckets")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.hash_buckets, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.force_mapreduce is not None and self.force_mapreduce != False:
            self.__func_other_arg_sql_names.append("ForceMapReduce")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.force_mapreduce, "'"))
            self.__func_other_arg_json_datatypes.append("BOOLEAN")
        
        if self.cost is not None and self.cost != 1.0:
            self.__func_other_arg_sql_names.append("Cost")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.cost, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.bias is not None and self.bias != 0.0:
            self.__func_other_arg_sql_names.append("Bias")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.bias, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.class_weights is not None:
            self.__func_other_arg_sql_names.append("ClassWeights")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.class_weights, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.max_step is not None and self.max_step != 100:
            self.__func_other_arg_sql_names.append("MaxStep")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.max_step, "'"))
            self.__func_other_arg_json_datatypes.append("INTEGER")
        
        if self.epsilon is not None and self.epsilon != 0.01:
            self.__func_other_arg_sql_names.append("Epsilon")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.epsilon, "'"))
            self.__func_other_arg_json_datatypes.append("DOUBLE")
        
        if self.seed is not None and self.seed != 0:
            self.__func_other_arg_sql_names.append("Seed")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.seed, "'"))
            self.__func_other_arg_json_datatypes.append("LONG")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
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
        
        # Process data
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.data, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("InputTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "SVMSparse"
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
        sqlmr_stdout_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_sqlmr_out_", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        try:
            # Generate the output.
            UtilFuncs._create_table(sqlmr_stdout_temp_tablename, self.sqlmr_query)
        except Exception as emsg:
            raise TeradataMlException(Messages.get_message(MessageCodes.TDMLDF_EXEC_SQL_FAILED, str(emsg)), MessageCodes.TDMLDF_EXEC_SQL_FAILED)
        
        # Update output table data frames.
        self._mlresults = []
        self.model_table = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__model_table_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__model_table_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.model_table)
        self._mlresults.append(self.output)
        
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
        model_table = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("model_table", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)
        
        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.model_table  = model_table 
        obj.output  = output 
        
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
        obj.model_table = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.model_table), source_type="table", database_name=UtilFuncs._extract_db_name(obj.model_table))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.model_table)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a SVMSparse class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ model_table Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.model_table)
        return repr_string
        
