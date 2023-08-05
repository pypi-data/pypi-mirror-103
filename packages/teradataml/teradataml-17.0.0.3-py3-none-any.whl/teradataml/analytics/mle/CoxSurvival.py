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
# Function Version: 1.10
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
from teradataml.analytics.mle.CoxPH import CoxPH

class CoxSurvival:
    
    def __init__(self,
        object = None,
        cox_model_table = None,
        predict_table = None,
        predict_feature_names = None,
        predict_feature_columns = None,
        accumulate = None,
        cox_model_table_sequence_column = None,
        object_sequence_column = None,
        predict_table_sequence_column = None):
        """
        DESCRIPTION:
            The CoxSurvival function takes as input the coefficient and linear
            prediction tables generated by the function CoxPH and outputs a
            teradataml DataFrame of survival probabilities.
         
         
        PARAMETERS:
            object:
                Required Argument.
                Specifies the teradataml DataFrame of the Cox coefficient model, which was
                output by the CoxPH function or instance of CoxPH.
         
            cox_model_table:
                Required Argument.
                Specifies the teradataml DataFrame of the Cox linear predictor model, which was
                output by the CoxPH function.
         
            predict_table:
                Required Argument.
                Specifies the teradataml DataFrame, which contains new
                prediction feature values for survival calculation.
         
            predict_feature_names:
                Required Argument.
                Specifies the names of features in the Cox model.
                Types: str OR list of Strings (str)
         
            predict_feature_columns:
                Required Argument.
                Specifies the names of the columns that contain the values for the
                features in the Cox model—one column name for each feature name. The
                ith feature name corresponds to the ith column name. For example,
                consider this pair of arguments: predict.feature.names("name",
                "age"), predict.feature.columns("c1", "c2") The predictive values of
                the feature "name" are in column "c1", and the predictive values of
                the feature "age" are in column "c2".
                Types: str OR list of Strings (str)
         
            accumulate:
                Optional Argument.
                Specifies the names of the columns in predict_table that the function
                copies to the output table.
                Types: str OR list of Strings (str)
         
            cox_model_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "cox_model_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            object_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "object". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
            predict_table_sequence_column:
                Optional Argument.
                Specifies the list of column(s) that uniquely identifies each row of
                the input argument "predict_table". The argument is used to ensure
                deterministic results for functions which produce results that vary
                from run to run.
                Types: str OR list of Strings (str)
         
        RETURNS:
            Instance of CoxSurvival.
            Output teradataml DataFrames can be accessed using attribute
            references, such as CoxSurvivalObj.<attribute_name>.
            Output teradataml DataFrame attribute name is:
                1. output
                2. survival_probability
         
         
        RAISES:
            TeradataMlException
         
         
        EXAMPLES:
            # Load the data to run the example.
            load_example_data("coxsurvival", ["lc_new_predictors", "lungcancer"])
         
            # Create teradataml DataFrame objects.
            lungcancer = DataFrame.from_table("lungcancer")
            lc_new_predictors = DataFrame.from_table("lc_new_predictors")
         
            # Generate CoxPH model object.
            coxph_out = CoxPH(data = lungcancer,
                              feature_columns = ["trt","celltype","karno","diagtime","age","prior"],
                              time_interval_column = "time_int",
                              event_column = "status",
                              categorical_columns = ["trt","celltype","prior"])
         
            # linear model predictor table and coefficient table that are generated from the td_coxph function
            # are used to determine the survival probabilities of the new patients.
            # Example 1 - Pass generated coefficient table and linear predictor dataframes
            cox_survival_out = CoxSurvival(object = coxph_out.coefficient_table,
                                           cox_model_table = coxph_out.linear_predictor_table,
                                           predict_table = lc_new_predictors,
                                           predict_feature_names = ["trt", "celltype","karno","diagtime","age","prior"],
                                           predict_feature_columns = ["trt","celltype","karno","diagtime","age", "prior"],
                                           accumulate = ["id", "name"])
         
            # Print the results.
            print(cox_survival_out.output)
            print(cox_survival_out.survival_probability)
         
            # Example 2 - Pass output of coxph_out directly as object argument.
            cox_survival_out = CoxSurvival(object = coxph_out,
                                           cox_model_table = coxph_out.linear_predictor_table,
                                           predict_table = lc_new_predictors,
                                           predict_feature_names = ["trt", "celltype","karno","diagtime","age","prior"],
                                           predict_feature_columns = ["trt","celltype","karno","diagtime","age", "prior"],
                                           accumulate = ["id", "name"])
         
            # Print the results.
            print(cox_survival_out.output)
            print(cox_survival_out.survival_probability)
        
        """
        
        # Start the timer to get the build time
        _start_time = time.time()
        
        self.object  = object 
        self.cox_model_table  = cox_model_table 
        self.predict_table  = predict_table 
        self.predict_feature_names  = predict_feature_names 
        self.predict_feature_columns  = predict_feature_columns 
        self.accumulate  = accumulate 
        self.cox_model_table_sequence_column  = cox_model_table_sequence_column 
        self.object_sequence_column  = object_sequence_column 
        self.predict_table_sequence_column  = predict_table_sequence_column 
        
        # Create TeradataPyWrapperUtils instance which contains validation functions.
        self.__awu = AnalyticsWrapperUtils()
        self.__aed_utils = AedUtils()
        
        # Create argument information matrix to do parameter checking
        self.__arg_info_matrix = []
        self.__arg_info_matrix.append(["object", self.object, False, (DataFrame)])
        self.__arg_info_matrix.append(["cox_model_table", self.cox_model_table, False, (DataFrame)])
        self.__arg_info_matrix.append(["predict_table", self.predict_table, False, (DataFrame)])
        self.__arg_info_matrix.append(["predict_feature_names", self.predict_feature_names, False, (str,list)])
        self.__arg_info_matrix.append(["predict_feature_columns", self.predict_feature_columns, False, (str,list)])
        self.__arg_info_matrix.append(["accumulate", self.accumulate, True, (str,list)])
        self.__arg_info_matrix.append(["cox_model_table_sequence_column", self.cox_model_table_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["object_sequence_column", self.object_sequence_column, True, (str,list)])
        self.__arg_info_matrix.append(["predict_table_sequence_column", self.predict_table_sequence_column, True, (str,list)])
        
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
        if isinstance(self.object, CoxPH):
            self.object = self.object._mlresults[0]
        
        # Make sure that a non-NULL value has been supplied for all mandatory arguments
        self.__awu._validate_missing_required_arguments(self.__arg_info_matrix)
        
        # Make sure that a non-NULL value has been supplied correct type of argument
        self.__awu._validate_argument_types(self.__arg_info_matrix)
        
        # Check to make sure input table types are strings or data frame objects or of valid type.
        self.__awu._validate_input_table_datatype(self.cox_model_table, "cox_model_table", None)
        self.__awu._validate_input_table_datatype(self.object, "object", CoxPH)
        self.__awu._validate_input_table_datatype(self.predict_table, "predict_table", None)
        
        # Check whether the input columns passed to the argument are not empty.
        # Also check whether the input columns passed to the argument valid or not.
        self.__awu._validate_input_columns_not_empty(self.predict_feature_columns, "predict_feature_columns")
        self.__awu._validate_dataframe_has_argument_columns(self.predict_feature_columns, "predict_feature_columns", self.predict_table, "predict_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.accumulate, "accumulate")
        self.__awu._validate_dataframe_has_argument_columns(self.accumulate, "accumulate", self.predict_table, "predict_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.cox_model_table_sequence_column, "cox_model_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.cox_model_table_sequence_column, "cox_model_table_sequence_column", self.cox_model_table, "cox_model_table", False)
        
        self.__awu._validate_input_columns_not_empty(self.object_sequence_column, "object_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.object_sequence_column, "object_sequence_column", self.object, "object", False)
        
        self.__awu._validate_input_columns_not_empty(self.predict_table_sequence_column, "predict_table_sequence_column")
        self.__awu._validate_dataframe_has_argument_columns(self.predict_table_sequence_column, "predict_table_sequence_column", self.predict_table, "predict_table", False)
        
        
    def __form_tdml_query(self):
        """
        Function to generate the analytical function queries. The function defines 
        variables and list of arguments required to form the query.
        """
        # Generate temp table names for output table parameters if any.
        self.__survival_probability_temp_tablename = UtilFuncs._generate_temp_table_name(prefix="td_coxsurvival0", use_default_database=True, gc_on_quit=True, quote=False, table_type=TeradataConstants.TERADATA_TABLE)
        
        # Output table arguments list
        self.__func_output_args_sql_names = ["OutputTable"]
        self.__func_output_args = [self.__survival_probability_temp_tablename]
        
        # Model Cataloging related attributes.
        self._sql_specific_attributes = {}
        self._sql_formula_attribute_mapper = {}
        self._target_column = None
        self._algorithm_name = None
        
        # Generate lists for rest of the function arguments
        self.__func_other_arg_sql_names = []
        self.__func_other_args = []
        self.__func_other_arg_json_datatypes = []
        
        self.__func_other_arg_sql_names.append("PredictFeatureColumns")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.predict_feature_columns, "\""), "'"))
        self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        if self.accumulate is not None:
            self.__func_other_arg_sql_names.append("Accumulate")
            self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(UtilFuncs._teradata_quote_arg(self.accumulate, "\""), "'"))
            self.__func_other_arg_json_datatypes.append("COLUMN_NAMES")
        
        self.__func_other_arg_sql_names.append("PredictFeatureNames")
        self.__func_other_args.append(UtilFuncs._teradata_collapse_arglist(self.predict_feature_names, "'"))
        self.__func_other_arg_json_datatypes.append("STRING")
        
        # Generate lists for rest of the function arguments
        sequence_input_by_list = []
        if self.cox_model_table_sequence_column is not None:
            sequence_input_by_list.append("CoxLinearPredictorModelTable:" + UtilFuncs._teradata_collapse_arglist(self.cox_model_table_sequence_column, ""))
        
        if self.object_sequence_column is not None:
            sequence_input_by_list.append("CoxCoefModelTable:" + UtilFuncs._teradata_collapse_arglist(self.object_sequence_column, ""))
        
        if self.predict_table_sequence_column is not None:
            sequence_input_by_list.append("PredictTable:" + UtilFuncs._teradata_collapse_arglist(self.predict_table_sequence_column, ""))
        
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
        
        # Process cox_model_table
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.cox_model_table, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("CoxLinearPredictorModelTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        # Process object
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.object, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("CoxCoefModelTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        # Process predict_table
        self.__table_ref = self.__awu._teradata_on_clause_from_dataframe(self.predict_table, False)
        self.__func_input_distribution.append("NONE")
        self.__func_input_arg_sql_names.append("PredictTable")
        self.__func_input_table_view_query.append(self.__table_ref["ref"])
        self.__func_input_dataframe_type.append(self.__table_ref["ref_type"])
        self.__func_input_partition_by_cols.append("NA_character_")
        self.__func_input_order_by_cols.append("NA_character_")
        
        function_name = "CoxSurvival"
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
        self.survival_probability = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(self.__survival_probability_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(self.__survival_probability_temp_tablename))
        self.output = self.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(sqlmr_stdout_temp_tablename), source_type="table", database_name=UtilFuncs._extract_db_name(sqlmr_stdout_temp_tablename))
        self._mlresults.append(self.survival_probability)
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
        survival_probability = None,
        output = None,
        **kwargs):
        """
        Classmethod is used by Model Cataloging, to instantiate this wrapper class.
        """
        kwargs.pop("survival_probability", None)
        kwargs.pop("output", None)
        
        # Model Cataloging related attributes.
        target_column = kwargs.pop("__target_column", None)
        prediction_type = kwargs.pop("__prediction_type", None)
        algorithm_name = kwargs.pop("__algorithm_name", None)
        build_time = kwargs.pop("__build_time", None)

        # Let's create an object of this class.
        obj = cls(**kwargs)
        obj.survival_probability  = survival_probability 
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
        obj.survival_probability = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.survival_probability), source_type="table", database_name=UtilFuncs._extract_db_name(obj.survival_probability))
        obj.output = obj.__awu._create_data_set_object(df_input=UtilFuncs._extract_table_name(obj.output), source_type="table", database_name=UtilFuncs._extract_db_name(obj.output))
        obj._mlresults.append(obj.survival_probability)
        obj._mlresults.append(obj.output)
        return obj
        
    def __repr__(self):
        """
        Returns the string representation for a CoxSurvival class instance.
        """
        repr_string="############ STDOUT Output ############"
        repr_string = "{}\n\n{}".format(repr_string,self.output)
        repr_string="{}\n\n\n############ survival_probability Output ############".format(repr_string)
        repr_string = "{}\n\n{}".format(repr_string,self.survival_probability)
        return repr_string
        
