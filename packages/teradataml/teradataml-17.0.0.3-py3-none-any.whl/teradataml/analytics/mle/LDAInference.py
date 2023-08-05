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
# Function Version: 1.6
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
from teradataml.analytics.mle.LDA import LDA

class LDAInference:
    
    def __init__(self,
        object = None,
        data = None,
        docid_column = None,
        word_column = None,
        count_column = None,
        out_topicnum = "all",
        out_topicwordnum = "none",
        data_sequence_column = None,
        object_sequence_column = None):
        """
        DESCRIPTION:
            The LDAInference function uses the model teradataml DataFrame
            generated by the function LDA to infer the topic distribution
            in a set of new documents. You can use the distribution for tasks
            such as classification and clustering.
         
        PARAMETERS:
            object:
                Required Argument.
                Specifies the name of the model teradataml DataFrame generated
                by the  function LDA or instance of LDA, which contains the
                model.
         
            data:
                Required Argument.
                Specifies the name of the teradataml DataFrame that contains
                the new documents.
         
            docid_column:
                Required Argument.
                Specifies the name of the input column that contains the document
                identifiers.
                Types: str OR list of Strings (str)
         
            word_column:
                Required Argument.
                Specifies the name of the input column that contains the words (one
                word in each row).
                Types: str OR list of Strings (str)
         
            count_column:
                Optional Argument.
                Specifies the name of the input column that contains the count of
                the corresponding word in the row, a column of numeric type.
                Types: str OR list of Strings (str)
         
            out_topicnum:
                Optional Argument.
                Specifies the number of top-weighted topics and their weights to
                include in the output teradataml DataFrame for each training
                document. The value out_topicnum must be a positive int. The value
                "all", specifies all topics and their weights.
                Default Value: "all"
                Types: str
         
            out_topicwordnum:
                Optional Argument.
                Specifies the number of top topic words and their topic identifiers
                to include in the output teradataml DataFrame for each training
                document. The value out_topicwordnum must be a positive int. The value
                "all" specifies all topic words and their topic identifiers. The
                value, "none", specifies no topic words or topic identifiers.
                Default Value: "none"
                Types: str
         
            data_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "data". The argument is used to ensure
                deterministic results for functions which produce results that
                vary from run to run.
                Types: str OR list of Strings (str)
         
            object_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "object". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of LDAInference.
            Output teradataml DataFrames can be accessed using attribute
            references, such as LDAInferenceObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                1. doc_distribution_data
                2. output
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load example data.
            load_example_data("LDAInference", ["complaints_testtoken","complaints_traintoken"])
         
            # Create teradataml DataFrame objects.
            complaints_testtoken = DataFrame.from_table("complaints_testtoken")
            complaints_traintoken = DataFrame.from_table("complaints_traintoken")
         
            # Example 1 - Build a model using LDA and use it's output as direct input to LDAInference
            lda_out = LDA(data = complaints_traintoken,
                          topic_num = 5,
                          docid_column = "doc_id",
                          word_column = "token",
                          count_column = "frequency",
                          maxiter = 30,
                          convergence_delta = 1e-3,
                          seed = 2
                          )
         
            ldainference_out1 = LDAInference(data=complaints_testtoken,
                                  object=lda_out,
                                  docid_column='doc_id',
                                  word_column='token',
                                  count_column='frequency',
                                  out_topicnum='all',
                                  out_topicwordnum='none',
                                  data_sequence_column='doc_id',
                                  object_sequence_column='topicid'
                                  )
         
            # Print the result teradataml DataFrame
            print(ldainference_out1.doc_distribution_data)
            print(ldainference_out1.output)
         
            # Example 2 - Use the table by persisting LDA model generarted.
            # Persist the model table generated by the LDA function.
            copy_to_sql(lda_out.model_table, "model_lda_out")
         
            # Create teradataml DataFrame objects.
            model_lda_out = DataFrame.from_table("model_lda_out")
         
            ldainference_out2 = LDAInference(data=complaints_testtoken,
                                             object=model_lda_out,
                                             docid_column='doc_id',
                                             word_column='token',
                                             count_column='frequency',
                                             out_topicnum='all',
                                             out_topicwordnum='none',
                                             data_sequence_column='doc_id',
                                             object_sequence_column='topicid'
                                             )
         
            # Print the result teradataml DataFrame
            print(ldainference_out2)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.object  = object 
        self.data  = data 
        self.docid_column  = docid_column 
        self.word_column  = word_column 
        self.count_column  = count_column 
        self.out_topicnum  = out_topicnum 
        self.out_topicwordnum  = out_topicwordnum 
        self.data_sequence_column  = data_sequence_column 
        self.object_sequence_column  = object_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["object", self.object, False, (DataFrame)])
        self.__arg_info_matrix.append(["data", self.data, False, (DataFrame)])
        self.__arg_info_matrix.append(["docid_column", self.docid_column, False, (str)])
        self.__arg_info_matrix.append(["word_column", self.word_column, False, (str)])
        self.__arg_info_matrix.append(["count_column", self.count_column, True, (str)])
        self.__arg_info_matrix.append(["out_topicnum", self.out_topicnum, True, (str)])
        self.__arg_info_matrix.append(["out_topicwordnum", self.out_topicwordnum, True, (str)])
        self.__arg_info_matrix.append(["data_sequence_column", self.data_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["object_sequence_column", self.object_sequence_column, True, (str,list)])
        
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
        if isinstance(self.object, LDA):
            self.object = self.object._mlresults[0]
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.data, "data", None)
        self.__awu._validate_input_table_datatype(self.object, "object", LDA)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.docid_column, "docid_column")
        self.__awu._validate_dataframe_has_argument_columns(self.docid_column, "docid_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.word_column, "word_column")
        self.__awu._validate_dataframe_has_argument_columns(self.word_column, "word_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.count_column, "count_column")
        self.__awu._validate_dataframe_has_argument_columns(self.count_column, "count_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.data_sequence_column, "data_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.data_sequence_column, "data_sequence_column", self.data, "data", False)
        
        self.__awu._validate_input_columns_not_empty(self.object_sequence_column, "object_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_sequence_column, "object_sequence_column", self.object, "object", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__doc_distribution_data_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_ldainference0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable"]
        self.__func_output_args = [self.__doc_distribution_data_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("DocIDColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.docid_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("WordColumn")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.word_column, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.count_column is not None:
            self.__func_other_arg_sql_names.append("CountColumn")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.count_column, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.out_topicnum is not None and self.out_topicnum != "all":
            self.__func_other_arg_sql_names.append("OutputTopicNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.out_topicnum, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        if self.out_topicwordnum is not None and self.out_topicwordnum != "none":
            self.__func_other_arg_sql_names.append("OutputTopicWordNum")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.out_topicwordnum, "'"))
            self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.data_sequence_column is not None:
            sequence_input_by_list.append("InputTable:" + UtilFuncs._teradata_collapse_arglist(self.data_sequence_column, ""))
        
        if self.object_sequence_column is not None:
            sequence_input_by_list.append("ModelTable:" + UtilFuncs._teradata_collapse_arglist(self.object_sequence_column, ""))
        
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
        
        # Process object
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.object, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("ModelTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "LDAInference"
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
        self.doc_distribution_data = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__doc_distribution_data_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__doc_distribution_data_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.doc_distribution_data)
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
        doc_distribution_data = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("doc_distribution_data", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.doc_distribution_data  = doc_distribution_data 
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
        obj.doc_distribution_data = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.doc_distribution_data), source_type="table", database_name=UtilFuncs._extract_db_name(obj.doc_distribution_data))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.doc_distribution_data)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a LDAInference class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ doc_distribution_data Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.doc_distribution_data)
        return repr_string
        
